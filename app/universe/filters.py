# app/universe/filters.py
#
# Per-strategy second-stage universe filters.
#
# All three classes share the same interface as UniverseSelectionAgent:
#   select_universe(candidates) → list[UniverseCandidate]
#   select_symbols(candidates)  → list[str]
#
# They receive the top-80 UniverseCandidate list from DynamicUniverseAgent
# (already carrying trend signals) and apply strategy-specific criteria.
# No DB access — all signal data comes from the candidate objects.
#
# Why three separate filters?
# ----------------------------
# The shared DynamicUniverseAgent scores by "activity" (vol spike + abs return
# + realised vol). This optimises for Breakout (loud, high-volume moves) but
# actively excludes TrendPullback's ideal candidates (quiet pullbacks on
# declining volume) and RSI-MR's candidates (oversold stocks that may not be
# moving loudly today). Each filter re-ranks the same 80 candidates using
# criteria that match its strategy's entry signal.

from app.universe.models import UniverseCandidate


class BreakoutUniverseFilter:
    """
    Selects stocks showing a volume spike + large price move today.

    These are the conditions most likely to precede a 10-day high breakout:
    institutional participation (high relative volume) combined with a price
    move that shows the market is actively repricing the stock.

    This is identical in spirit to the original UniverseSelectionAgent but
    explicitly named so the intent is clear.

    Scoring: cross-sectional activity score (same as DynamicUniverseAgent's
    opportunity_score — already embedded in candidate.score).
    """

    def __init__(
        self,
        vol_threshold:    float = 1.5,   # relative volume must exceed this
        return_threshold: float = 0.015, # abs(daily_return) must exceed this (1.5%)
        top_n:            int   = 20,
    ):
        self.vol_threshold    = vol_threshold
        self.return_threshold = return_threshold
        self.top_n            = top_n

    def select_universe(
        self, candidates: list[UniverseCandidate]
    ) -> list[UniverseCandidate]:
        filtered = [
            c for c in candidates
            if c.relative_volume > self.vol_threshold
            and abs(c.daily_return) > self.return_threshold
        ]
        # Reuse DynamicAgent's opportunity_score — already the right metric here
        filtered.sort(key=lambda c: c.score, reverse=True)
        return filtered[: self.top_n]

    def select_symbols(self, candidates: list[UniverseCandidate]) -> list[str]:
        return [c.symbol for c in self.select_universe(candidates)]


class PullbackUniverseFilter:
    """
    Selects stocks in a confirmed, rising uptrend that are currently pulling
    back quietly — the ideal entry candidates for TrendPullbackStrategy.

    Hard filters:
      - sma_20_above_sma_50   : stock is in a medium-term uptrend
      - sma_20_slope_positive : uptrend is still accelerating (not topping)
      - return_3d in [-max_pullback, -min_pullback]
                              : meaningful pullback, not a crash
      - relative_volume < max_vol
                              : volume declining on the pullback (healthy
                                rotation / profit-taking, not distribution)

    Scoring: ranked by depth of pullback descending (-return_3d), so the
    strongest prior-trend stocks that pulled back the most appear first.
    The strategy's own entry logic (`price_3d_ago > SMA_20 * 1.05`) then
    provides the final gate — the filter just ensures the right pool.
    """

    def __init__(
        self,
        min_pullback: float = 0.015,  # must have pulled back at least 1.5% over 3d
        max_pullback: float = 0.12,   # ignore crashes (> 12% in 3d = breakdown)
        max_vol:      float = 1.4,    # volume should not be spiking on the pullback
        top_n:        int   = 20,
    ):
        self.min_pullback = min_pullback
        self.max_pullback = max_pullback
        self.max_vol      = max_vol
        self.top_n        = top_n

    def select_universe(
        self, candidates: list[UniverseCandidate]
    ) -> list[UniverseCandidate]:
        filtered = [
            c for c in candidates
            if c.sma_20_above_sma_50                          # uptrend intact
            and c.sma_20_slope_positive                       # trend still rising
            and c.return_3d < -self.min_pullback              # meaningful pullback
            and c.return_3d > -self.max_pullback              # not a crash
            and c.relative_volume < self.max_vol              # volume drying up
        ]
        # Sort by deepest pullback first — most mean-reversion potential
        filtered.sort(key=lambda c: c.return_3d)
        return filtered[: self.top_n]

    def select_symbols(self, candidates: list[UniverseCandidate]) -> list[str]:
        return [c.symbol for c in self.select_universe(candidates)]


class MeanReversionUniverseFilter:
    """
    Selects stocks that are oversold within an uptrend — the "oversold bounce"
    candidates for RSI-MR strategy.

    Hard filters:
      - sma_20_above_sma_50  : stock is in a medium-term uptrend.
                               "Oversold in a downtrend" = falling knife.
                               "Oversold in an uptrend"  = bounce candidate.
      - return_3d < -min_3d_drop
                             : stock has fallen meaningfully over 3 days, which
                               correlates with RSI_3 < 10 (extreme oversold).
                               Using return_3d as a proxy avoids re-computing RSI
                               at this layer (RSI is computed in MarketObserver).

    Scoring: ranked by 3-day return ascending (most oversold first).
    RSI_3 is computed per-symbol in MarketObserver; the filter just narrows the
    pool to stocks where extreme overselling is plausible.
    """

    def __init__(
        self,
        min_3d_drop: float = 0.03,  # stock must be down at least 3% over 3 days
        max_3d_drop: float = 0.15,  # ignore extreme crashes (> 15% = potential halt)
        top_n:       int   = 20,
    ):
        self.min_3d_drop = min_3d_drop
        self.max_3d_drop = max_3d_drop
        self.top_n       = top_n

    def select_universe(
        self, candidates: list[UniverseCandidate]
    ) -> list[UniverseCandidate]:
        filtered = [
            c for c in candidates
            if c.sma_20_above_sma_50                         # uptrend only
            and c.return_3d < -self.min_3d_drop              # oversold
            and c.return_3d > -self.max_3d_drop              # not a crash
        ]
        # Most oversold first
        filtered.sort(key=lambda c: c.return_3d)
        return filtered[: self.top_n]

    def select_symbols(self, candidates: list[UniverseCandidate]) -> list[str]:
        return [c.symbol for c in self.select_universe(candidates)]
