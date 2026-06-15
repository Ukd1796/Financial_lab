import inspect
import os
from collections import deque
from datetime import datetime
from typing import List

from app.backtest.models import BacktestResult, Trade
from app.meta.regime_snapshot import build_regime_snapshot


class BacktestEngine:

    def __init__(
        self,
        observer,
        strategy_router,
        risk_agent,
        execution_agent,
        portfolio,
        repository=None,
        dynamic_universe_agent=None,
        universe_agent=None,
        adaptive_selector=None,
        regime_context_agent=None,
        pnl_tracker=None,
        exposure_gate=None,
    ):
        self.observer                = observer
        self.strategy_router         = strategy_router
        self.risk_agent              = risk_agent
        self.execution_agent         = execution_agent
        self.portfolio               = portfolio
        self.repository              = repository
        self.dynamic_universe_agent  = dynamic_universe_agent
        self.universe_agent          = universe_agent
        # Optional: AdaptiveStrategySelector — calls LLM weekly to update weights.
        # When None, the router's weights stay constant (equal-weight baseline).
        self.adaptive_selector       = adaptive_selector
        self.regime_context_agent    = regime_context_agent
        # Optional: StrategyPnLTracker — fed by record_fill on every SELL and
        # record_daily_equity end-of-day. Consumed by PerformanceFeedbackAgent
        # to surface recent strategy P&L into the AdaptiveSelector LLM prompt.
        # When None, this is a no-op — legacy behavior preserved byte-for-byte.
        self.pnl_tracker             = pnl_tracker
        # Optional: ExposureGate — reduces gross BUY sizing when ALL core
        # strategies (default: Breakout + DualMA) are bleeding 30d. Reads
        # from the pnl_tracker. When None, no scaling applied — legacy
        # behavior preserved. See app/risk/exposure_gate.py + docs/next_explorations.md.
        self.exposure_gate           = exposure_gate

    # ==================================================
    # MAIN RUN
    # ==================================================
    def run(self, symbols: List[str], historical_dates: List[datetime]):

        results          = []
        completed_trades = []
        trade_count      = 0

        if not historical_dates:
            return [], []

        start_date = historical_dates[0]
        end_date   = historical_dates[-1]

        # Determine dispatch path once — avoids repeated inspection in the loop.
        # Multi-symbol strategies: decide(current_date, symbol_states, portfolio)  → 3 params
        # Per-symbol strategies:   decide(market_state, portfolio)                 → 2 params
        _n_params     = len(inspect.signature(self.strategy_router.decide).parameters)
        _multi_symbol = _n_params == 3

        # Observer is preloaded lazily — only when a symbol first appears
        # in the filtered universe, never upfront for the full symbol list.
        _preloaded_syms: set = set()

        # Tracks the last seen price for every symbol ever observed.
        # Used to value held positions that are absent from today's universe
        # so that total_equity is never distorted by missing prices.
        _last_known_prices: dict = {}

        open_positions_meta = {}

        # RCA quality gate — rolling Breakout WR window. When recent Breakout
        # WR is poor, the CB relaxation that RCA applies during TRANSITION_UP
        # (engine ll. ~210) becomes an amplifier that lets more bad Breakout
        # trades through. Disable relaxation when quality < threshold.
        _rca_gate_enabled       = os.environ.get("RCA_QUALITY_GATE", "1") != "0"
        _rca_gate_window        = int(os.environ.get("RCA_QUALITY_WINDOW", "20"))
        _rca_gate_min_samples   = int(os.environ.get("RCA_QUALITY_MIN_SAMPLES", "10"))
        _rca_gate_wr_threshold  = float(os.environ.get("RCA_QUALITY_WR_THRESHOLD", "0.40"))
        _breakout_recent_wins: deque = deque(maxlen=_rca_gate_window)
        _rca_gate_logged = False

        # ==================================================
        # DAILY LOOP
        # ==================================================
        for current_date in historical_dates:
            # One-shot per-day flag for the ExposureGate trigger log line.
            # The gate's current_multiplier() may be called many times in a
            # single day; we only want one log line per day on first trigger.
            _gate_logged_today = False

            # --- Two-stage universe filtering ---
            # Stage 1: DynamicUniverseAgent scores all symbols → top 80 UniverseCandidates
            #          (activity-biased; used by Breakout filters)
            #          + all candidates without gate (for strategy-native filters)
            # Stage 2: UnionUniverseFilter selects symbols
            if self.dynamic_universe_agent and self.universe_agent:
                broad_candidates = self.dynamic_universe_agent.select_candidates(current_date)
                all_candidates = self.dynamic_universe_agent.select_all_candidates(current_date)
                active_symbols = self.universe_agent.select_symbols(
                    broad_candidates, all_candidates=all_candidates
                )
                if not active_symbols:
                    fallback_n = getattr(self.universe_agent, "top_n", len(broad_candidates))
                    active_symbols = [c.symbol for c in broad_candidates[:fallback_n]]
            elif self.dynamic_universe_agent:
                active_symbols = self.dynamic_universe_agent.select_symbols(current_date)
            else:
                active_symbols = symbols

            # P0 fix: always include held positions so exit signals can fire
            # and prices are always available for equity valuation.
            held_symbols   = set(self.portfolio.positions.keys())
            active_symbols = list(set(active_symbols) | held_symbols)

            daily_symbol_states = {}
            current_prices      = {}

            # --- Lazy preload: load observer data on first encounter ---
            for symbol in active_symbols:
                if symbol not in _preloaded_syms:
                    try:
                        self.observer.preload(symbol, start_date, end_date)
                    except Exception:
                        pass  # symbol has no data for this period — skip silently
                    _preloaded_syms.add(symbol)

            # --- Gather market states ---
            for symbol in active_symbols:
                state = self.observer.run_for_day(symbol, current_date)
                if state:
                    daily_symbol_states[symbol] = state
                    current_prices[symbol]       = state.latest_price
                    _last_known_prices[symbol]   = state.latest_price

            if not daily_symbol_states:
                continue

            # --- P0 fix: build a complete price map for equity valuation ---
            # Merge today's prices with last-known prices for any held position
            # that has no data today (trading halt, de-listing, etc.) so that
            # total_equity never prices a live position at $0.
            equity_prices = dict(_last_known_prices)
            equity_prices.update(current_prices)

            # --- Strategy layer ---
            if _multi_symbol:
                proposed_decisions = self.strategy_router.decide(
                    current_date,
                    daily_symbol_states,
                    self.portfolio,
                )
            else:
                proposed_decisions = []
                for symbol, state in daily_symbol_states.items():
                    decision = self.strategy_router.decide(
                        state,
                        self.portfolio,
                    )
                    proposed_decisions.append(decision)

            # --- Market breadth: fraction of active universe in DOWNTREND ---
            # Used by the breadth circuit breaker in RiskAgent.
            downtrend_count = sum(
                1 for s in daily_symbol_states.values()
                if isinstance(s.indicators.get("regime"), str)
                and "DOWNTREND" in s.indicators["regime"]
            )
            market_downtrend_pct = (
                downtrend_count / len(daily_symbol_states) if daily_symbol_states else 0.0
            )

            # Current account equity — fed into the regime snapshot so the
            # AdaptiveStrategySelector can concentrate allocation at low capital
            # (a ₹10k account cannot diversify across 5 strategies). Uses the
            # same total_equity() call the equity-snapshot below uses.
            current_equity = self.portfolio.total_equity(equity_prices)

            # --- Regime snapshot: enhanced (RCA) or base ---
            # RCA is built whenever present — not only when adaptive_selector is active,
            # because its broad_regime drives the CB relaxation below.
            regime_snapshot = None
            if self.regime_context_agent:
                regime_snapshot = self.regime_context_agent.build_snapshot(
                    daily_symbol_states, current_date, capital=current_equity
                )

            # --- Adaptive weight rebalance (weekly, LLM-driven) ---
            if self.adaptive_selector and hasattr(self.strategy_router, "update_weights"):
                if regime_snapshot is None:
                    regime_snapshot = build_regime_snapshot(
                        daily_symbol_states, current_date, capital=current_equity
                    )
                new_weights = self.adaptive_selector.rebalance(current_date, regime_snapshot)
                self.strategy_router.update_weights(new_weights)

            # --- CB relaxation during transition/recovery phases ---
            # During TRANSITION_UP the market is recovering but pct_downtrend is still
            # elevated (e.g. 50%). Without relaxation the CB (threshold=35%) would block
            # ALL buys even as breadth genuinely improves. Cap effective downtrend to
            # allow cautious re-entry before SMA_50-based rules catch the move.
            effective_downtrend_pct = market_downtrend_pct
            if regime_snapshot:
                broad_regime = regime_snapshot.get("broad_regime")
                # RCA quality gate: skip relaxation when rolling Breakout WR is
                # below threshold. Prevents the amplifier-effect in periods where
                # Breakout's signal quality is structurally broken (Live, Bull, Bear).
                rca_quality_ok = True
                if _rca_gate_enabled and len(_breakout_recent_wins) >= _rca_gate_min_samples:
                    recent_wr = sum(_breakout_recent_wins) / len(_breakout_recent_wins)
                    if recent_wr < _rca_gate_wr_threshold:
                        rca_quality_ok = False
                        if not _rca_gate_logged:
                            print(
                                f"  [RCAQualityGate] {current_date.date()} → Breakout WR "
                                f"{recent_wr:.1%} < {_rca_gate_wr_threshold:.0%} over last "
                                f"{len(_breakout_recent_wins)} trades — CB relaxation disabled"
                            )
                            _rca_gate_logged = True
                if rca_quality_ok:
                    if broad_regime == "TRANSITION_UP":
                        effective_downtrend_pct = min(market_downtrend_pct, 0.30)
                    elif broad_regime == "BEAR_EARLY":
                        effective_downtrend_pct = min(market_downtrend_pct, 0.38)

            # --- Risk + execution ---
            # Process higher-weight strategy signals first so they claim cash
            # before lower-weight strategies when capital is constrained.
            proposed_decisions = sorted(
                (d for d in proposed_decisions if d is not None),
                key=lambda d: getattr(d, "weight", 1.0),
                reverse=True,
            )
            # --- Exposure gate (optional) ----------------------------------
            # When enabled and ALL core strategies are bleeding 30d, scale
            # down NEW BUY sizing so capital sits as cash instead of being
            # deployed into a broken signal regime. SELLs/HOLDs untouched
            # (don't force-exit existing positions; let them turn over
            # naturally). See app/risk/exposure_gate.py.
            gate_multiplier = 1.0
            if self.exposure_gate is not None:
                gate_multiplier = self.exposure_gate.current_multiplier(current_date)
                # One-shot daily log on first trigger so the run output is
                # readable instead of spamming a line per BUY.
                if (
                    gate_multiplier < 1.0
                    and self.exposure_gate.triggered_today()
                    and not _gate_logged_today
                ):
                    contribs = self.exposure_gate.last_trigger_contribs()
                    contrib_str = "  ".join(
                        f"{k}={v*100:+.1f}%" if v is not None else f"{k}=n/a"
                        for k, v in contribs.items()
                    )
                    print(
                        f"  [ExposureGate] {current_date.date()} → ALL core bleeding "
                        f"({contrib_str}) → exposure scaled to {gate_multiplier:.0%}"
                    )
                    _gate_logged_today = True

            for decision in proposed_decisions:

                symbol       = decision.symbol
                market_state = daily_symbol_states.get(symbol)

                if not market_state:
                    continue

                # Apply gate multiplier to BUY decisions only. Modifying the
                # decision's weight in-place is safe because the decision is
                # built fresh by the router each day (not reused across days).
                # SELLs and HOLDs are not touched — we don't force-exit existing
                # positions; gate effect builds gradually as positions roll over.
                if gate_multiplier < 1.0 and decision.action == "BUY":
                    decision.weight = decision.weight * gate_multiplier

                risk_adjusted    = self.risk_agent.evaluate(
                    decision,
                    self.portfolio,
                    market_state,
                    equity_prices=equity_prices,
                    market_downtrend_pct=effective_downtrend_pct,
                )
                execution_result = self.execution_agent.execute(risk_adjusted, market_state, self.portfolio)

                # Diagnostic: count post-router BUY rejections per strategy.
                # If the router's BUY decision didn't execute (RiskAgent
                # converted to HOLD due to cash starvation / breadth CB /
                # ATR-to-cost / regime gate), bump buy_rejected for the
                # originating strategy. Pairs with the router's signal-drop
                # counters to give a full picture of where signals die.
                # See docs/next_explorations.md §5.
                if decision.action == "BUY" and (
                    not execution_result.executed
                    or execution_result.action != "BUY"
                ):
                    src = getattr(decision, "source", "") or ""
                    if hasattr(self.strategy_router, "diag_counters") and src in self.strategy_router.diag_counters:
                        # Lazily ensure the buy_rejected key exists; the router
                        # only creates the 4 baseline counters.
                        self.strategy_router.diag_counters[src].setdefault("buy_rejected", 0)
                        self.strategy_router.diag_counters[src]["buy_rejected"] += 1

                if execution_result.executed:
                    trade_count += 1

                    if execution_result.action == "BUY":
                        # Capture the OPENING strategy from the router's pre-risk
                        # decision (decision.source). risk_adjusted.source may be
                        # empty here because RiskAgent often constructs a fresh
                        # sized Decision that doesn't propagate the .source field.
                        # We then re-read this on SELL for correct P&L attribution
                        # — works for both strategy-driven exits AND ATR-stop exits.
                        open_positions_meta[symbol] = {
                            "entry_date":  current_date,
                            "entry_price": execution_result.price,
                            "quantity":    execution_result.quantity,
                            "strategy":    getattr(decision, "source", "") or "",
                        }

                    elif execution_result.action == "SELL":
                        # Capture the owning strategy BEFORE we clear open_positions_meta,
                        # so the PAA tracker hook below can attribute P&L correctly
                        # even when the SELL was generated by an ATR stop (in which
                        # case risk_adjusted.source is empty because RiskAgent built
                        # a fresh Decision object — see app/risk/agent.py:174).
                        owning_strategy = ""
                        if symbol in open_positions_meta:
                            entry = open_positions_meta[symbol]
                            owning_strategy = entry.get("strategy", "") or ""
                            # "atr_stop" when the strategy proposed HOLD/BUY but
                            # RiskAgent converted it to SELL via the trailing stop.
                            exit_reason = (
                                "atr_stop" if decision.action != "SELL" else "strategy"
                            )
                            completed_trades.append(
                                Trade(
                                    symbol=symbol,
                                    entry_price=entry["entry_price"],
                                    exit_price=execution_result.price,
                                    quantity=entry["quantity"],
                                    pnl=execution_result.trade_pnl,
                                    entry_date=entry["entry_date"],
                                    exit_date=current_date,
                                    exit_reason=exit_reason,
                                    strategy=owning_strategy,
                                )
                            )
                            if owning_strategy == "Breakout":
                                _breakout_recent_wins.append(
                                    1 if execution_result.trade_pnl > 0 else 0
                                )
                            del open_positions_meta[symbol]
                        # Per-strategy P&L attribution (PAA Phase 1).
                        # Owner-at-BUY-time is the right attribution target (not
                        # the strategy that *signaled* the SELL, which for ATR
                        # stops is just whoever happened to issue a same-symbol
                        # decision that week).
                        if self.pnl_tracker is not None:
                            self.pnl_tracker.record_fill(
                                date=current_date,
                                strategy_name=owning_strategy,
                                action="SELL",
                                pnl=execution_result.trade_pnl,
                            )

                    if self.repository:
                        self.repository.log_decision(
                            timestamp=market_state.timestamp,
                            symbol=symbol,
                            decision=risk_adjusted,
                            execution_result=execution_result,
                        )

            # --- Equity snapshot (uses full price map, never prices positions at $0) ---
            eod_equity = self.portfolio.total_equity(equity_prices)
            results.append(
                BacktestResult(
                    date=current_date,
                    equity=eod_equity,
                    cash=self.portfolio.cash,
                    realized_pnl=self.portfolio.realized_pnl,
                )
            )
            # PAA Phase 1: feed daily equity to the tracker for rolling
            # contribution-pct normalisation. No-op when tracker is absent.
            if self.pnl_tracker is not None:
                self.pnl_tracker.record_daily_equity(current_date, eod_equity)

        return results, completed_trades
