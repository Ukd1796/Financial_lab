# app/universe/filters.py
#
# Per-strategy second-stage universe filters.
#
# All five filter classes share the same interface as UniverseSelectionAgent:
#   select_universe(candidates) → list[UniverseCandidate]
#   select_symbols(candidates)  → list[str]
#
# They receive the top-80 UniverseCandidate list from DynamicUniverseAgent
# (already carrying trend signals) and apply strategy-specific criteria.
# No DB access — all signal data comes from the candidate objects.
#
# Why separate filters per strategy?
# ------------------------------------
# The shared DynamicUniverseAgent scores by "activity" (vol spike + abs return
# + realised vol). This optimises for Breakout (loud, high-volume moves) but
# actively excludes TrendPullback's ideal candidates (quiet pullbacks on
# declining volume), RSI-MR's candidates (oversold stocks that may not be
# moving loudly today), and DualMA's candidates (stocks near a golden cross
# that often show normal, not spiking, activity). Each filter re-ranks the
# same 80 candidates using criteria that match its strategy's entry signal.
#
# UnionUniverseFilter (at the bottom of this file) aggregates multiple
# per-strategy filters for multi-strategy experiments.

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

    use_full_universe = False: Breakout intentionally uses the top-80
    activity-biased candidates — the activity bias aligns with breakout
    morphology and the top-80 gate acts as a natural liquidity screen.
    """

    use_full_universe = False

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

    def select_symbols(
        self,
        candidates: list[UniverseCandidate],
        all_candidates: list[UniverseCandidate] | None = None,
    ) -> list[str]:
        src = all_candidates if (self.use_full_universe and all_candidates is not None) else candidates
        return [c.symbol for c in self.select_universe(src)]


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

    use_full_universe = True: quiet pullbacks (low relative volume) rank low
    on the activity-based top-80 score and are often excluded before this
    filter runs. Scanning all 150 candidates surfaces the correct morphology.
    """

    use_full_universe = False

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
            if c.sma_20_above_sma_50                # uptrend intact
            and c.sma_20_slope_positive             # trend still rising
            and c.return_3d < -self.min_pullback    # meaningful pullback
            and c.return_3d > -self.max_pullback    # not a crash
            and c.relative_volume < self.max_vol    # volume drying up
        ]
        # Sort by deepest pullback first — most mean-reversion potential
        filtered.sort(key=lambda c: c.return_3d)
        return filtered[: self.top_n]

    def select_symbols(
        self,
        candidates: list[UniverseCandidate],
        all_candidates: list[UniverseCandidate] | None = None,
    ) -> list[str]:
        src = all_candidates if (getattr(self, "use_full_universe", False) and all_candidates is not None) else candidates
        return [c.symbol for c in self.select_universe(src)]


class MeanReversionUniverseFilter:
    """
    Selects stocks that are oversold within an uptrend — the "oversold bounce"
    candidates for RSI-MR strategy.

    Hard filters:
      - sma_20_above_sma_50  : stock is in a medium-term uptrend.
                               "Oversold in a downtrend" = falling knife.
                               "Oversold in an uptrend"  = bounce candidate.
      - sma_cross_age >= 10  : SMA_20 has been above SMA_50 for 10+ consecutive days.
                               A stock that crossed into uptrend in the last 9 days
                               has an unreliable signal — the crossover may be a
                               temporary bounce inside a broader downtrend.
                               (R2 improvement)
      - return_3d < -min_3d_drop
                             : stock has fallen meaningfully over 3 days, which
                               correlates with RSI_3 < 10 (extreme oversold).
                               Using return_3d as a proxy avoids re-computing RSI
                               at this layer (RSI is computed in MarketObserver).

    Scoring: ranked by 3-day return ascending (most oversold first).
    RSI_3 is computed per-symbol in MarketObserver; the filter just narrows the
    pool to stocks where extreme overselling is plausible.

    use_full_universe = True: oversold stocks often have low volume and small
    daily moves (distributional selling not yet explosive), so they rank low
    on the activity-based top-80 and are excluded before this filter runs.
    Scanning all 150 candidates ensures oversold bounces are not missed.
    """

    use_full_universe = False

    def __init__(
        self,
        min_3d_drop:   float = 0.03,  # stock must be down at least 3% over 3 days
        max_3d_drop:   float = 0.15,  # ignore extreme crashes (> 15% = potential halt)
        min_cross_age: int   = 10,    # SMA_20 must have been > SMA_50 for this many days (R2)
        top_n:         int   = 20,
    ):
        self.min_3d_drop   = min_3d_drop
        self.max_3d_drop   = max_3d_drop
        self.min_cross_age = min_cross_age
        self.top_n         = top_n

    def select_universe(
        self, candidates: list[UniverseCandidate]
    ) -> list[UniverseCandidate]:
        filtered = [
            c for c in candidates
            if c.sma_20_above_sma_50                         # uptrend only
            and c.sma_cross_age >= self.min_cross_age        # confirmed trend, not fresh crossover (R2)
            and c.return_3d < -self.min_3d_drop              # oversold
            and c.return_3d > -self.max_3d_drop              # not a crash
        ]
        # Most oversold first
        filtered.sort(key=lambda c: c.return_3d)
        return filtered[: self.top_n]

    def select_symbols(
        self,
        candidates: list[UniverseCandidate],
        all_candidates: list[UniverseCandidate] | None = None,
    ) -> list[str]:
        src = all_candidates if (getattr(self, "use_full_universe", False) and all_candidates is not None) else candidates
        return [c.symbol for c in self.select_universe(src)]


class DualMAUniverseFilter:
    """
    Selects stocks near or at a golden cross (SMA_20 crossing above SMA_50)
    for DualMovingAverageStrategy.

    The strategy fires a BUY on the exact day of the crossover and a SELL when
    SMA_20 crosses back below SMA_50.  The engine always includes held positions
    regardless of this filter (P0 fix in BacktestEngine), so exit signals fire
    correctly even when a stock falls out of this filter.
    This filter's job is purely to surface fresh entry candidates each day.

    Hard filters:
      - sma_20_above_sma_50        : currently in uptrend (cross has happened)
      - 1 <= sma_cross_age <= max_cross_age
                                   : cross happened recently — the strategy's BUY
                                     fires on sma_cross_age == 1 (the exact day
                                     SMA20 first exceeds SMA50). Allowing a small
                                     window (default 5 days) handles cases where the
                                     stock was out of the top-80 on the exact cross day.
      - relative_volume >= min_vol : basic liquidity gate — crossovers on zero-volume
                                     days are data artefacts, not real signals.

    Scoring: ranked by sma_cross_age ascending so the freshest crosses appear first.

    use_full_universe = True: golden crosses on normal volume score poorly on the
    activity-based top-80 ranking (no vol spike, moderate daily return). Scanning
    all 150 ensures no crossover events are missed due to the activity gate.
    """

    use_full_universe = False

    def __init__(
        self,
        max_cross_age: int   = 5,    # include crosses up to 5 days old
        min_vol:       float = 0.8,  # lower bar than Breakout — no spike required
        top_n:         int   = 30,   # wider pool — crossovers are rare events
    ):
        self.max_cross_age = max_cross_age
        self.min_vol       = min_vol
        self.top_n         = top_n

    def select_universe(
        self, candidates: list[UniverseCandidate]
    ) -> list[UniverseCandidate]:
        filtered = [
            c for c in candidates
            if c.sma_20_above_sma_50                            # in uptrend
            and 1 <= c.sma_cross_age <= self.max_cross_age      # fresh cross
            and c.relative_volume >= self.min_vol               # basic liquidity
        ]
        # Freshest crosses first — strategy's entry signal is strongest on day 1
        filtered.sort(key=lambda c: c.sma_cross_age)
        return filtered[: self.top_n]

    def select_symbols(
        self,
        candidates: list[UniverseCandidate],
        all_candidates: list[UniverseCandidate] | None = None,
    ) -> list[str]:
        src = all_candidates if (getattr(self, "use_full_universe", False) and all_candidates is not None) else candidates
        return [c.symbol for c in self.select_universe(src)]


class AffordabilityFilter:
    """
    Capital-aware wrapper that drops candidates too expensive to buy at least
    one share within the per-position budget.

    Why a wrapper (not another child of UnionUniverseFilter)?
    --------------------------------------------------------
    Affordability is a *global* capital gate, not a strategy-domain signal.
    Wrapping the composed UnionUniverseFilter keeps each child filter's
    domain logic intact and simply removes names a small account can never
    take a position in (e.g. MRF ≈ ₹1.4L on a ₹10k account). At ₹1L+ the cap
    is high enough that nothing is dropped, so this is a no-op on large
    accounts.

    Parameters
    ----------
    inner : object exposing select_universe(candidates) -> list[UniverseCandidate]
        Typically a UnionUniverseFilter (but any filter works).
    max_price : float
        Drop candidates whose price exceeds this. Derived from capital as
        capital * max_position_pct so a single share fits the undiluted
        absolute single-name ceiling enforced by RiskAgent.

    A candidate with price <= 0 is treated as "price unknown" and kept — the
    RiskAgent cash gate is still the authoritative backstop on spend.
    """

    def __init__(self, inner, max_price: float):
        self.inner     = inner
        self.max_price = max_price
        # Preserve the composed top_n so callers that introspect it still work.
        self.top_n     = getattr(inner, "top_n", 20)

    def select_universe(
        self, candidates: list[UniverseCandidate]
    ) -> list[UniverseCandidate]:
        selected = self.inner.select_universe(candidates)
        return [
            c for c in selected
            if c.price <= 0 or c.price <= self.max_price
        ]

    def select_symbols(
        self,
        candidates: list[UniverseCandidate],
        all_candidates: list[UniverseCandidate] | None = None,
    ) -> list[str]:
        src = all_candidates if (getattr(self, "use_full_universe", False) and all_candidates is not None) else candidates
        return [c.symbol for c in self.select_universe(src)]


class UnionUniverseFilter:
    """
    Aggregates the outputs of multiple per-strategy filters into a single
    de-duplicated symbol list for multi-strategy experiments.

    Why this fixes the equal-weight baseline:
    -----------------------------------------
    When 5 strategies share a single activity-based top-20 universe, each
    strategy sees only ~4 stocks per day (20 / 5 strategies).  At 20% weight,
    that is ~4% of normal capital working — the portfolio is mostly cash and
    transaction costs erode returns.

    UnionUniverseFilter runs every child filter on the same top-80 DynamicAgent
    candidates and takes the de-duplicated union.  TrendPB gets its quiet
    pullback stocks, RSI-MR gets its oversold stocks, DualMA gets fresh golden
    crosses, Breakout gets high-activity stocks — each from the correct domain,
    without competing for the same 20 slots.

    Ordering: candidates from earlier filters appear first so the BacktestEngine
    processes higher-priority entries first on conflict.
    """

    def __init__(self, filters: list):
        self.filters = filters
        self.top_n   = sum(getattr(f, "top_n", 20) for f in filters)

    def select_universe(
        self,
        candidates: list[UniverseCandidate],
        all_candidates: list[UniverseCandidate] | None = None,
    ) -> list[UniverseCandidate]:
        """
        Run each child filter with the appropriate candidate pool.

        Filters with `use_full_universe = True` receive `all_candidates`
        (all 150 scored symbols, no activity gate) so that morphologies
        excluded by the top-80 activity bias — quiet pullbacks, oversold
        stocks, normal-volume golden crosses — are visible to their filters.

        Filters with `use_full_universe = False` (default, e.g. Breakout)
        continue to receive the activity-biased top-80 `candidates`.

        When `all_candidates` is None (backward-compat path), all filters
        receive `candidates` regardless of `use_full_universe`.
        """
        full_pool = all_candidates if all_candidates is not None else candidates
        seen:   set  = set()
        result: list = []
        for f in self.filters:
            src = full_pool if getattr(f, "use_full_universe", False) else candidates
            for candidate in f.select_universe(src):
                if candidate.symbol not in seen:
                    seen.add(candidate.symbol)
                    result.append(candidate)
        return result

    def select_symbols(
        self,
        candidates: list[UniverseCandidate],
        all_candidates: list[UniverseCandidate] | None = None,
    ) -> list[str]:
        return [c.symbol for c in self.select_universe(candidates, all_candidates)]
