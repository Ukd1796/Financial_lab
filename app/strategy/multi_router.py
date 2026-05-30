# app/strategy/multi_router.py
#
# MultiStrategyRouter — runs multiple strategies simultaneously on a shared
# portfolio and merges their decisions into a single list for RiskAgent.
#
# Design constraints
# ------------------
# 1. Strategies use two different decide() signatures:
#      Multi-symbol : decide(current_date, symbol_states, portfolio) → list[Decision]
#      Per-symbol   : decide(market_state, portfolio)                → Decision
#    The router detects this once at construction time (no per-call reflection).
#
# 2. Conflict resolution is risk-first:
#      SELL > BUY > HOLD
#    When two strategies disagree at the same priority level the higher-weight
#    strategy's decision is kept.
#
# 3. The winning Decision carries .weight and .source.
#    RiskAgent uses .weight to scale position size — a strategy at weight 0.30
#    sizes positions to 30% of what it would deploy at full weight.
#
# 4. update_weights() is called by AdaptiveStrategySelector (step 12) each week
#    to shift capital allocation based on the current market regime.

import inspect
from datetime import datetime

from app.strategy.models import Decision

_ACTION_PRIORITY = {"SELL": 2, "BUY": 1, "HOLD": 0}


class MultiStrategyRouter:
    """
    Aggregates decisions from N strategies on a shared portfolio.

    Parameters
    ----------
    strategies : dict[str, strategy_instance]
        Named strategy objects. Keys are used as the Decision.source label.
        Example: {"DualMA": DualMovingAverageStrategy(), "Breakout": BreakoutMomentumStrategy()}

    weights : dict[str, float] | None
        Capital weight per strategy. Automatically normalised to sum to 1.0.
        Defaults to equal weighting across all strategies.
        Values below 0.01 are treated as effectively disabled (skipped entirely).

    allowed_regimes : dict[str, list[str] | None] | None
        Per-strategy regime allowlist. Before calling a strategy's decide(),
        symbol_states is filtered to only include symbols whose regime is in
        the strategy's allowlist. None means no filtering for that strategy.
        Example: {"RSI-MR": ["LOW_VOL_UPTREND", "MID_VOL_UPTREND", ...],
                  "DualMA": None}  # DualMA sees all regimes

    Usage
    -----
    router = MultiStrategyRouter(
        strategies={"DualMA": dual_ma, "Breakout": breakout, ...},
        weights={"DualMA": 0.30, "Breakout": 0.25, ...},
        allowed_regimes={"DualMA": _UPTREND_ONLY, "RSI-MR": _UPTREND_AND_SIDEWAYS, ...},
    )
    # BacktestEngine treats this as a multi-symbol strategy (3-param decide)
    decisions = router.decide(current_date, symbol_states, portfolio)
    """

    def __init__(
        self,
        strategies: dict,
        weights: dict | None = None,
        allowed_regimes: dict | None = None,
        allow_cross_strategy_exits: bool = False,
        cross_exit_strategies: set | None = None,
        per_strategy_universe_source=None,
        exclusive_strategies: set | None = None,
    ):
        self.strategies      = strategies
        self.weights         = self._normalise(
            weights or {k: 1.0 for k in strategies}
        )
        # Per-strategy regime allowlists — None means no regime filtering
        self.allowed_regimes = allowed_regimes or {}

        # Experimental: when True, any strategy can SELL any position
        # (cross-strategy exits allowed). When False (default, legacy
        # behavior), only the strategy that opened the position may close
        # it via a strategy signal — though the RiskAgent's ATR trailing
        # stop already overrides this rule.
        #
        # Background: signal-drop diagnostics revealed that TrendPB and
        # RSI-MR collectively issue ~3,600 blocked SELL signals per period
        # against Breakout-owned positions in Live 2025-26. Removing the
        # block lets those exit signals fire. Trade-off: in directional
        # regimes (Bull, Recovery, Recent) where positions are winning,
        # cross-strategy exits will prematurely cut winners. A/B test
        # required to determine net effect.
        # See docs/next_explorations.md.
        self.allow_cross_strategy_exits = allow_cross_strategy_exits

        # Selective cross-exit: only named strategies may SELL positions they
        # did not open. Narrower than allow_cross_strategy_exits (which lifts
        # the gate for everyone). {"TrendPB"} = only TrendPB can exit Breakout
        # positions, letting its price-recovery and max-hold-days exit signals
        # fire on Breakout-owned stock without allowing all strategies to do so.
        # Requires dispatch to also show cross-exit strategies ALL held positions
        # (not just their own + regime-matched ones) so signals can generate.
        self.cross_exit_strategies: set = cross_exit_strategies or set()

        # Optional per-strategy universe gate. When set, this callable returns
        # {strategy_name: set[symbol]} for the *current bar* — typically a
        # closure over UnionUniverseFilter.last_per_strategy_symbols. Each
        # strategy then sees only the symbols its own universe filter selected
        # (plus held positions for exits). Without this gate, every strategy
        # sees the merged active_symbols, allowing one strategy to fire on
        # another's intended slice (e.g. Breakout poaching QuietBrk's quiet
        # stocks). Strategies whose name is absent from the dict bypass the
        # gate (backwards-compat for untagged unions).
        self.per_strategy_universe_source = per_strategy_universe_source

        # Asymmetric gate: only strategies named here get the "see only my
        # slice" treatment. Every other strategy sees (merged - union of
        # exclusive slices) — i.e. their universe is reduced by exactly the
        # symbols reserved for exclusive strategies, but they still poach
        # freely across the remaining slices.
        #
        # Rationale: the symmetric gate (every tagged strategy on its own
        # slice) regressed Adapt+RCA -4.85pp Crash / -9.47pp Recent because
        # Breakout's broad poaching was generating real PnL. An asymmetric
        # gate scoped to {"QuietBrk"} only takes ~10% of Breakout's surface
        # (the quiet slice) while giving QuietBrk an uncontested lane to
        # express its standalone Sharpe-2 behavior. See plan file
        # `velvet-swimming-harbor.md` for the full design.
        #
        # Empty / None = no asymmetry; falls through to the symmetric gate
        # (if per_strategy_universe_source set) or legacy (if not).
        self.exclusive_strategies: set = exclusive_strategies or set()

        # Detect dispatch mode once — avoids repeated introspection per bar
        self._multi_symbol: dict[str, bool] = {
            name: (len(inspect.signature(s.decide).parameters) == 3)
            for name, s in strategies.items()
        }

        # Tracks which strategy entered each open position.
        # Only the owning strategy (or the ATR stop in RiskAgent) may close it
        # by default. The allow_cross_strategy_exits flag (above) bypasses
        # this rule when set.
        self.position_owners: dict[str, str] = {}

        # ----------------------------------------------------------------
        # Per-strategy signal-drop diagnostics — see docs/next_explorations.md §5.
        # Counts how often each strategy's raw decisions get filtered/dropped
        # by the merge mechanism. Surfaces the "solo positive but combined
        # negative" mystery numerically. Reset is intentional: counters are
        # cumulative across the whole backtest so the harness can report at
        # end-of-period. The engine adds a `buy_rejected` counter separately
        # for post-router cash/breadth/ATR rejections.
        # ----------------------------------------------------------------
        self.diag_counters: dict[str, dict] = {
            name: {
                "signals_issued":    0,   # raw decisions strategy proposed
                "won_merge":         0,   # decisions kept after the priority/weight contest
                "dropped_priority":  0,   # decisions overridden by a competing strategy on same symbol
                "dropped_ownership": 0,   # SELL skipped because strategy didn't own the position
                "conflict_count":    0,   # times two strategies proposed different actions on same symbol
                "conflict_log":      [],  # sample of (symbol, own_action, rival, their_action); capped at 50
                "cross_exits":       0,   # SELLs that fired on another strategy's position (selective CSX)
            }
            for name in strategies
        }

    # ------------------------------------------------------------------
    # PUBLIC API
    # ------------------------------------------------------------------
    def update_weights(self, weights: dict) -> None:
        """Replace the current weight vector (called by AdaptiveStrategySelector)."""
        self.weights = self._normalise(weights)

    def decide(
        self,
        current_date: datetime,
        symbol_states: dict,
        portfolio,
    ) -> list[Decision]:
        """
        Collect decisions from every active strategy and merge them.

        The merged list contains at most one Decision per symbol.
        Each Decision carries .weight (for RiskAgent sizing) and
        .source (which strategy generated it).

        Ownership rule: only the strategy that BUYed a position may SELL it.
        This prevents cross-strategy premature exits (e.g. RSI-MR selling a
        DualMA position because RSI crossed 80 mid-trend).  ATR stops in
        RiskAgent are unaffected — they run after this layer.
        """
        # Sync ownership map: remove positions that are no longer held
        # (could have been closed by an ATR stop or a prior-round SELL).
        held = set(portfolio.positions.keys())
        self.position_owners = {
            k: v for k, v in self.position_owners.items() if k in held
        }

        # symbol → (Decision, weight, strategy_name)
        merged: dict[str, tuple] = {}

        for name, strategy in self.strategies.items():
            w = self.weights.get(name, 0.0)
            if w < 0.01:
                continue  # effectively disabled — skip entirely

            # Collect raw decisions from this strategy
            raw: list[Decision] = self._dispatch(
                name, strategy, current_date, symbol_states, portfolio
            )

            for d in raw:
                if d is None:
                    continue

                # Track every raw decision the strategy issued (excluding None).
                # This is the denominator for "what % of signals got through".
                self.diag_counters[name]["signals_issued"] += 1

                # Ownership gate: by default, ignore SELL from a strategy that
                # did not open this position. The owning strategy and untracked
                # positions always pass. Two ways to bypass:
                #   allow_cross_strategy_exits=True  — everyone may SELL anything
                #   cross_exit_strategies={name}     — only listed strategies may
                if d.action == "SELL" and not self.allow_cross_strategy_exits:
                    owner = self.position_owners.get(d.symbol)
                    if owner is not None and owner != name:
                        if name not in self.cross_exit_strategies:
                            self.diag_counters[name]["dropped_ownership"] += 1
                            continue  # cross-strategy exit — blocked
                        # Selective cross-exit: allowed for this strategy
                        self.diag_counters[name]["cross_exits"] += 1

                self._merge_into(merged, d, w, name)

        # Stamp weight + source onto the winning decision for each symbol;
        # update ownership tracking. Increment won_merge for the winning
        # strategy per symbol — this is the post-priority/post-weight survivor.
        result = []
        for sym, (d, w, name) in merged.items():
            d.weight = w
            d.source = name
            if d.action == "BUY":
                self.position_owners[sym] = name
            elif d.action == "SELL":
                self.position_owners.pop(sym, None)
            self.diag_counters[name]["won_merge"] += 1
            result.append(d)

        return result

    # ------------------------------------------------------------------
    # INTERNAL HELPERS
    # ------------------------------------------------------------------
    def _dispatch(
        self,
        name: str,
        strategy,
        current_date: datetime,
        symbol_states: dict,
        portfolio,
    ) -> list[Decision]:
        """
        Apply per-strategy regime filter, then call strategy.decide() in the
        correct dispatch mode.

        Held positions owned by THIS strategy are always included regardless of
        regime so that exit signals (SELL / HOLD for ATR stop) can fire.
        Positions owned by other strategies are excluded — exit responsibility
        lies with the owning strategy.  Untracked positions (no owner recorded)
        are included as a safe fallback.
        """
        # Symbols this strategy owns (should always receive exit signals)
        owned = {
            sym for sym, owner in self.position_owners.items() if owner == name
        }

        # ── Per-strategy universe gate ────────────────────────────────────
        # Two modes depending on `exclusive_strategies`:
        #
        # ASYMMETRIC (`exclusive_strategies` non-empty):
        #   - If `name` is in exclusive_strategies → see only `slices[name]`
        #     (reserved private lane).
        #   - Else → see (merged - union of all exclusive slices). Keeps the
        #     strategy's normal poaching reach minus the reserved symbols.
        #
        # SYMMETRIC (legacy gate, `exclusive_strategies` empty):
        #   - If `name` is in slices → see only `slices[name]`.
        #   - Else → no filtering (backwards-compat for untagged routers).
        #
        # Bypass rules (both modes): own positions, untracked positions, and
        # cross-exit strategies pass through so exit signals always fire.
        if self.per_strategy_universe_source is not None:
            slices = self.per_strategy_universe_source() or {}

            if self.exclusive_strategies:
                # Asymmetric mode
                excluded_union: set = set()
                for excl_name in self.exclusive_strategies:
                    excluded_union |= slices.get(excl_name, set())

                if name in self.exclusive_strategies:
                    allowed_syms = slices.get(name, set())
                    symbol_states = {
                        sym: state for sym, state in symbol_states.items()
                        if sym in allowed_syms
                        or sym in owned
                        or (
                            sym in portfolio.positions
                            and sym not in self.position_owners
                        )
                        or (
                            name in self.cross_exit_strategies
                            and sym in portfolio.positions
                        )
                    }
                elif excluded_union:
                    symbol_states = {
                        sym: state for sym, state in symbol_states.items()
                        if sym not in excluded_union
                        or sym in owned
                        or (
                            sym in portfolio.positions
                            and sym not in self.position_owners
                        )
                        or (
                            name in self.cross_exit_strategies
                            and sym in portfolio.positions
                        )
                    }
            elif name in slices:
                # Symmetric mode (legacy)
                allowed_syms = slices[name]
                symbol_states = {
                    sym: state for sym, state in symbol_states.items()
                    if sym in allowed_syms
                    or sym in owned
                    or (
                        sym in portfolio.positions
                        and sym not in self.position_owners
                    )
                    or (
                        name in self.cross_exit_strategies
                        and sym in portfolio.positions
                    )
                }

        regimes = self.allowed_regimes.get(name)
        if regimes is not None:
            filtered_states = {
                sym: state for sym, state in symbol_states.items()
                if state.indicators.get("regime") in regimes
                or sym in owned                  # own positions bypass regime gate
                or (                             # untracked positions also pass through
                    sym in portfolio.positions
                    and sym not in self.position_owners
                )
                or (                             # cross-exit strategies see ALL held
                    name in self.cross_exit_strategies
                    and sym in portfolio.positions
                )
            }
        else:
            filtered_states = symbol_states

        if not filtered_states:
            return []

        if self._multi_symbol[name]:
            return strategy.decide(current_date, filtered_states, portfolio)
        else:
            decisions = []
            for state in filtered_states.values():
                d = strategy.decide(state, portfolio)
                if d is not None:
                    decisions.append(d)
            return decisions

    def _merge_into(
        self,
        merged: dict,
        d: Decision,
        w: float,
        name: str,
    ) -> None:
        """Apply conflict resolution rules and update `merged` in place.

        Diagnostic side-effect: when a decision is overridden by another
        strategy (priority loss or weight loss on a tied action), the losing
        strategy gets `dropped_priority` incremented. The won_merge counter
        is incremented in decide() for whichever strategy survives, so this
        only handles the loser bookkeeping here.
        """
        sym   = d.symbol
        p_new = _ACTION_PRIORITY.get(d.action, 0)

        if sym not in merged:
            merged[sym] = (d, w, name)
            return

        existing_d, existing_w, existing_name = merged[sym]
        p_old = _ACTION_PRIORITY.get(existing_d.action, 0)

        # Log competing convictions when two strategies disagree on action
        if d.action != existing_d.action:
            for ctr_name, own_action, rival, rival_action in [
                (name, d.action, existing_name, existing_d.action),
                (existing_name, existing_d.action, name, d.action),
            ]:
                self.diag_counters[ctr_name]["conflict_count"] += 1
                log = self.diag_counters[ctr_name]["conflict_log"]
                if len(log) < 50:
                    log.append((sym, own_action, rival, rival_action))

        # Higher-priority action always wins (SELL > BUY > HOLD)
        # Ties broken by strategy weight (higher weight = more capital = more say)
        if p_new > p_old or (p_new == p_old and w > existing_w):
            # New wins → the existing (now displaced) one loses on priority.
            self.diag_counters[existing_name]["dropped_priority"] += 1
            merged[sym] = (d, w, name)
        else:
            # New loses to existing.
            self.diag_counters[name]["dropped_priority"] += 1

    @staticmethod
    def _normalise(weights: dict) -> dict:
        """Clip negatives and normalise to sum=1.0. Falls back to equal if all zero."""
        clipped = {k: max(0.0, v) for k, v in weights.items()}
        total   = sum(clipped.values())
        if total <= 0:
            n = max(len(clipped), 1)
            return {k: 1.0 / n for k in clipped}
        return {k: v / total for k, v in clipped.items()}
