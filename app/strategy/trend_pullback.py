from datetime import datetime

from app.strategy.models import Decision


class TrendPullbackStrategy:
    """
    Buy short-term pullbacks inside a confirmed medium-term uptrend.

    Trend filter:   SMA_20 > SMA_50  (medium-term uptrend intact)
    Entry:          return_3d < -pullback_threshold  (recent price weakness)
    Exit:           latest_price > SMA_5  (short-term recovery confirmed)

    Horizon: 2–7 days.
    """

    def __init__(
        self,
        pullback_threshold: float = 0.03,
    ):
        self.pullback_threshold = pullback_threshold

    def decide(
        self,
        current_date:  datetime,
        symbol_states: dict,
        portfolio,
    ) -> list[Decision]:

        decisions = []

        for symbol, state in symbol_states.items():

            price     = state.latest_price
            sma_5     = state.indicators.get("sma_5")
            sma_20    = state.indicators.get("sma_20")
            sma_50    = state.indicators.get("sma_50")
            return_3d = state.indicators.get("return_3d")

            if None in (sma_5, sma_20, sma_50, return_3d):
                continue

            in_position = symbol in portfolio.positions

            # --- Exit: short-term recovery confirmed ---
            if in_position and price > sma_5:
                decisions.append(Decision(
                    symbol=symbol,
                    action="SELL",
                    reasoning=(
                        f"Price recovered above SMA_5 "
                        f"(price={price:.2f} > SMA_5={sma_5:.2f})"
                    ),
                ))
                continue

            # --- Entry: uptrend + pullback ---
            if (
                not in_position
                and sma_20 > sma_50
                and return_3d < -self.pullback_threshold
            ):
                decisions.append(Decision(
                    symbol=symbol,
                    action="BUY",
                    reasoning=(
                        f"Pullback in uptrend detected "
                        f"(return_3d={return_3d * 100:.1f}%, "
                        f"SMA_20={sma_20:.2f} > SMA_50={sma_50:.2f})"
                    ),
                ))

        return decisions
