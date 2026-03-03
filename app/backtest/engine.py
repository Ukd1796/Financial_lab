from datetime import datetime
from typing import List

from app.backtest.models import BacktestResult , Trade
from app.strategy.cross_sectional import CrossSectionalMomentumStrategy


class BacktestEngine:

    def __init__(
        self,
        observer,
        strategy_router,
        risk_agent,
        execution_agent,
        portfolio,
        repository=None,
    ):
        self.observer         = observer
        self.strategy_router  = strategy_router
        self.risk_agent       = risk_agent
        self.execution_agent  = execution_agent
        self.portfolio        = portfolio
        self.repository       = repository

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

        # ------------------------------------------
        # PRELOAD DATA
        # ------------------------------------------
        for symbol in symbols:
            self.observer.preload(symbol, start_date, end_date)

        open_positions_meta = {}

        # ==================================================
        # DAILY LOOP
        # ==================================================
        for current_date in historical_dates:

            daily_symbol_states = {}
            current_prices      = {}

            # --- Gather market states ---
            for symbol in symbols:
                state = self.observer.run_for_day(symbol, current_date)
                if state:
                    daily_symbol_states[symbol] = state
                    current_prices[symbol]       = state.latest_price

            if not daily_symbol_states:
                continue

            # --- Strategy layer ---
            if isinstance(self.strategy_router, CrossSectionalMomentumStrategy):
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

            # --- Risk + execution ---
            for decision in proposed_decisions:

                if decision is None:
                    continue

                symbol       = decision.symbol
                market_state = daily_symbol_states.get(symbol)

                if not market_state:
                    continue

                risk_adjusted    = self.risk_agent.evaluate(decision, self.portfolio, market_state)
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

            # --- Equity snapshot ---
            results.append(
                BacktestResult(
                    date=current_date,
                    equity=self.portfolio.total_equity(current_prices),
                    cash=self.portfolio.cash,
                    realized_pnl=self.portfolio.realized_pnl,
                )
            )

        return results, completed_trades
