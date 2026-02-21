from app.strategy.base import BaseStrategyAgent
from app.strategy.models import Decision


class MovingAverageStrategy(BaseStrategyAgent):

    def decide(self, market_state, portfolio):

        price_today = market_state.latest_price
        price_yesterday = market_state.previous_price

        sma_today = market_state.indicators.get("sma_20")
        sma_yesterday = market_state.previous_indicators.get("sma_20")

        # Safety check
        if None in [price_yesterday, sma_yesterday, sma_today]:
            return Decision(
                symbol=market_state.symbol,
                action="HOLD",
                reasoning="Insufficient history"
            )

        # ----------------------------
        # Bullish crossover
        # ----------------------------
        if (
            price_yesterday <= sma_yesterday
            and price_today > sma_today
            and market_state.symbol not in portfolio.positions
        ):
            return Decision(
                symbol=market_state.symbol,
                action="BUY",
                quantity=None,
                confidence=0.7,
                reasoning="Bullish crossover detected"
            )

        # ----------------------------
        # Bearish crossover
        # ----------------------------
        if (
            price_yesterday >= sma_yesterday
            and price_today < sma_today
            and market_state.symbol in portfolio.positions
        ):
            return Decision(
                symbol=market_state.symbol,
                action="SELL",
                quantity=None,  # Risk agent decides full exit
                confidence=0.7,
                reasoning="Bearish crossover detected"
            )

        # ----------------------------
        # Default: HOLD
        # ----------------------------
        return Decision(
            symbol=market_state.symbol,
            action="HOLD",
            reasoning="No crossover"
        )

