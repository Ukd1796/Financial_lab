# app/strategy/cross_sectional.py

from app.strategy.models import Decision
from datetime import timedelta


class CrossSectionalMomentumStrategy:

    def __init__(
        self,
        lookback_days: int = 100,
        top_n: int = 3,
        rebalance_frequency: int = 20,
        momentum_threshold: float = 0.05
    ):
        self.lookback_days = lookback_days
        self.top_n = top_n
        self.rebalance_frequency = rebalance_frequency
        self.momentum_threshold = momentum_threshold
        self.day_counter = 0
        self.price_history = {}

    def decide(self, current_date, symbol_states: dict, portfolio):

        # ----------------------------
        # 1️⃣ Always update price history
        # ----------------------------
        for symbol, state in symbol_states.items():

            price = state.latest_price

            if symbol not in self.price_history:
                self.price_history[symbol] = []

            self.price_history[symbol].append(price)

        # ----------------------------
        # 2️⃣ Rebalance logic
        # ----------------------------
        if not hasattr(self, "last_rebalance_date"):
            self.last_rebalance_date = current_date

        days_since = (current_date - self.last_rebalance_date).days

        if days_since < self.rebalance_frequency:
            return []

        self.last_rebalance_date = current_date

        # ----------------------------
        # 3️⃣ Compute momentum
        # ----------------------------
        momentum_scores = []

        for symbol, state in symbol_states.items():

            if len(self.price_history[symbol]) < self.lookback_days:
                continue

            price = state.latest_price
            price_lookback = self.price_history[symbol][-self.lookback_days]

            momentum = (price / price_lookback) - 1

            if momentum > self.momentum_threshold:
                momentum_scores.append((symbol, momentum))

        if not momentum_scores:
            return []

        ranked = sorted(momentum_scores, key=lambda x: x[1], reverse=True)
        selected_symbols = [s[0] for s in ranked[:self.top_n]]

        decisions = []

        for held_symbol in list(portfolio.positions.keys()):
            if held_symbol not in selected_symbols:
                decisions.append(
                    Decision(
                        symbol=held_symbol,
                        action="SELL",
                        quantity=portfolio.positions[held_symbol].quantity,
                        reasoning="Dropped from top momentum ranking"
                    )
                )

        for symbol in selected_symbols:
            if symbol not in portfolio.positions:
                decisions.append(
                    Decision(
                        symbol=symbol,
                        action="BUY",
                        quantity=None,
                        reasoning="Selected by 50-day momentum ranking"
                    )
                )

        return decisions