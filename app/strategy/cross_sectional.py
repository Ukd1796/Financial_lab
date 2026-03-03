from app.strategy.models import Decision


class CrossSectionalMomentumStrategy:

    def __init__(
        self,
        lookback_days: int = 100,
        top_n: int = 3,
        rebalance_frequency: int = 20,
        momentum_threshold: float = 0.05,
    ):
        self.lookback_days        = lookback_days
        self.top_n                = top_n
        self.rebalance_frequency  = rebalance_frequency
        self.momentum_threshold   = momentum_threshold

        self.price_history        = {}
        self.last_rebalance_date  = None

    def decide(self, current_date, symbol_states: dict, portfolio):

        # Always update price history
        for symbol, state in symbol_states.items():
            self.price_history.setdefault(symbol, []).append(state.latest_price)

        # Rebalance gate
        if self.last_rebalance_date is None:
            self.last_rebalance_date = current_date

        if (current_date - self.last_rebalance_date).days < self.rebalance_frequency:
            return []

        self.last_rebalance_date = current_date

        # Compute momentum scores
        momentum_scores = []
        for symbol, state in symbol_states.items():
            history = self.price_history[symbol]
            if len(history) < self.lookback_days:
                continue
            momentum = (state.latest_price / history[-self.lookback_days]) - 1
            if momentum > self.momentum_threshold:
                momentum_scores.append((symbol, momentum))

        if not momentum_scores:
            return []

        selected = [s for s, _ in sorted(momentum_scores, key=lambda x: x[1], reverse=True)[:self.top_n]]

        decisions = []

        # Exit positions no longer in top-N
        for held in list(portfolio.positions):
            if held not in selected:
                decisions.append(Decision(
                    symbol=held,
                    action="SELL",
                    quantity=portfolio.positions[held].quantity,
                    reasoning="Dropped from top momentum ranking",
                ))

        # Enter new top-N positions
        for symbol in selected:
            if symbol not in portfolio.positions:
                decisions.append(Decision(
                    symbol=symbol,
                    action="BUY",
                    quantity=None,
                    reasoning="Selected by momentum ranking",
                ))

        return decisions
