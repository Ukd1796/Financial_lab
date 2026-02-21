from app.strategy.base import BaseStrategyAgent
from app.strategy.models import Decision


class DualMovingAverageStrategy(BaseStrategyAgent):

    def decide(self, market_state, portfolio):

        fast_today = market_state.indicators.get("sma_20")
        slow_today = market_state.indicators.get("sma_50")

        fast_yesterday = market_state.previous_indicators.get("sma_20")
        slow_yesterday = market_state.previous_indicators.get("sma_50")

        symbol = market_state.symbol

        if None in [fast_today, slow_today, fast_yesterday, slow_yesterday]:
            return Decision(symbol=symbol, action="HOLD")

        # ----------------------------
        # Bullish crossover
        # ----------------------------
        if (
            fast_yesterday <= slow_yesterday and
            fast_today > slow_today and
            symbol not in portfolio.positions
        ):
            return Decision(
                symbol=symbol,
                action="BUY",
                quantity=None,
                reasoning="Bullish dual MA crossover"
            )

        # ----------------------------
        # Bearish crossover
        # ----------------------------
        if (
            fast_yesterday >= slow_yesterday and
            fast_today < slow_today and
            symbol in portfolio.positions
        ):
            return Decision(
                symbol=symbol,
                action="SELL",
                quantity=None,
                reasoning="Bearish dual MA crossover"
            )

        return Decision(symbol=symbol, action="HOLD")
