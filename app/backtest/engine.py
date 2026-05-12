import inspect
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

        # ==================================================
        # DAILY LOOP
        # ==================================================
        for current_date in historical_dates:

            # --- Two-stage universe filtering ---
            # Stage 1: DynamicUniverseAgent scores all symbols → top 80 UniverseCandidates
            # Stage 2: UniverseSelectionAgent applies hard thresholds → top 20 symbols
            if self.dynamic_universe_agent and self.universe_agent:
                broad_candidates = self.dynamic_universe_agent.select_candidates(current_date)
                active_symbols   = self.universe_agent.select_symbols(broad_candidates)
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

            # --- Regime snapshot: enhanced (RCA) or base ---
            # RCA is built whenever present — not only when adaptive_selector is active,
            # because its broad_regime drives the CB relaxation below.
            regime_snapshot = None
            if self.regime_context_agent:
                regime_snapshot = self.regime_context_agent.build_snapshot(
                    daily_symbol_states, current_date
                )

            # --- Adaptive weight rebalance (weekly, LLM-driven) ---
            if self.adaptive_selector and hasattr(self.strategy_router, "update_weights"):
                if regime_snapshot is None:
                    regime_snapshot = build_regime_snapshot(daily_symbol_states, current_date)
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
            for decision in proposed_decisions:

                symbol       = decision.symbol
                market_state = daily_symbol_states.get(symbol)

                if not market_state:
                    continue

                risk_adjusted    = self.risk_agent.evaluate(
                    decision,
                    self.portfolio,
                    market_state,
                    equity_prices=equity_prices,
                    market_downtrend_pct=effective_downtrend_pct,
                )
                execution_result = self.execution_agent.execute(risk_adjusted, market_state, self.portfolio)

                if execution_result.executed:
                    trade_count += 1

                    if execution_result.action == "BUY":
                        open_positions_meta[symbol] = {
                            "entry_date":  current_date,
                            "entry_price": execution_result.price,
                            "quantity":    execution_result.quantity,
                        }

                    elif execution_result.action == "SELL":
                        if symbol in open_positions_meta:
                            entry = open_positions_meta[symbol]
                            completed_trades.append(
                                Trade(
                                    symbol=symbol,
                                    entry_price=entry["entry_price"],
                                    exit_price=execution_result.price,
                                    quantity=entry["quantity"],
                                    pnl=execution_result.trade_pnl,
                                    entry_date=entry["entry_date"],
                                    exit_date=current_date,
                                )
                            )
                            del open_positions_meta[symbol]

                    if self.repository:
                        self.repository.log_decision(
                            timestamp=market_state.timestamp,
                            symbol=symbol,
                            decision=risk_adjusted,
                            execution_result=execution_result,
                        )

            # --- Equity snapshot (uses full price map, never prices positions at $0) ---
            results.append(
                BacktestResult(
                    date=current_date,
                    equity=self.portfolio.total_equity(equity_prices),
                    cash=self.portfolio.cash,
                    realized_pnl=self.portfolio.realized_pnl,
                )
            )

        return results, completed_trades
