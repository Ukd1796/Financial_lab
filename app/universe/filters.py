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


class QuietBreakoutUniverseFilter:
    """
    Selects slow-grinding, low-activity stocks for QuietBreakoutStrategy.

    QuietBreakoutStrategy's 20-day-high entry signal is structurally similar
    to BreakoutMomentumStrategy's 10-day-high entry — every QuietBrk BUY
    candidate is also a Breakout BUY candidate on the same bar. When both
    filters draw from the same activity-biased top-80 pool, the router's
    weight tiebreak and ownership rule mean Breakout wins every entry and
    QuietBrk contributes 0 won_merge across all periods (verified across
    backtest history).

    This filter solves the collision at the *universe* layer by giving
    QuietBrk a structurally orthogonal slice: stocks in the middle band of
    activity (calm but not dead) that Breakout's own entry gate (vol_ratio
    > 1.2, |daily_return| effectively > 1.5%) will reject. QuietBrk's
    20-day signal then has an uncontested cohort to find genuine breakouts
    in — the slow drifters that produce 20-day highs without the daily
    fireworks Breakout requires.

    Hard filters (per-day cross-sectional percentiles on the pool):
      - atr_ratio        in [25th, 60th] pct of pool — moderate range
      - rolling_vol_5d   in [25th, 60th] pct of pool — moderate choppiness
      - |daily_return|   < 0.015                     — no big move today
      - relative_volume  in [0.7, 1.5]               — normal-ish volume

    Fallback for warm-up / sparse pools (< 4 non-zero atr_ratio values):
      use fixed thresholds atr_ratio < 0.04 and rolling_vol_5d < 0.025.

    Scoring: rank by rolling_vol_5d ascending (calmest first) so the
    quietest tail of the band appears first in the union ordering.

    use_full_universe = True: low-activity stocks score poorly on the
    DynamicAgent's activity-biased opportunity_score and are excluded from
    the top-80. Scanning all 150 surfaces the correct morphology.
    """

    use_full_universe = True

    def __init__(
        self,
        atr_pct_low:        float = 0.25,
        atr_pct_high:       float = 0.60,
        vol5d_pct_low:      float = 0.25,
        vol5d_pct_high:     float = 0.60,
        max_abs_return:     float = 0.015,
        min_rel_volume:     float = 0.7,
        max_rel_volume:     float = 1.5,
        fallback_atr_max:   float = 0.04,
        fallback_vol5d_max: float = 0.025,
        min_pool_for_pct:   int   = 4,
        top_n:              int   = 20,
    ):
        self.atr_pct_low        = atr_pct_low
        self.atr_pct_high       = atr_pct_high
        self.vol5d_pct_low      = vol5d_pct_low
        self.vol5d_pct_high     = vol5d_pct_high
        self.max_abs_return     = max_abs_return
        self.min_rel_volume     = min_rel_volume
        self.max_rel_volume     = max_rel_volume
        self.fallback_atr_max   = fallback_atr_max
        self.fallback_vol5d_max = fallback_vol5d_max
        self.min_pool_for_pct   = min_pool_for_pct
        self.top_n              = top_n

    @staticmethod
    def _pct(sorted_vals: list[float], q: float) -> float:
        # Linear-interpolating percentile on a pre-sorted list. No numpy dep —
        # the rest of this module is pure stdlib and we keep that constraint.
        if not sorted_vals:
            return 0.0
        if len(sorted_vals) == 1:
            return sorted_vals[0]
        pos = q * (len(sorted_vals) - 1)
        lo  = int(pos)
        hi  = min(lo + 1, len(sorted_vals) - 1)
        frac = pos - lo
        return sorted_vals[lo] * (1.0 - frac) + sorted_vals[hi] * frac

    def select_universe(
        self, candidates: list[UniverseCandidate]
    ) -> list[UniverseCandidate]:
        atr_vals   = sorted(c.atr_ratio      for c in candidates if c.atr_ratio      > 0)
        vol5d_vals = sorted(c.rolling_vol_5d for c in candidates if c.rolling_vol_5d > 0)

        use_pct = (
            len(atr_vals)   >= self.min_pool_for_pct
            and len(vol5d_vals) >= self.min_pool_for_pct
        )
        if use_pct:
            atr_lo   = self._pct(atr_vals,   self.atr_pct_low)
            atr_hi   = self._pct(atr_vals,   self.atr_pct_high)
            vol5d_lo = self._pct(vol5d_vals, self.vol5d_pct_low)
            vol5d_hi = self._pct(vol5d_vals, self.vol5d_pct_high)
        else:
            # Warm-up / sparse-pool fallback: fixed absolute thresholds.
            atr_lo,   atr_hi   = 0.0, self.fallback_atr_max
            vol5d_lo, vol5d_hi = 0.0, self.fallback_vol5d_max

        filtered = [
            c for c in candidates
            if atr_lo   <= c.atr_ratio      <= atr_hi
            and vol5d_lo <= c.rolling_vol_5d <= vol5d_hi
            and abs(c.daily_return) < self.max_abs_return
            and self.min_rel_volume <= c.relative_volume <= self.max_rel_volume
        ]
        # Calmest first — QuietBrk wants the slowest drifters, not the
        # busiest of the quiet cohort.
        filtered.sort(key=lambda c: c.rolling_vol_5d)
        return filtered[: self.top_n]

    def select_symbols(
        self,
        candidates: list[UniverseCandidate],
        all_candidates: list[UniverseCandidate] | None = None,
    ) -> list[str]:
        src = all_candidates if (self.use_full_universe and all_candidates is not None) else candidates
        return [c.symbol for c in self.select_universe(src)]


class ActivityTailFilter:
    """
    Selects the activity tail — stocks Breakout's strict thresholds reject
    but that are still active enough for a 20-day breakout signal to fire.

    Why this exists (replaces QuietBreakoutUniverseFilter for QuietBrk's lane):
    The middle-band quiet filter (QuietBreakoutUniverseFilter) gave QuietBrk
    structurally inactive stocks — low ATR ratio, low rolling vol, no daily
    move. But QuietBreakoutStrategy's entry signal (price > high_20d with
    vol_ratio > 1.2) needs *movement* to fire. Inactive stocks rarely break
    above a 20-day high. Empirically (2 backtest runs), QuietBrk fired only
    1-5 trades per period in the ensemble on that universe, vs 287 trades in
    Crash and 546 trades in Recov standalone on the relaxed-Breakout universe.

    This filter gives QuietBrk a universe closer to its standalone one
    (moderate-activity stocks) while structurally avoiding Breakout's strict
    territory — so the asymmetric router gate (exclusive_strategies={"QuietBrk"})
    keeps these reserved for QuietBrk without poaching opportunities Breakout
    would otherwise take.

    Hard filters (on the top-80 broad pool):
      - NOT (relative_volume > breakout_vol_threshold
             AND |daily_return| > breakout_return_threshold)
                                                       — exclude Breakout's strict picks
      - relative_volume > min_vol                      — still moderate volume
      - |daily_return|  > min_abs_return               — still moves enough to break out

    Scoring: rank by candidate.score descending (same activity-based metric
    Breakout uses) so the best of the second-tier appears first.

    use_full_universe = False: operates on the activity-biased top-80, the
    pool where 20-day breakouts actually happen. The all-150 pool's tail
    (stocks rank 80-150) is the dead zone QuietBrk struggled with before.
    """

    use_full_universe = False

    def __init__(
        self,
        breakout_vol_threshold:    float = 1.5,
        breakout_return_threshold: float = 0.015,
        min_vol:                   float = 1.0,
        min_abs_return:            float = 0.005,
        top_n:                     int   = 20,
    ):
        self.breakout_vol_threshold    = breakout_vol_threshold
        self.breakout_return_threshold = breakout_return_threshold
        self.min_vol                   = min_vol
        self.min_abs_return            = min_abs_return
        self.top_n                     = top_n

    def select_universe(
        self, candidates: list[UniverseCandidate]
    ) -> list[UniverseCandidate]:
        filtered = [
            c for c in candidates
            if not (
                c.relative_volume > self.breakout_vol_threshold
                and abs(c.daily_return) > self.breakout_return_threshold
            )
            and c.relative_volume > self.min_vol
            and abs(c.daily_return) > self.min_abs_return
        ]
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
        # Accept either:
        #   [filter, filter, ...]            — legacy untagged form
        #   [(strategy_name, filter), ...]   — tagged form for per-strategy gating
        # When tagged, `last_per_strategy_symbols` is populated after each
        # select_universe call so MultiStrategyRouter can blind each strategy
        # to symbols outside its assigned slice (preventing Breakout from
        # poaching QuietBrk's quiet stocks in `symbol_states`).
        if filters and isinstance(filters[0], tuple):
            self._tags   = [t for (t, _) in filters]
            self.filters = [f for (_, f) in filters]
        else:
            self._tags   = [None] * len(filters)
            self.filters = list(filters)
        self.top_n   = sum(getattr(f, "top_n", 20) for f in self.filters)
        # Per-filter overlap diagnostics. `absorbed_by_earlier[i]` counts how
        # many candidates filter i selected that were already claimed by an
        # earlier filter in the union ordering. `call_count` lets callers
        # report mean/max per day at end-of-period. Reset is intentional:
        # counters are cumulative across the run.
        self.absorbed_by_earlier: dict[int, int] = {i: 0 for i in range(len(self.filters))}
        self.absorbed_max:        dict[int, int] = {i: 0 for i in range(len(self.filters))}
        self.call_count:          int            = 0
        # Latest per-strategy symbol sets from the most recent select_universe
        # call. Only populated for tagged filters; untagged entries contribute
        # nothing (router's gate no-ops when a strategy name is absent).
        self.last_per_strategy_symbols: dict[str, set] = {}

    def get_overlap_stats(self) -> list[dict]:
        """
        Per-filter overlap stats since instantiation. One dict per filter:
            {name, total_absorbed, max_absorbed_in_a_call, mean_per_call}

        Use after a backtest period to confirm structurally orthogonal slices.
        Low mean (< 3/day) = filters select different cohorts. High mean
        (> 8/day) = filters competing for same names; carve isn't working.
        """
        calls = max(self.call_count, 1)
        return [
            {
                "name":                   type(self.filters[i]).__name__,
                "total_absorbed":         self.absorbed_by_earlier[i],
                "max_absorbed_in_a_call": self.absorbed_max[i],
                "mean_per_call":          self.absorbed_by_earlier[i] / calls,
            }
            for i in range(len(self.filters))
        ]

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
        self.call_count += 1
        per_strategy: dict[str, set] = {}
        for i, f in enumerate(self.filters):
            src = full_pool if getattr(f, "use_full_universe", False) else candidates
            absorbed_this_call = 0
            picks = f.select_universe(src)
            tag   = self._tags[i]
            if tag is not None:
                per_strategy[tag] = {c.symbol for c in picks}
            for candidate in picks:
                if candidate.symbol not in seen:
                    seen.add(candidate.symbol)
                    result.append(candidate)
                else:
                    absorbed_this_call += 1
            self.absorbed_by_earlier[i] += absorbed_this_call
            if absorbed_this_call > self.absorbed_max[i]:
                self.absorbed_max[i] = absorbed_this_call
        # Mutate in place so callers holding a reference to last_per_strategy_symbols
        # see the new bar's slices without re-fetching the attribute each call.
        self.last_per_strategy_symbols.clear()
        self.last_per_strategy_symbols.update(per_strategy)
        return result

    def select_symbols(
        self,
        candidates: list[UniverseCandidate],
        all_candidates: list[UniverseCandidate] | None = None,
    ) -> list[str]:
        return [c.symbol for c in self.select_universe(candidates, all_candidates)]
