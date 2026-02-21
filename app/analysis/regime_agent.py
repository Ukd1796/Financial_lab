import numpy as np
import pandas as pd
from collections import Counter
from dataclasses import dataclass


class RegimeAnalysisAgent:

    # =========================================================
    # PART 1 — DAILY REGIME CLASSIFICATION
    # =========================================================
    def classify_regimes(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Requires columns:
        - close
        - sma_50
        - sma_20
        - atr_14
        """

        df = df.copy()

        # ---- Trend Classification ----
        df["sma_50_slope"] = df["sma_50"].diff()

        conditions = [
            (df["close"] > df["sma_50"]) & (df["sma_50_slope"] > 0),
            (df["close"] < df["sma_50"]) & (df["sma_50_slope"] < 0),
        ]

        choices = ["UPTREND", "DOWNTREND"]

        df["trend_state"] = np.select(
            conditions,
            choices,
            default="SIDEWAYS"
        )

        # ---- Volatility Classification via ATR Percentile ----
        df["atr_percentile"] = (
            df["atr_14"]
            .rolling(252, min_periods=50)
            .apply(lambda x: pd.Series(x).rank(pct=True).iloc[-1])
        )

        df["vol_state"] = pd.cut(
            df["atr_percentile"],
            bins=[0, 0.33, 0.66, 1.0],
            labels=["LOW_VOL", "MID_VOL", "HIGH_VOL"]
        )

        # ---- Composite Regime ----
        df["regime"] = df["vol_state"].astype(str) + "_" + df["trend_state"]

        return df

    # =========================================================
    # PART 2 — TRADE REGIME TAGGING
    # =========================================================
    def tag_trades_with_regime(self, trades, regime_df):

        regime_map = regime_df["regime"].to_dict()

        for trade in trades:

            entry_regime = regime_map.get(trade.entry_date)
            exit_regime = regime_map.get(trade.exit_date)

            trade.regime_at_entry = entry_regime
            trade.regime_at_exit = exit_regime

            # Dominant regime during holding period
            holding_slice = regime_df.loc[
                trade.entry_date:trade.exit_date
            ]["regime"]

            if not holding_slice.empty:
                trade.dominant_regime_during_trade = Counter(
                    holding_slice
                ).most_common(1)[0][0]
            else:
                trade.dominant_regime_during_trade = None

        return trades

    # =========================================================
    # PART 3 — PERFORMANCE ATTRIBUTION
    # =========================================================
    def regime_performance(self, trades, regime_df):

        regime_groups = {}

        for trade in trades:
            regime = getattr(trade, "dominant_regime_during_trade", None)
            if regime is None:
                continue

            regime_groups.setdefault(regime, []).append(trade)

        results = {}

        for regime, regime_trades in regime_groups.items():

            pnls = [t.pnl for t in regime_trades]

            total_pnl = sum(pnls)
            trade_count = len(pnls)
            win_rate = len([p for p in pnls if p > 0]) / trade_count
            avg_pnl = np.mean(pnls)

            results[regime] = {
                "total_pnl": total_pnl,
                "trade_count": trade_count,
                "win_rate": win_rate,
                "avg_pnl": avg_pnl,
            }

        return results

    # =========================================================
    # PART 4 — REGIME DEPENDENCY METRICS
    # =========================================================
    def regime_dependency_metrics(self, regime_perf_dict):

        if not regime_perf_dict:
            return {}

        sharpe_by_regime = {}
        pnl_by_regime = {}

        for regime, stats in regime_perf_dict.items():
            pnl_by_regime[regime] = stats["total_pnl"]

            # crude Sharpe proxy from trade returns
            pnls = stats.get("avg_pnl", 0)
            sharpe_by_regime[regime] = pnls  # placeholder

        sharpe_values = list(sharpe_by_regime.values())

        sharpe_dispersion = max(sharpe_values) - min(sharpe_values)

        total_profit = sum(
            v for v in pnl_by_regime.values() if v > 0
        )

        best_regime = max(pnl_by_regime, key=pnl_by_regime.get)
        worst_regime = min(pnl_by_regime, key=pnl_by_regime.get)

        dependency_score = (
            pnl_by_regime[best_regime] / total_profit
            if total_profit != 0 else 0
        )

        return {
            "sharpe_by_regime": sharpe_by_regime,
            "pnl_by_regime": pnl_by_regime,
            "sharpe_dispersion": sharpe_dispersion,
            "dependency_score": dependency_score,
            "most_profitable_regime": best_regime,
            "most_fragile_regime": worst_regime
        }

    # =========================================================
    # PART 5 — STABILITY DIAGNOSTICS
    # =========================================================
    def stability_diagnostics(self, equity_curve: pd.Series):

        daily_returns = equity_curve.pct_change().dropna()

        rolling_sharpe = (
            daily_returns
            .rolling(252)
            .mean() /
            daily_returns
            .rolling(252)
            .std()
        ) * np.sqrt(252)

        rolling_sharpe_std = rolling_sharpe.std()

        instability_flag = rolling_sharpe_std > 1.0

        return {
            "rolling_sharpe_std": rolling_sharpe_std,
            "instability_flag": instability_flag
        }
