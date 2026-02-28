from datetime import datetime
from typing import List

from app.backtest.models import BacktestResult
from app.backtest.trade_models import Trade
from app.strategy.cross_sectional import CrossSectionalMomentumStrategy
from app.risk.agent import MODE_POLICIES



class BacktestEngine:

    def __init__(
        self,
        observer,
        strategy_router,
        risk_agent,
        execution_agent,
        portfolio,
        repository=None,
        meta_reflection=None,
        meta_frequency=20,
        meta_lookback=50
    ):
        self.observer = observer
        self.strategy_router = strategy_router
        self.risk_agent = risk_agent
        self.execution_agent = execution_agent
        self.portfolio = portfolio
        self.repository = repository
        self.meta_reflection = meta_reflection
        self.meta_frequency = meta_frequency
        self.meta_lookback = meta_lookback
        self.meta_mode_history = []

        self.current_mode = None
        self.last_mode_change_index = None
        self.min_mode_duration = 30  # Minimum days before switching mode

    # ==================================================
    # MAIN RUN
    # ==================================================
    def run(self, symbols: List[str], historical_dates: List[datetime]):

        results = []
        completed_trades = []
        trade_count = 0

        if not historical_dates:
            return [], []

        start_date = historical_dates[0]
        end_date = historical_dates[-1]

        # ------------------------------------------
        # 1️⃣ PRELOAD DATA
        # ------------------------------------------
        for symbol in symbols:
            self.observer.preload(symbol, start_date, end_date)

        open_positions_meta = {}

        # ==================================================
        # 2️⃣ DAILY LOOP
        # ==================================================
        for day_index, current_date in enumerate(historical_dates):

            daily_symbol_states = {}
            current_prices = {}

            # ------------------------------------------
            # Gather market states
            # ------------------------------------------
            for symbol in symbols:
                state = self.observer.run_for_day(symbol, current_date)
                if state:
                    daily_symbol_states[symbol] = state
                    current_prices[symbol] = state.latest_price

            if not daily_symbol_states:
                continue

            # ------------------------------------------
            # STRATEGY LAYER
            # ------------------------------------------
            if isinstance(self.strategy_router, CrossSectionalMomentumStrategy):

                proposed_decisions = self.strategy_router.decide(
                    current_date,
                    daily_symbol_states,
                    self.portfolio
                )

            else:
                proposed_decisions = []
                for symbol, state in daily_symbol_states.items():
                    decision = self.strategy_router.decide(
                        current_date,
                        state,
                        self.portfolio
                    )
                    proposed_decisions.append(decision)

            # ------------------------------------------
            # PROCESS DECISIONS
            # ------------------------------------------
            for decision in proposed_decisions:

                if decision is None:
                    continue

                symbol = decision.symbol
                market_state = daily_symbol_states.get(symbol)

                if not market_state:
                    continue

                risk_adjusted = self.risk_agent.evaluate(
                    decision,
                    self.portfolio,
                    market_state
                )

                execution_result = self.execution_agent.execute(
                    risk_adjusted,
                    market_state,
                    self.portfolio
                )

                if execution_result.executed:
                    trade_count += 1

                    if execution_result.action == "BUY":
                        open_positions_meta[symbol] = {
                            "entry_date": current_date,
                            "entry_price": execution_result.price,
                            "quantity": execution_result.quantity
                        }

                    elif execution_result.action == "SELL":
                        if symbol in open_positions_meta:
                            entry_data = open_positions_meta[symbol]

                            completed_trades.append(
                                Trade(
                                    symbol=symbol,
                                    entry_price=entry_data["entry_price"],
                                    exit_price=execution_result.price,
                                    quantity=entry_data["quantity"],
                                    pnl=execution_result.trade_pnl,
                                    entry_date=entry_data["entry_date"],
                                    exit_date=current_date
                                )
                            )

                            del open_positions_meta[symbol]

                    if self.repository:
                        self.repository.log_decision(
                            timestamp=market_state.timestamp,
                            symbol=symbol,
                            decision=risk_adjusted,
                            execution_result=execution_result
                        )

            # ------------------------------------------
            # EQUITY SNAPSHOT
            # ------------------------------------------
            equity = self.portfolio.total_equity(current_prices)

            results.append(
                BacktestResult(
                    date=current_date,
                    equity=equity,
                    cash=self.portfolio.cash,
                    realized_pnl=self.portfolio.realized_pnl
                )
            )

            # ------------------------------------------
            # 🔥 META LAYER (INSIDE LOOP)
            # ------------------------------------------
            if (
                self.meta_reflection
                and day_index >= self.meta_lookback
                and day_index % self.meta_frequency == 0
            ):

                rolling_equity = [
                    r.equity for r in results[-self.meta_lookback:]
                ]

                if len(rolling_equity) < self.meta_lookback:
                    continue

                regime_metrics = {
                    symbol: state.indicators.get("regime")
                    for symbol, state in daily_symbol_states.items()
                }

                meta_decision = self.meta_reflection.evaluate(
                    rolling_equity=rolling_equity,
                    regime_metrics=regime_metrics
                )

                new_mode = meta_decision.get("mode")

                if not new_mode:
                    new_mode = self.current_mode

                # ------------------------------------------
                # MODE INITIALIZATION
                # ------------------------------------------
                if self.current_mode is None and new_mode:

                    self.current_mode = new_mode
                    self.last_mode_change_index = day_index

                    self.strategy_router.apply_mode(new_mode)
                    self.risk_agent.apply_mode_policy(MODE_POLICIES[new_mode])

                    print(f"[META INIT] {current_date.date()} → {new_mode.value}")

                # ------------------------------------------
                # MODE SWITCH WITH PERSISTENCE
                # ------------------------------------------
                elif new_mode and new_mode != self.current_mode:

                    days_since_switch = day_index - self.last_mode_change_index

                    if days_since_switch >= self.min_mode_duration:

                        self.current_mode = new_mode
                        self.last_mode_change_index = day_index

                        self.strategy_router.apply_mode(new_mode)
                        self.risk_agent.apply_mode_policy(MODE_POLICIES[new_mode])

                        print(f"[META MODE SWITCH] {current_date.date()} → {new_mode.value}")

                    else:
                        print(
                            f"[META HOLD] {current_date.date()} → "
                            f"Attempted {new_mode.value} but only {days_since_switch} days elapsed"
                        )

                self.meta_mode_history.append({
                    "date": current_date,
                    "mode": self.current_mode.value if self.current_mode else None
                })

                print(
                    f"[META STATUS] {current_date.date()} → "
                    f"Active Mode: {self.current_mode.value if self.current_mode else 'None'}"
                )

                print(f"Total Trades Executed: {trade_count}")
                print(f"Completed Trades: {len(completed_trades)}")

        return results, completed_trades