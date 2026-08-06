"""
Strategy-filter diagnostics for the universe layer.

This is a replay-only observer. It calls the existing DynamicUniverseAgent and
universe filters on cached data, then records why each strategy-specific filter
accepted or rejected each candidate. It does not mutate or replace trading
behaviour.
"""

from __future__ import annotations

import csv
import os
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from app.universe.filters import (
    ActivityTailFilter,
    BreakoutUniverseFilter,
    DualMAUniverseFilter,
    MeanReversionUniverseFilter,
    PullbackUniverseFilter,
    QuietBreakoutUniverseFilter,
)
from app.universe.models import UniverseCandidate


PASSED = ""
UNKNOWN = "UNKNOWN"
FILTER_TOP_N_CUTOFF = "FILTER_TOP_N_CUTOFF"
LIQUIDITY_FILTER = "LIQUIDITY_FILTER"


@dataclass
class StrategyFilterDiagnosticRecord:
    date: datetime
    symbol: str
    strategy: str
    passed_filter: bool
    rejection_reason: str
    opportunity_score: float
    overall_rank: Optional[int]
    selected_into_final_union: bool
    raw_filter_metrics: dict = field(default_factory=dict)


@dataclass
class StrategyFilterDiagnostics:
    records: list[StrategyFilterDiagnosticRecord] = field(default_factory=list)

    def print_summary(self, label: str = "") -> None:
        if not self.records:
            return

        by_strategy = defaultdict(lambda: {"passed": 0, "rejected": 0})
        by_reason = Counter()
        for r in self.records:
            if r.passed_filter:
                by_strategy[r.strategy]["passed"] += 1
            else:
                by_strategy[r.strategy]["rejected"] += 1
                by_reason[r.rejection_reason or UNKNOWN] += 1

        print(f"\n  -- Strategy Filter Diagnostics {label} --")
        print("    Rejections by strategy     : " + ", ".join(
            f"{strategy} {vals['rejected']}"
            for strategy, vals in sorted(by_strategy.items())
        ))
        print("    Pass rate per strategy     : " + ", ".join(
            f"{strategy} {_pct(vals['passed'], vals['passed'] + vals['rejected']):.1f}%"
            for strategy, vals in sorted(by_strategy.items())
        ))
        print("    Rejections by reason       : " + ", ".join(
            f"{reason} {count}" for reason, count in by_reason.most_common()
        ))
        print("    Top rejection reasons      : " + ", ".join(
            f"{reason} {count}" for reason, count in by_reason.most_common(10)
        ))

    def export_csv(self, path: str) -> None:
        if not self.records:
            return
        write_header = not os.path.exists(path) or os.path.getsize(path) == 0
        with open(path, "a", newline="") as f:
            w = csv.writer(f)
            if write_header:
                w.writerow([
                    "date",
                    "symbol",
                    "strategy",
                    "passed_filter",
                    "rejection_reason",
                    "opportunity_score",
                    "overall_rank",
                    "selected_into_final_union",
                ])
            for r in self.records:
                w.writerow([
                    r.date.date(),
                    r.symbol,
                    r.strategy,
                    int(r.passed_filter),
                    r.rejection_reason,
                    f"{r.opportunity_score:.6f}",
                    "" if r.overall_rank is None else r.overall_rank,
                    int(r.selected_into_final_union),
                ])


def compute_strategy_filter_diagnostics(ctx, universe_filter) -> StrategyFilterDiagnostics:
    diagnostics = StrategyFilterDiagnostics()

    for date in ctx.historical_dates:
        broad = ctx.dynamic_universe_agent.select_candidates(date)
        all_candidates = ctx.dynamic_universe_agent.select_all_candidates(date)
        overall_rank = {c.symbol: i + 1 for i, c in enumerate(all_candidates)}

        filter_entries = _iter_filter_entries(universe_filter)
        if not filter_entries:
            continue

        final_union = _final_union_symbols(filter_entries, broad, all_candidates)
        for strategy, child_filter in filter_entries:
            source = (
                all_candidates
                if getattr(child_filter, "use_full_universe", False)
                else broad
            )
            picks = child_filter.select_universe(source)
            passed_symbols = {c.symbol for c in picks}
            threshold_reasons = {
                c.symbol: _threshold_rejection_reason(child_filter, c, source)
                for c in source
            }

            for candidate in source:
                passed = candidate.symbol in passed_symbols
                diagnostics.records.append(StrategyFilterDiagnosticRecord(
                    date=date,
                    symbol=candidate.symbol,
                    strategy=strategy,
                    passed_filter=passed,
                    rejection_reason=PASSED if passed else _rejection_reason(
                        threshold_reasons.get(candidate.symbol, UNKNOWN)
                    ),
                    opportunity_score=float(candidate.score),
                    overall_rank=overall_rank.get(candidate.symbol),
                    selected_into_final_union=candidate.symbol in final_union,
                    raw_filter_metrics=_raw_metrics(candidate),
                ))

    return diagnostics


def _iter_filter_entries(universe_filter) -> list[tuple[str, object]]:
    filters = getattr(universe_filter, "filters", None)
    if filters is None:
        return [(_strategy_name(None, universe_filter), universe_filter)]
    tags = getattr(universe_filter, "_tags", [None] * len(filters))
    return [
        (_strategy_name(tag, child_filter), child_filter)
        for tag, child_filter in zip(tags, filters)
    ]


def _strategy_name(tag, child_filter) -> str:
    if tag:
        return str(tag)
    name = type(child_filter).__name__
    return name.removesuffix("UniverseFilter").removesuffix("Filter")


def _final_union_symbols(filter_entries, broad, all_candidates) -> set[str]:
    seen: set[str] = set()
    for _strategy, child_filter in filter_entries:
        source = (
            all_candidates
            if getattr(child_filter, "use_full_universe", False)
            else broad
        )
        for candidate in child_filter.select_universe(source):
            seen.add(candidate.symbol)
    return seen


def _rejection_reason(threshold_reason: str) -> str:
    if threshold_reason == PASSED:
        return FILTER_TOP_N_CUTOFF
    return threshold_reason or UNKNOWN


def _threshold_rejection_reason(
    child_filter,
    c: UniverseCandidate,
    candidates: list[UniverseCandidate],
) -> str:
    if isinstance(child_filter, BreakoutUniverseFilter):
        if c.relative_volume <= child_filter.vol_threshold:
            return "BREAKOUT_VOLUME_FILTER"
        if abs(c.daily_return) <= child_filter.return_threshold:
            return "BREAKOUT_RANGE_FILTER"
        return PASSED

    if isinstance(child_filter, ActivityTailFilter):
        if (
            c.relative_volume > child_filter.breakout_vol_threshold
            and abs(c.daily_return) > child_filter.breakout_return_threshold
        ):
            return "QUIET_BREAKOUT_STRICT_BREAKOUT_OVERLAP"
        if c.relative_volume <= child_filter.min_vol:
            return LIQUIDITY_FILTER
        if abs(c.daily_return) <= child_filter.min_abs_return:
            return "QUIET_BREAKOUT_RANGE_FILTER"
        return PASSED

    if isinstance(child_filter, PullbackUniverseFilter):
        if not c.sma_20_above_sma_50 or not c.sma_20_slope_positive:
            return "TREND_PULLBACK_NOT_IN_UPTREND"
        if not (c.return_3d < -child_filter.min_pullback):
            return "TREND_PULLBACK_NOT_PULLING_BACK"
        if not (c.return_3d > -child_filter.max_pullback):
            return "TREND_PULLBACK_CRASH_FILTER"
        if not (c.relative_volume < child_filter.max_vol):
            return LIQUIDITY_FILTER
        return PASSED

    if isinstance(child_filter, MeanReversionUniverseFilter):
        if not c.sma_20_above_sma_50:
            return "RSI_NOT_IN_UPTREND"
        if c.sma_cross_age < child_filter.min_cross_age:
            return "RSI_TREND_TOO_FRESH"
        if not (c.return_3d < -child_filter.min_3d_drop):
            return "RSI_NOT_OVERSOLD"
        if not (c.return_3d > -child_filter.max_3d_drop):
            return "RSI_CRASH_FILTER"
        return PASSED

    if isinstance(child_filter, DualMAUniverseFilter):
        if not c.sma_20_above_sma_50:
            return "DUAL_MA_NOT_ALIGNED"
        if not (1 <= c.sma_cross_age <= child_filter.max_cross_age):
            return "DUAL_MA_CROSS_AGE_FILTER"
        if c.relative_volume < child_filter.min_vol:
            return LIQUIDITY_FILTER
        return PASSED

    if isinstance(child_filter, QuietBreakoutUniverseFilter):
        atr_lo, atr_hi, vol5d_lo, vol5d_hi = _quiet_breakout_bounds(child_filter, candidates)
        if not (atr_lo <= c.atr_ratio <= atr_hi):
            return "QUIET_BREAKOUT_ATR_FILTER"
        if not (vol5d_lo <= c.rolling_vol_5d <= vol5d_hi):
            return "QUIET_BREAKOUT_VOLATILITY_FILTER"
        if not (abs(c.daily_return) < child_filter.max_abs_return):
            return "QUIET_BREAKOUT_RANGE_FILTER"
        if not (child_filter.min_rel_volume <= c.relative_volume <= child_filter.max_rel_volume):
            return LIQUIDITY_FILTER
        return PASSED

    return UNKNOWN


def _quiet_breakout_bounds(child_filter, candidates: list[UniverseCandidate]) -> tuple[float, float, float, float]:
    atr_vals = sorted(c.atr_ratio for c in candidates if c.atr_ratio > 0)
    vol5d_vals = sorted(c.rolling_vol_5d for c in candidates if c.rolling_vol_5d > 0)
    use_pct = (
        len(atr_vals) >= child_filter.min_pool_for_pct
        and len(vol5d_vals) >= child_filter.min_pool_for_pct
    )
    if not use_pct:
        return 0.0, child_filter.fallback_atr_max, 0.0, child_filter.fallback_vol5d_max
    return (
        child_filter._pct(atr_vals, child_filter.atr_pct_low),
        child_filter._pct(atr_vals, child_filter.atr_pct_high),
        child_filter._pct(vol5d_vals, child_filter.vol5d_pct_low),
        child_filter._pct(vol5d_vals, child_filter.vol5d_pct_high),
    )


def _raw_metrics(c: UniverseCandidate) -> dict:
    return {
        "relative_volume": c.relative_volume,
        "daily_return": c.daily_return,
        "abs_daily_return": abs(c.daily_return),
        "return_3d": c.return_3d,
        "rolling_vol_5d": c.rolling_vol_5d,
        "atr_ratio": c.atr_ratio,
        "sma_20_above_sma_50": c.sma_20_above_sma_50,
        "sma_20_slope_positive": c.sma_20_slope_positive,
        "sma_cross_age": c.sma_cross_age,
        "price": c.price,
    }


def _pct(num: int, den: int) -> float:
    return (num / den * 100.0) if den else 0.0
