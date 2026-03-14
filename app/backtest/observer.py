from datetime import datetime, timedelta
from typing import Optional

import pandas as pd

from app.data.models import MarketState
from app.data.repository import MarketDataRepository
from app.features.indicators import (
    average_true_range,
    relative_strength_index,
    simple_moving_average,
)


def _nan_to_none(series: pd.Series) -> list:
    """Convert a pandas Series to a list, replacing NaN / inf with None."""
    return [None if (v != v or v is None) else float(v) for v in series]


class MarketObserverAgent:

    def __init__(self, repository: MarketDataRepository):
        self.repository   = repository
        self.symbol_cache = {}

    # ------------------------------------------------------------------
    # PRELOAD
    # ------------------------------------------------------------------
    def preload(self, symbol: str, start: datetime, end: datetime):
        """
        Fetch OHLC data for `symbol`, compute all indicators once, and
        cache a MarketState object per trading day.

        A 300-day look-back buffer is prepended to `start` so that
        long-window indicators (SMA_50, ATR_14) are warm by the first
        date in the requested range.
        """
        buffer_start = start - timedelta(days=300)
        records      = self.repository.get_ohlc(symbol, buffer_start, end)

        if not records:
            raise ValueError(f"No data found for {symbol}")

        closes = [r.close for r in records]
        highs  = [r.high  for r in records]
        lows   = [r.low   for r in records]

        # ----------------------------------------------------------
        # List-based indicators (consistent with existing helpers)
        # ----------------------------------------------------------

        # Medium-term trend (existing)
        sma_20 = simple_moving_average(closes, 20)
        sma_50 = simple_moving_average(closes, 50)
        atr_14 = average_true_range(highs, lows, closes, 14)

        # Short-term trend
        sma_5  = simple_moving_average(closes, 5)
        sma_10 = simple_moving_average(closes, 10)

        # Short-term volatility
        atr_5  = average_true_range(highs, lows, closes, 5)

        # Mean-reversion oscillators
        rsi_2  = relative_strength_index(closes, 2)
        rsi_3  = relative_strength_index(closes, 3)

        # ----------------------------------------------------------
        # Vectorized pandas features (multi-bar returns, rolling vol,
        # price-range levels)
        # ----------------------------------------------------------
        closes_s = pd.Series(closes, dtype=float)
        highs_s  = pd.Series(highs,  dtype=float)
        lows_s   = pd.Series(lows,   dtype=float)

        daily_return    = closes_s.pct_change(1)
        return_3d       = closes_s.pct_change(3)
        return_5d       = closes_s.pct_change(5)
        return_10d      = closes_s.pct_change(10)

        rolling_vol_5d  = daily_return.rolling(5,  min_periods=5).std()
        rolling_vol_10d = daily_return.rolling(10, min_periods=10).std()

        # shift(1) excludes today so that close > high_10d is a valid
        # breakout condition (today's close can't exceed today's high).
        high_10d        = highs_s.shift(1).rolling(10, min_periods=10).max()
        low_10d         = lows_s.shift(1).rolling(10,  min_periods=10).min()

        # Convert to None-safe lists for uniform index access in the loop
        daily_return_l    = _nan_to_none(daily_return)
        return_3d_l       = _nan_to_none(return_3d)
        return_5d_l       = _nan_to_none(return_5d)
        return_10d_l      = _nan_to_none(return_10d)
        rolling_vol_5d_l  = _nan_to_none(rolling_vol_5d)
        rolling_vol_10d_l = _nan_to_none(rolling_vol_10d)
        high_10d_l        = _nan_to_none(high_10d)
        low_10d_l         = _nan_to_none(low_10d)

        # ----------------------------------------------------------
        # Regime classification (existing vectorised logic)
        # ----------------------------------------------------------
        df = pd.DataFrame({
            "close":  closes,
            "sma_50": sma_50,
            "atr_14": atr_14,
        })

        df["sma_50_slope"] = df["sma_50"].diff()
        df["trend_state"]  = "SIDEWAYS"

        df.loc[
            (df["close"] > df["sma_50"]) & (df["sma_50_slope"] > 0),
            "trend_state",
        ] = "UPTREND"

        df.loc[
            (df["close"] < df["sma_50"]) & (df["sma_50_slope"] < 0),
            "trend_state",
        ] = "DOWNTREND"

        df["atr_percentile"] = (
            df["atr_14"]
            .rolling(252, min_periods=100)
            .apply(lambda x: pd.Series(x).rank(pct=True).iloc[-1])
        )

        df["vol_state"] = pd.cut(
            df["atr_percentile"],
            bins=[0, 0.33, 0.66, 1.0],
            labels=["LOW_VOL", "MID_VOL", "HIGH_VOL"],
        )

        df["regime"] = df["vol_state"].astype(str) + "_" + df["trend_state"]

        # ----------------------------------------------------------
        # Build MarketState cache — one entry per trading day
        # ----------------------------------------------------------
        symbol_data = {}

        for i in range(1, len(records)):

            # Require base medium-term indicators before emitting a state.
            # Short-term indicators may still be None for the earliest bars
            # but are stored as-is; strategy agents must guard for None.
            if sma_20[i] is None or sma_50[i] is None or atr_14[i] is None:
                continue

            latest   = records[i]
            previous = records[i - 1]

            symbol_data[latest.timestamp] = MarketState(
                symbol=symbol,
                timestamp=latest.timestamp,
                latest_price=latest.close,
                previous_price=previous.close,
                indicators={
                    # ---- Medium-term trend (existing) ----
                    "sma_20":  sma_20[i],
                    "sma_50":  sma_50[i],
                    "atr_14":  atr_14[i],
                    "regime":  df["regime"].iloc[i],
                    # ---- Short-term trend ----
                    "sma_5":   sma_5[i],
                    "sma_10":  sma_10[i],
                    # ---- Momentum (multi-day returns) ----
                    "daily_return":  daily_return_l[i],
                    "return_3d":     return_3d_l[i],
                    "return_5d":     return_5d_l[i],
                    "return_10d":    return_10d_l[i],
                    # ---- Mean-reversion oscillators ----
                    "rsi_2":  rsi_2[i],
                    "rsi_3":  rsi_3[i],
                    # ---- Short-term volatility ----
                    "atr_5":           atr_5[i],
                    "rolling_vol_5d":  rolling_vol_5d_l[i],
                    "rolling_vol_10d": rolling_vol_10d_l[i],
                    # ---- Price-range levels ----
                    "high_10d": high_10d_l[i],
                    "low_10d":  low_10d_l[i],
                },
                previous_indicators={
                    # ---- Medium-term trend (existing) ----
                    "sma_20": sma_20[i - 1],
                    "sma_50": sma_50[i - 1],
                    "atr_14": atr_14[i - 1],
                    # ---- Short-term trend ----
                    "sma_5":  sma_5[i - 1],
                    "sma_10": sma_10[i - 1],
                    # ---- Mean-reversion oscillators ----
                    "rsi_2":  rsi_2[i - 1],
                    "rsi_3":  rsi_3[i - 1],
                },
            )

        self.symbol_cache[symbol] = symbol_data

    # ------------------------------------------------------------------
    # QUERY
    # ------------------------------------------------------------------
    def run_for_day(self, symbol: str, date: datetime) -> Optional[MarketState]:
        """Return the precomputed MarketState for the given symbol and date."""
        if symbol not in self.symbol_cache:
            return None
        return self.symbol_cache[symbol].get(date)

    # ------------------------------------------------------------------
    # EXPORT (for analysis / visualisation)
    # ------------------------------------------------------------------
    def export_symbol_dataframe(self, symbol: str) -> Optional[pd.DataFrame]:

        if symbol not in self.symbol_cache:
            return None

        rows = []
        for date, state in self.symbol_cache[symbol].items():
            row = {"date": date, "close": state.latest_price}
            row.update(state.indicators)
            rows.append(row)

        df = pd.DataFrame(rows).sort_values("date").set_index("date")
        return df
