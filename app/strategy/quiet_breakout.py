from datetime import datetime

from app.strategy.models import Decision


class QuietBreakoutStrategy:
    """
    Low-volatility variant of BreakoutMomentumStrategy.

    Designed for slow-bull markets where stocks drift upward gradually and
    rarely produce the single-day 1.5%+ move that BreakoutMomentumStrategy
    requires.  Meaningful breakouts in this regime occur over 20 days, not 10.

    Entry:  Close breaks above the 20-day rolling high.
            Using a longer lookback makes the signal more selective — a stock
            must clear a wider range of recent prices, filtering out intraday
            noise that would pollute a 10-day signal in low-vol conditions.

    Exit:   Close falls back below SMA_20.
            SMA_20 gives the trade more room than SMA_10, appropriate for a
            strategy that expects a longer hold horizon (1–3 weeks) in a
            trending but subdued market.  The RiskAgent's ATR stop provides
            a secondary hard exit for sharp reversals.

    Universe filter:  BreakoutUniverseFilter with relaxed thresholds:
        - vol_threshold    = 1.2   (vs 1.5 for 10d breakout)
        - return_threshold = 0.008 (0.8% vs 1.5% for 10d breakout)
    These reflect the lower typical activity in slow-bull conditions.

    Horizon: 5–20 days.
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
            high_20d = state.indicators.get("high_20d")
            sma_20   = state.indicators.get("sma_20")

            if high_20d is None or sma_20 is None:
                continue

            in_position = symbol in portfolio.positions

            # --- Exit: momentum fading below SMA_20 ---
            if in_position and price < sma_20:
                decisions.append(Decision(
                    symbol=symbol,
                    action="SELL",
                    reasoning=(
                        f"Quiet breakout momentum fading "
                        f"(price={price:.2f} < SMA_20={sma_20:.2f})"
                    ),
                ))
                continue

            # --- Still holding above SMA_20: emit HOLD so RiskAgent checks ATR stop ---
            if in_position:
                decisions.append(Decision(
                    symbol=symbol,
                    action="HOLD",
                    reasoning=f"Quiet breakout intact (price={price:.2f} >= SMA_20={sma_20:.2f})",
                ))
                continue

            # --- Entry: 20-day breakout ---
            if not in_position and price > high_20d:
                decisions.append(Decision(
                    symbol=symbol,
                    action="BUY",
                    reasoning=(
                        f"20-day quiet breakout detected "
                        f"(price={price:.2f} > high_20d={high_20d:.2f})"
                    ),
                ))

        return decisions
