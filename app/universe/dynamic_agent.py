# app/universe/dynamic_agent.py

from datetime import datetime, timedelta

import pandas as pd

from app.data.repository import MarketDataRepository
from app.universe.models import UniverseCandidate


class DynamicUniverseAgent:
    """
    Broad first-pass scanner across the full stock universe (~150 symbols).

    Computes an opportunity_score for every symbol each trading day using:
      - relative_volume   : today volume / 20d avg volume  (liquidity spike)
      - abs_daily_return  : magnitude of today's price move
      - rolling_vol_5d    : 5-day realised volatility (recent activity level)

    All three metrics are cross-sectionally rank-normalised (0→1) before
    weighting so that no single metric dominates regardless of scale.

    No hard filters are applied — every symbol with sufficient history
    receives a score.  The agent returns the top_n symbols by score as
    the candidate universe for UnionUniverseFilter.

    Workflow
        1. Call preload(start_date, end_date) once before the backtest loop.
        2. Call select_symbols(current_date) each day to get the broad list.
    """

    def __init__(
        self,
        repository:     MarketDataRepository,
        symbols:        list[str],
        top_n:          int = 80,
        vol_avg_window: int = 20,
    ):
        self.repository     = repository
        self.symbols        = symbols
        self.top_n          = top_n
        self.vol_avg_window = vol_avg_window

        # symbol → DataFrame indexed by timestamp with precomputed signals
        self._cache: dict[str, pd.DataFrame] = {}

    # ------------------------------------------------------------------
    # PRELOAD
    # ------------------------------------------------------------------
    def preload(self, start_date: datetime, end_date: datetime) -> None:
        """
        Fetch OHLCV history for all symbols in a single bulk DB query,
        then precompute signals for each symbol in memory.

        A 90-day buffer is prepended so that rolling windows are warm from
        the first date in the requested range.

        Symbols with no data or insufficient history for the period are
        logged and skipped — they are not treated as hard failures.
        """
        buffer_start = start_date - timedelta(days=200)

        print(f"[DynamicUniverseAgent] Bulk fetching {len(self.symbols)} symbols "
              f"from {buffer_start.date()} to {end_date.date()} ...")

        all_records = self.repository.get_ohlc_bulk(self.symbols, buffer_start, end_date)

        skipped = []
        for symbol in self.symbols:
            records = all_records.get(symbol, [])

            if not records:
                skipped.append(f"{symbol}(no data)")
                continue

            if len(records) < self.vol_avg_window + 5:
                skipped.append(f"{symbol}(only {len(records)} rows)")
                continue

            df = pd.DataFrame(
                {
                    "close":  [r.close  for r in records],
                    "high":   [r.high   for r in records],
                    "low":    [r.low    for r in records],
                    "volume": [r.volume for r in records],
                },
                index=[r.timestamp for r in records],
            )

            self._cache[symbol] = self._compute_signals(df)

        print(f"[DynamicUniverseAgent] Loaded {len(self._cache)} symbols. "
              f"Skipped {len(skipped)}: {', '.join(skipped) if skipped else 'none'}")

    def _compute_signals(self, df: pd.DataFrame) -> pd.DataFrame:
        """Compute all per-symbol signals, fully look-ahead free (shift(1))."""

        # ---- Liquidity ----
        df["vol_avg"] = (
            df["volume"]
            .shift(1)
            .rolling(self.vol_avg_window, min_periods=self.vol_avg_window)
            .mean()
        )
        df["relative_volume"] = df["volume"] / df["vol_avg"]

        # ---- Price movement ----
        df["daily_return"] = df["close"].pct_change(1)
        df["return_3d"]    = df["close"].pct_change(3)

        # ---- Short-term realised volatility ----
        df["rolling_vol_5d"] = (
            df["daily_return"].rolling(5, min_periods=5).std()
        )

        # ---- Trend state — used by per-strategy universe filters ----
        # shift(1) so that today's SMA is computed from completed bars only;
        # no look-ahead into today's close.
        df["sma_20"] = df["close"].rolling(20, min_periods=20).mean()
        df["sma_50"] = df["close"].rolling(50, min_periods=50).mean()
        df["sma_20_above_sma_50"]   = df["sma_20"] > df["sma_50"]
        # slope > 0 means the SMA_20 is still rising — trend accelerating, not topping
        df["sma_20_slope_positive"] = df["sma_20"].diff() > 0

        # Consecutive days SMA_20 has been above SMA_50 (resets on cross-under).
        # Used by PullbackUniverseFilter (R3, threshold=15) and
        # MeanReversionUniverseFilter (R2, threshold=10) to reject stocks whose
        # uptrend is too fresh — these are often false crossovers that will fail.
        cross_age = []
        count = 0
        for above in df["sma_20_above_sma_50"]:
            count = count + 1 if above else 0
            cross_age.append(count)
        df["sma_cross_age"] = cross_age

        # ---- Normalised ATR (stored for reference, not used in scoring) ----
        prev_close = df["close"].shift(1)
        true_range = pd.concat(
            [
                df["high"] - df["low"],
                (df["high"] - prev_close).abs(),
                (df["low"]  - prev_close).abs(),
            ],
            axis=1,
        ).max(axis=1)
        df["atr_14"]    = true_range.rolling(14, min_periods=14).mean()
        df["atr_ratio"] = df["atr_14"] / df["close"]

        return df

    # ------------------------------------------------------------------
    # SELECT
    # ------------------------------------------------------------------
    def _build_scored_df(self, current_date: datetime):
        """
        Collect valid rows for current_date and compute cross-sectional
        opportunity scores. Returns (rows_list, scores_DataFrame) where
        scores is None when fewer than 2 symbols have data.
        """
        rows = []

        for symbol, df in self._cache.items():
            loc_key = df.index.asof(current_date)
            if pd.isnull(loc_key):
                continue

            row = df.loc[loc_key]
            rel_vol   = row["relative_volume"]
            daily_ret = row["daily_return"]
            vol_5d    = row["rolling_vol_5d"]
            atr_ratio = row["atr_ratio"]

            if pd.isna(rel_vol) or pd.isna(daily_ret) or pd.isna(vol_5d):
                continue

            return_3d          = row.get("return_3d", float("nan"))
            sma_20_above_sma50 = row.get("sma_20_above_sma_50", False)
            sma_20_slope_pos   = row.get("sma_20_slope_positive", False)
            sma_cross_age      = row.get("sma_cross_age", 0)
            close_px           = row.get("close", float("nan"))

            rows.append(
                {
                    "symbol":                symbol,
                    "relative_volume":       float(rel_vol),
                    "daily_return":          float(daily_ret),
                    "abs_daily_return":      abs(float(daily_ret)),
                    "rolling_vol_5d":        float(vol_5d),
                    "atr_ratio":             float(atr_ratio) if not pd.isna(atr_ratio) else 0.0,
                    "return_3d":             float(return_3d) if not pd.isna(return_3d) else 0.0,
                    "sma_20_above_sma_50":   bool(sma_20_above_sma50),
                    "sma_20_slope_positive": bool(sma_20_slope_pos),
                    "sma_cross_age":         int(sma_cross_age) if not pd.isna(sma_cross_age) else 0,
                    "price":                 float(close_px) if not pd.isna(close_px) else 0.0,
                }
            )

        if len(rows) < 2:
            return rows, None

        scores = pd.DataFrame(rows).set_index("symbol")
        for col in ["relative_volume", "abs_daily_return", "rolling_vol_5d"]:
            scores[f"{col}_rank"] = scores[col].rank(pct=True)
        scores["opportunity_score"] = (
            0.40 * scores["relative_volume_rank"]
            + 0.30 * scores["abs_daily_return_rank"]
            + 0.30 * scores["rolling_vol_5d_rank"]
        )
        return rows, scores

    def _candidates_from_scores(self, scores, index) -> list[UniverseCandidate]:
        """Build UniverseCandidate objects for the given symbol index."""
        return [
            UniverseCandidate(
                symbol=symbol,
                score=float(scores.loc[symbol, "opportunity_score"]),
                relative_volume=float(scores.loc[symbol, "relative_volume"]),
                daily_return=float(scores.loc[symbol, "daily_return"]),
                atr_ratio=float(scores.loc[symbol, "atr_ratio"]),
                sma_20_above_sma_50=bool(scores.loc[symbol, "sma_20_above_sma_50"]),
                sma_20_slope_positive=bool(scores.loc[symbol, "sma_20_slope_positive"]),
                return_3d=float(scores.loc[symbol, "return_3d"]),
                rolling_vol_5d=float(scores.loc[symbol, "rolling_vol_5d"]),
                sma_cross_age=int(scores.loc[symbol, "sma_cross_age"]),
                price=float(scores.loc[symbol, "price"]),
            )
            for symbol in index
        ]

    def select_candidates(self, current_date: datetime) -> list[UniverseCandidate]:
        """
        Return the top-N UniverseCandidate objects by cross-sectional
        opportunity score.

        Score = 0.40 × rank(relative_volume)
              + 0.30 × rank(|daily_return|)
              + 0.30 × rank(rolling_vol_5d)

        Ranks are computed across all symbols that have valid data for
        current_date (0–1 percentile). Returns an empty list when fewer
        than 2 symbols have data.

        These candidates — carrying all precomputed metrics — are passed
        directly to UnionUniverseFilter for threshold filtering.
        """
        rows, scores = self._build_scored_df(current_date)
        if scores is None:
            return [
                UniverseCandidate(
                    symbol=r["symbol"], score=0.0,
                    relative_volume=r["relative_volume"],
                    daily_return=r["daily_return"],
                    atr_ratio=r["atr_ratio"],
                    sma_20_above_sma_50=r["sma_20_above_sma_50"],
                    sma_20_slope_positive=r["sma_20_slope_positive"],
                    return_3d=r["return_3d"],
                    rolling_vol_5d=r["rolling_vol_5d"],
                    sma_cross_age=r["sma_cross_age"],
                    price=r["price"],
                )
                for r in rows
            ]
        top_index = scores["opportunity_score"].nlargest(self.top_n).index
        return self._candidates_from_scores(scores, top_index)

    def select_all_candidates(self, current_date: datetime) -> list[UniverseCandidate]:
        """
        Return ALL scored candidates without the top-N activity gate.

        Used by strategy-native universe filters (TrendPB, RSI-MR, DualMA)
        that need to scan the full 150-symbol universe. Breakout filters
        should continue using select_candidates() (top-80) since activity
        bias is intentional for breakout morphology.

        Returns candidates sorted by opportunity_score descending.
        """
        rows, scores = self._build_scored_df(current_date)
        if scores is None:
            return [
                UniverseCandidate(
                    symbol=r["symbol"], score=0.0,
                    relative_volume=r["relative_volume"],
                    daily_return=r["daily_return"],
                    atr_ratio=r["atr_ratio"],
                    sma_20_above_sma_50=r["sma_20_above_sma_50"],
                    sma_20_slope_positive=r["sma_20_slope_positive"],
                    return_3d=r["return_3d"],
                    rolling_vol_5d=r["rolling_vol_5d"],
                    sma_cross_age=r["sma_cross_age"],
                    price=r["price"],
                )
                for r in rows
            ]
        all_index = scores["opportunity_score"].sort_values(ascending=False).index
        return self._candidates_from_scores(scores, all_index)

    def select_symbols(self, current_date: datetime) -> list[str]:
        """Convenience wrapper — returns symbol strings from select_candidates()."""
        return [c.symbol for c in self.select_candidates(current_date)]

    def get_price_feed(self) -> dict[str, dict]:
        """
        Extract a {symbol: {date: close_price}} dict from the preloaded cache.
        Covers the full buffered date range (start_date - 200 days → end_date),
        giving CrossSectionalMomentumStrategy enough history to compute
        lookbacks from the very first day of the backtest period.
        """
        return {
            symbol: df["close"].to_dict()
            for symbol, df in self._cache.items()
        }
