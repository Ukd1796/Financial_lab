from datetime import datetime, timedelta
from app.data.repository import MarketDataRepository
from app.features.indicators import (
    simple_moving_average,
    average_true_range
)
from app.data.models import MarketState
import pandas as pd


class MarketObserverAgent:

    def __init__(self, repository: MarketDataRepository):
        self.repository = repository
        self.symbol_cache = {}

    def preload(self, symbol: str, start: datetime, end: datetime):

        buffer_start = start - timedelta(days=300)  
        records = self.repository.get_ohlc(symbol, buffer_start, end)

        if not records:
            raise ValueError(f"No data found for {symbol}")

        closes = [r.close for r in records]
        highs = [r.high for r in records]
        lows = [r.low for r in records]

        sma_20 = simple_moving_average(closes, 20)
        sma_50 = simple_moving_average(closes, 50)
        atr_14 = average_true_range(highs, lows, closes, 14)

        # --- Build DataFrame for regime classification ---
        df = pd.DataFrame({
            "close": closes,
            "sma_50": sma_50,
            "atr_14": atr_14,
        })

        # Trend slope
        df["sma_50_slope"] = df["sma_50"].diff()

        # Trend classification
        df["trend_state"] = "SIDEWAYS"

        df.loc[
            (df["close"] > df["sma_50"]) &
            (df["sma_50_slope"] > 0),
            "trend_state"
        ] = "UPTREND"

        df.loc[
            (df["close"] < df["sma_50"]) &
            (df["sma_50_slope"] < 0),
            "trend_state"
        ] = "DOWNTREND"

        # Volatility percentile using rolling 252-day window
        df["atr_percentile"] = (
            df["atr_14"]
            .rolling(252, min_periods=100)
            .apply(lambda x: pd.Series(x).rank(pct=True).iloc[-1])
        )

        df["vol_state"] = pd.cut(
            df["atr_percentile"],
            bins=[0, 0.33, 0.66, 1.0],
            labels=["LOW_VOL", "MID_VOL", "HIGH_VOL"]
        )

        df["regime"] = df["vol_state"].astype(str) + "_" + df["trend_state"]

        symbol_data = {}

        for i in range(1, len(records)):

            if (
                sma_20[i] is None or
                sma_50[i] is None or
                atr_14[i] is None or
                df["regime"].iloc[i] is None
            ):
                continue

            latest = records[i]
            previous = records[i - 1]

            symbol_data[latest.timestamp] = MarketState(
                symbol=symbol,
                timestamp=latest.timestamp,
                latest_price=latest.close,
                previous_price=previous.close,
                indicators={
                    "sma_20": sma_20[i],
                    "sma_50": sma_50[i],
                    "atr_14": atr_14[i],
                    "regime": df["regime"].iloc[i],  
                },
                previous_indicators={
                    "sma_20": sma_20[i - 1],
                    "sma_50": sma_50[i - 1],
                    "atr_14": atr_14[i - 1],
                }
            )

        self.symbol_cache[symbol] = symbol_data

    def run_for_day(self, symbol: str, date: datetime):
        """
        Return precomputed MarketState for the given day.
        """

        if symbol not in self.symbol_cache:
            return None

        return self.symbol_cache[symbol].get(date)
    
    def export_symbol_dataframe(self, symbol: str):

        if symbol not in self.symbol_cache:
            return None

        records = []

        for date, state in self.symbol_cache[symbol].items():

            row = {
                "date": date,
                "close": state.latest_price,
                "sma_20": state.indicators.get("sma_20"),
                "sma_50": state.indicators.get("sma_50"),
                "atr_14": state.indicators.get("atr_14"),
            }

            records.append(row)


        df = pd.DataFrame(records)
        df = df.sort_values("date")
        df.set_index("date", inplace=True)

        return df

