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
    ):
        self.strategies      = strategies
        self.weights         = self._normalise(
            weights or {k: 1.0 for k in strategies}
        )
        # Per-strategy regime allowlists — None means no regime filtering
        self.allowed_regimes = allowed_regimes or {}

        # Detect dispatch mode once — avoids repeated introspection per bar
        self._multi_symbol: dict[str, bool] = {
            name: (len(inspect.signature(s.decide).parameters) == 3)
            for name, s in strategies.items()
        }

        # Tracks which strategy entered each open position.
        # Only the owning strategy (or the ATR stop in RiskAgent) may close it.
        # Prevents cross-strategy premature exits, e.g. RSI-MR SFelling DualMA holds.
        self.position_owners: dict[str, str] = {}

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

                # Ownership gate: ignore SELL from a strategy that did not open
                # this position (the owning strategy or "untracked" positions pass).
                if d.action == "SELL":
                    owner = self.position_owners.get(d.symbol)
                    if owner is not None and owner != name:
                        continue  # cross-strategy exit — skip

                self._merge_into(merged, d, w, name)

        # Stamp weight + source onto the winning decision for each symbol;
        # update ownership tracking.
        result = []
        for sym, (d, w, name) in merged.items():
            d.weight = w
            d.source = name
            if d.action == "BUY":
                self.position_owners[sym] = name
            elif d.action == "SELL":
                self.position_owners.pop(sym, None)
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
        regimes = self.allowed_regimes.get(name)
        # Symbols this strategy owns (should always receive exit signals)
        owned = {
            sym for sym, owner in self.position_owners.items() if owner == name
        }
        if regimes is not None:
            filtered_states = {
                sym: state for sym, state in symbol_states.items()
                if state.indicators.get("regime") in regimes
                or sym in owned                  # own positions bypass regime gate
                or (                             # untracked positions also pass through
                    sym in portfolio.positions
                    and sym not in self.position_owners
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
        """Apply conflict resolution rules and update `merged` in place."""
        sym   = d.symbol
        p_new = _ACTION_PRIORITY.get(d.action, 0)

        if sym not in merged:
            merged[sym] = (d, w, name)
            return

        existing_d, existing_w, _existing_name = merged[sym]
        p_old = _ACTION_PRIORITY.get(existing_d.action, 0)

        # Higher-priority action always wins (SELL > BUY > HOLD)
        # Ties broken by strategy weight (higher weight = more capital = more say)
        if p_new > p_old or (p_new == p_old and w > existing_w):
            merged[sym] = (d, w, name)

    @staticmethod
    def _normalise(weights: dict) -> dict:
        """Clip negatives and normalise to sum=1.0. Falls back to equal if all zero."""
        clipped = {k: max(0.0, v) for k, v in weights.items()}
        total   = sum(clipped.values())
        if total <= 0:
            n = max(len(clipped), 1)
            return {k: 1.0 / n for k in clipped}
        return {k: v / total for k, v in clipped.items()}
