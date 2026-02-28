import numpy as np
import pandas as pd


class PerformanceMonitor:

    def __init__(
        self,
        min_observations: int = 60,
        sharpe_smoothing_window: int = 10,
        dd_elevated: float = -0.15,
        dd_critical: float = -0.30
    ):
        self.min_observations = min_observations
        self.sharpe_smoothing_window = sharpe_smoothing_window
        self.dd_elevated = dd_elevated
        self.dd_critical = dd_critical

    # ======================================================
    # MAIN ANALYSIS
    # ======================================================
    def analyze(self, rolling_equity: list) -> dict:

        if len(rolling_equity) < self.min_observations:
            return {
                "performance_state": "INSUFFICIENT",
                "sharpe": 0.0,
                "drawdown": 0.0,
                "trend": {},
                "volatility": 0.0
            }

        equity = np.array(rolling_equity)

        # -----------------------------------
        # Returns
        # -----------------------------------
        returns = np.diff(equity) / equity[:-1]

        if len(returns) < 5:
            return {
                "performance_state": "INSUFFICIENT",
                "sharpe": 0.0,
                "drawdown": 0.0,
                "trend": {},
                "volatility": 0.0
            }

        # -----------------------------------
        # Smoothed Sharpe
        # -----------------------------------
        returns_series = pd.Series(returns)
        smoothed_returns = returns_series.rolling(
            self.sharpe_smoothing_window
        ).mean().dropna()

        sharpe = (
            smoothed_returns.mean() /
            (smoothed_returns.std() + 1e-9)
        ) * np.sqrt(252)

        sharpe = float(np.clip(sharpe, -3, 3))  # clamp extremes

        # -----------------------------------
        # Drawdown
        # -----------------------------------
        peak = np.maximum.accumulate(equity)
        drawdowns = (equity - peak) / peak
        max_drawdown = float(np.min(drawdowns))

        # -----------------------------------
        # Volatility
        # -----------------------------------
        volatility = float(np.std(returns) * np.sqrt(252))

        # -----------------------------------
        # Trend Slopes
        # -----------------------------------
        slope_10 = self._slope(equity[-10:])
        slope_30 = self._slope(equity[-30:])
        slope_60 = self._slope(equity[-60:])

        # -----------------------------------
        # Classification (Stable Version)
        # -----------------------------------
        performance_state = self._classify(
            sharpe,
            max_drawdown
        )

        return {
            "performance_state": performance_state,
            "sharpe": round(sharpe, 3),
            "drawdown": round(max_drawdown, 3),
            "volatility": round(volatility, 3),
            "trend": {
                "slope_10": round(slope_10, 6),
                "slope_30": round(slope_30, 6),
                "slope_60": round(slope_60, 6)
            }
        }

    # ======================================================
    # Helpers
    # ======================================================
    def _slope(self, values):
        if len(values) < 2:
            return 0.0
        x = np.arange(len(values))
        slope, _ = np.polyfit(x, values, 1)
        return float(slope)

    def _classify(self, sharpe, drawdown):

        # Critical risk dominates
        if drawdown <= self.dd_critical:
            return "BROKEN"

        # Weak performance
        if sharpe < -0.2:
            return "BROKEN"

        if sharpe < 0.5:
            return "WEAK"

        if sharpe < 1.0:
            return "MODERATE"

        return "STRONG"