from datetime import datetime

from app.strategy.models import Decision


class BreakoutMomentumStrategy:
    """
    Short-term price-breakout strategy.

    Entry:  Close breaks above the 10-day rolling high — fresh momentum.
    Exit:   Close falls back below SMA_10 — momentum stalling.

    Horizon: 3–10 days.
    """

    def decide(
        self,
        current_date:  datetime,
        symbol_states: dict,
        portfolio,
    ) -> list[Decision]:

        decisions = []

        for symbol, state in symbol_states.items():

            price    = state.latest_price
            high_10d = state.indicators.get("high_10d")
            sma_10   = state.indicators.get("sma_10")

            if high_10d is None or sma_10 is None:
                continue

            in_position = symbol in portfolio.positions

            # --- Exit: momentum weakening ---
            if in_position and price < sma_10:
                decisions.append(Decision(
                    symbol=symbol,
                    action="SELL",
                    reasoning=(
                        f"Momentum weakening "
                        f"(price={price:.2f} < SMA_10={sma_10:.2f})"
                    ),
                ))
                continue

            # --- Entry: 10-day breakout ---
            if not in_position and price > high_10d:
                decisions.append(Decision(
                    symbol=symbol,
                    action="BUY",
                    reasoning=(
                        f"10-day breakout detected "
                        f"(price={price:.2f} > high_10d={high_10d:.2f})"
                    ),
                ))

        return decisions
