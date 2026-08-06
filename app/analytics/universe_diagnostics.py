"""
Research-grade universe diagnostics.

This module is intentionally observational: it replays the same cached
DynamicUniverseAgent and universe filter calls used by analytics, then records
why membership changed without modifying selection, strategies, risk, or
portfolio behaviour.
"""

from __future__ import annotations

import csv
import math
import os
from collections import Counter
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional


SELECTION_INITIAL = "INITIAL_SELECTION"
SELECTION_TOP80 = "TOP80"
SELECTION_FULL_UNIVERSE = "FULL_UNIVERSE_FILTER"
SELECTION_RETAINED = "RETAINED"
SELECTION_UNKNOWN = "UNKNOWN"

EVICTED_FELL_BELOW_TOP80 = "FELL_BELOW_TOP80"
EVICTED_FAILED_VOLUME = "FAILED_VOLUME_FILTER"
EVICTED_FAILED_RETURN = "FAILED_RETURN_FILTER"
EVICTED_FAILED_VOLATILITY = "FAILED_VOLATILITY_FILTER"
EVICTED_FAILED_STRATEGY = "FAILED_STRATEGY_FILTER"
EVICTED_MISSING_DATA = "MISSING_DATA"
EVICTED_UNKNOWN = "UNKNOWN"


@dataclass
class SymbolDiagnostic:
    date: datetime
    symbol: str
    selected_today: bool
    selected_yesterday: bool
    today_rank: Optional[int]
    yesterday_rank: Optional[int]
    today_score: Optional[float]
    yesterday_score: Optional[float]
    rank_delta: Optional[int]
    score_delta: Optional[float]
    volume_rank_today: Optional[int]
    return_rank_today: Optional[int]
    volatility_rank_today: Optional[int]
    selection_reason: str = ""
    eviction_reason: str = ""


@dataclass
class BoundaryDiagnostic:
    date: datetime
    rank_scores: Dict[int, Optional[float]]
    boundary_margin: Optional[float]
    boundary_band_width: Optional[float]


@dataclass
class RankPersistenceDiagnostic:
    entry_date: datetime
    check_date: Optional[datetime]
    symbol: str
    entry_rank: Optional[int]
    entry_score: Optional[float]
    check_rank: Optional[int]
    check_score: Optional[float]
    status: str


@dataclass
class UniverseDiagnosticLayer:
    symbol_records: List[SymbolDiagnostic] = field(default_factory=list)
    boundary_records: List[BoundaryDiagnostic] = field(default_factory=list)
    persistence_records: List[RankPersistenceDiagnostic] = field(default_factory=list)

    def rank_delta_histogram(self) -> Dict[str, int]:
        buckets = {
            "+1": 0,
            "+2": 0,
            "+3": 0,
            "+4": 0,
            "+5": 0,
            "6-10": 0,
            "11-20": 0,
            "21+": 0,
        }
        for r in self.symbol_records:
            if not (r.selected_yesterday and not r.selected_today):
                continue
            if r.rank_delta is None:
                continue
            delta = r.rank_delta
            if delta <= 0:
                continue
            if delta <= 5:
                buckets[f"+{delta}"] += 1
            elif delta <= 10:
                buckets["6-10"] += 1
            elif delta <= 20:
                buckets["11-20"] += 1
            else:
                buckets["21+"] += 1
        return buckets

    def eviction_attribution(self) -> Dict[str, tuple[int, float]]:
        labels = {
            EVICTED_FELL_BELOW_TOP80: "Hard cutoff",
            EVICTED_FAILED_VOLUME: "Volume",
            EVICTED_FAILED_RETURN: "Return",
            EVICTED_FAILED_VOLATILITY: "Volatility",
            EVICTED_FAILED_STRATEGY: "Strategy filter",
            EVICTED_MISSING_DATA: "Missing data",
            EVICTED_UNKNOWN: "Unknown",
        }
        counts = Counter(
            r.eviction_reason
            for r in self.symbol_records
            if r.selected_yesterday and not r.selected_today
        )
        total = sum(counts.values())
        return {
            label: (counts.get(reason, 0), counts.get(reason, 0) / total if total else 0.0)
            for reason, label in labels.items()
        }

    def print_summary(self, label: str = "") -> None:
        exits = sum(1 for r in self.symbol_records if r.selected_yesterday and not r.selected_today)
        entries = sum(1 for r in self.symbol_records if r.selected_today and not r.selected_yesterday)
        margins = [
            r.boundary_margin for r in self.boundary_records
            if r.boundary_margin is not None and not math.isnan(r.boundary_margin)
        ]
        widths = [
            r.boundary_band_width for r in self.boundary_records
            if r.boundary_band_width is not None and not math.isnan(r.boundary_band_width)
        ]
        print(f"\n  -- Universe WHY Diagnostics {label} --")
        print(f"    Entry events               : {entries}")
        print(f"    Exit events                : {exits}")
        if margins:
            print(f"    Avg rank80/81 margin       : {sum(margins) / len(margins):>8.4f}")
        if widths:
            print(f"    Avg rank75-85 band width   : {sum(widths) / len(widths):>8.4f}")
        attrib = self.eviction_attribution()
        if exits:
            print("    Eviction attribution       : " + ", ".join(
                f"{k} {pct * 100:.1f}%" for k, (_n, pct) in attrib.items() if _n
            ))

    def export_symbol_csv(self, path: str, period_label: str = "", run_label: str = "") -> None:
        if not self.symbol_records:
            return
        write_header = not os.path.exists(path) or os.path.getsize(path) == 0
        with open(path, "a", newline="") as f:
            w = csv.writer(f)
            if write_header:
                w.writerow([
                    "period", "run", "date", "symbol",
                    "selected_today", "selected_yesterday",
                    "today_rank", "yesterday_rank",
                    "today_score", "yesterday_score",
                    "rank_delta", "score_delta",
                    "volume_rank_today", "return_rank_today", "volatility_rank_today",
                    "selection_reason", "eviction_reason",
                ])
            for r in self.symbol_records:
                w.writerow([
                    period_label, run_label, r.date.date(), r.symbol,
                    int(r.selected_today), int(r.selected_yesterday),
                    _fmt_int(r.today_rank), _fmt_int(r.yesterday_rank),
                    _fmt_float(r.today_score), _fmt_float(r.yesterday_score),
                    _fmt_int(r.rank_delta), _fmt_float(r.score_delta),
                    _fmt_int(r.volume_rank_today),
                    _fmt_int(r.return_rank_today),
                    _fmt_int(r.volatility_rank_today),
                    r.selection_reason, r.eviction_reason,
                ])

    def export_boundary_csv(self, path: str, period_label: str = "", run_label: str = "") -> None:
        if not self.boundary_records:
            return
        write_header = not os.path.exists(path) or os.path.getsize(path) == 0
        with open(path, "a", newline="") as f:
            w = csv.writer(f)
            ranks = list(range(75, 86))
            if write_header:
                w.writerow([
                    "period", "run", "date",
                    *[f"score_rank{rank}" for rank in ranks],
                    "boundary_margin", "boundary_band_width",
                ])
            for r in self.boundary_records:
                w.writerow([
                    period_label, run_label, r.date.date(),
                    *[_fmt_float(r.rank_scores.get(rank)) for rank in ranks],
                    _fmt_float(r.boundary_margin),
                    _fmt_float(r.boundary_band_width),
                ])

    def export_rank_delta_histogram_csv(
        self, path: str, period_label: str = "", run_label: str = ""
    ) -> None:
        hist = self.rank_delta_histogram()
        write_header = not os.path.exists(path) or os.path.getsize(path) == 0
        with open(path, "a", newline="") as f:
            w = csv.writer(f)
            if write_header:
                w.writerow(["period", "run", "bucket", "count"])
            for bucket, count in hist.items():
                w.writerow([period_label, run_label, bucket, count])

    def export_eviction_attribution_csv(
        self, path: str, period_label: str = "", run_label: str = ""
    ) -> None:
        attrib = self.eviction_attribution()
        write_header = not os.path.exists(path) or os.path.getsize(path) == 0
        with open(path, "a", newline="") as f:
            w = csv.writer(f)
            if write_header:
                w.writerow(["period", "run", "bucket", "count", "pct"])
            for bucket, (count, pct) in attrib.items():
                w.writerow([period_label, run_label, bucket, count, f"{pct:.4f}"])

    def export_rank_persistence_csv(
        self, path: str, period_label: str = "", run_label: str = ""
    ) -> None:
        if not self.persistence_records:
            return
        write_header = not os.path.exists(path) or os.path.getsize(path) == 0
        with open(path, "a", newline="") as f:
            w = csv.writer(f)
            if write_header:
                w.writerow([
                    "period", "run", "entry_date", "check_date", "symbol",
                    "entry_rank", "entry_score", "check_rank", "check_score", "status",
                ])
            for r in self.persistence_records:
                w.writerow([
                    period_label, run_label,
                    r.entry_date.date(),
                    r.check_date.date() if r.check_date else "",
                    r.symbol,
                    _fmt_int(r.entry_rank), _fmt_float(r.entry_score),
                    _fmt_int(r.check_rank), _fmt_float(r.check_score),
                    r.status,
                ])


def compute_research_universe_diagnostics(ctx, universe_filter) -> UniverseDiagnosticLayer:
    layer = UniverseDiagnosticLayer()
    previous: Optional[dict] = None
    day_snapshots: List[dict] = []
    promotions: List[tuple[int, str]] = []

    for idx, date in enumerate(ctx.historical_dates):
        snapshot = _build_day_snapshot(ctx.dynamic_universe_agent, universe_filter, date)
        day_snapshots.append(snapshot)
        layer.boundary_records.append(snapshot["boundary"])

        today_selected = snapshot["selected_set"]
        yesterday_selected = previous["selected_set"] if previous else set()
        symbols_to_record = sorted(today_selected | yesterday_selected)

        for symbol in symbols_to_record:
            selected_today = symbol in today_selected
            selected_yesterday = symbol in yesterday_selected
            today_rank = snapshot["rank_map"].get(symbol)
            yesterday_rank = previous["rank_map"].get(symbol) if previous else None
            today_score = snapshot["score_map"].get(symbol)
            yesterday_score = previous["score_map"].get(symbol) if previous else None

            selection_reason = ""
            eviction_reason = ""
            if selected_today:
                selection_reason = _selection_reason(
                    selected_yesterday=selected_yesterday,
                    has_previous=previous is not None,
                    today_rank=today_rank,
                    top_n=snapshot["top_n"],
                )
                if not selected_yesterday:
                    promotions.append((idx, symbol))
            elif selected_yesterday:
                eviction_reason = _eviction_reason(
                    agent=ctx.dynamic_universe_agent,
                    date=date,
                    symbol=symbol,
                    today_rank=today_rank,
                    top_n=snapshot["top_n"],
                    has_full_universe_filters=snapshot["has_full_universe_filters"],
                )

            layer.symbol_records.append(SymbolDiagnostic(
                date=date,
                symbol=symbol,
                selected_today=selected_today,
                selected_yesterday=selected_yesterday,
                today_rank=today_rank,
                yesterday_rank=yesterday_rank,
                today_score=today_score,
                yesterday_score=yesterday_score,
                rank_delta=(
                    today_rank - yesterday_rank
                    if today_rank is not None and yesterday_rank is not None
                    else None
                ),
                score_delta=(
                    today_score - yesterday_score
                    if today_score is not None and yesterday_score is not None
                    else None
                ),
                volume_rank_today=snapshot["volume_rank_map"].get(symbol),
                return_rank_today=snapshot["return_rank_map"].get(symbol),
                volatility_rank_today=snapshot["volatility_rank_map"].get(symbol),
                selection_reason=selection_reason,
                eviction_reason=eviction_reason,
            ))

        previous = snapshot

    for entry_idx, symbol in promotions:
        entry = day_snapshots[entry_idx]
        check_idx = entry_idx + 5
        check = day_snapshots[check_idx] if check_idx < len(day_snapshots) else None
        check_rank = check["rank_map"].get(symbol) if check else None
        check_score = check["score_map"].get(symbol) if check else None
        layer.persistence_records.append(RankPersistenceDiagnostic(
            entry_date=entry["date"],
            check_date=check["date"] if check else None,
            symbol=symbol,
            entry_rank=entry["rank_map"].get(symbol),
            entry_score=entry["score_map"].get(symbol),
            check_rank=check_rank,
            check_score=check_score,
            status=_persistence_status(check_rank),
        ))

    return layer


def _build_day_snapshot(agent, universe_filter, date: datetime) -> dict:
    broad = agent.select_candidates(date)
    all_candidates = agent.select_all_candidates(date)
    selected = _select_universe(universe_filter, broad, all_candidates)
    selected_set = {c.symbol for c in selected}
    rank_map = {c.symbol: i + 1 for i, c in enumerate(all_candidates)}
    score_map = {c.symbol: float(c.score) for c in all_candidates}
    top_n = int(getattr(agent, "top_n", 80))

    volume_rank_map, return_rank_map, volatility_rank_map = _component_ranks(agent, date)

    return {
        "date": date,
        "selected_set": selected_set,
        "rank_map": rank_map,
        "score_map": score_map,
        "volume_rank_map": volume_rank_map,
        "return_rank_map": return_rank_map,
        "volatility_rank_map": volatility_rank_map,
        "boundary": _boundary_diagnostic(date, all_candidates),
        "top_n": top_n,
        "has_full_universe_filters": _has_full_universe_filters(universe_filter),
    }


def _select_universe(universe_filter, broad, all_candidates):
    try:
        return universe_filter.select_universe(broad, all_candidates=all_candidates)
    except TypeError:
        return universe_filter.select_universe(broad)


def _boundary_diagnostic(date: datetime, all_candidates) -> BoundaryDiagnostic:
    scores = {
        rank: (
            float(all_candidates[rank - 1].score)
            if len(all_candidates) >= rank
            else None
        )
        for rank in range(75, 86)
    }
    rank80 = scores.get(80)
    rank81 = scores.get(81)
    rank75 = scores.get(75)
    rank85 = scores.get(85)
    return BoundaryDiagnostic(
        date=date,
        rank_scores=scores,
        boundary_margin=rank80 - rank81 if rank80 is not None and rank81 is not None else None,
        boundary_band_width=rank75 - rank85 if rank75 is not None and rank85 is not None else None,
    )


def _component_ranks(agent, date: datetime) -> tuple[dict[str, int], dict[str, int], dict[str, int]]:
    build = getattr(agent, "_build_scored_df", None)
    if build is None:
        return {}, {}, {}
    try:
        _rows, scores = build(date)
    except Exception:
        return {}, {}, {}
    if scores is None:
        return {}, {}, {}
    return (
        _rank_series_desc(scores["relative_volume"]),
        _rank_series_desc(scores["abs_daily_return"]),
        _rank_series_desc(scores["rolling_vol_5d"]),
    )


def _rank_series_desc(series) -> dict[str, int]:
    ranks = series.rank(ascending=False, method="min")
    return {str(symbol): int(rank) for symbol, rank in ranks.items() if not math.isnan(float(rank))}


def _selection_reason(
    selected_yesterday: bool,
    has_previous: bool,
    today_rank: Optional[int],
    top_n: int,
) -> str:
    if not has_previous:
        return SELECTION_INITIAL
    if selected_yesterday:
        return SELECTION_RETAINED
    if today_rank is None:
        return SELECTION_UNKNOWN
    if today_rank <= top_n:
        return SELECTION_TOP80
    return SELECTION_FULL_UNIVERSE


def _eviction_reason(
    agent,
    date: datetime,
    symbol: str,
    today_rank: Optional[int],
    top_n: int,
    has_full_universe_filters: bool,
) -> str:
    if today_rank is None:
        return _invalid_signal_reason(agent, date, symbol)
    if today_rank > top_n and not has_full_universe_filters:
        return EVICTED_FELL_BELOW_TOP80
    if today_rank <= top_n or has_full_universe_filters:
        return EVICTED_FAILED_STRATEGY
    return EVICTED_UNKNOWN


def _invalid_signal_reason(agent, date: datetime, symbol: str) -> str:
    cache = getattr(agent, "_cache", {})
    df = cache.get(symbol)
    if df is None or df.empty:
        return EVICTED_MISSING_DATA
    loc_key = df.index.asof(date)
    if loc_key is None or _is_null(loc_key):
        return EVICTED_MISSING_DATA
    row = df.loc[loc_key]
    if _is_null(row.get("relative_volume")):
        return EVICTED_FAILED_VOLUME
    if _is_null(row.get("daily_return")):
        return EVICTED_FAILED_RETURN
    if _is_null(row.get("rolling_vol_5d")):
        return EVICTED_FAILED_VOLATILITY
    return EVICTED_MISSING_DATA


def _has_full_universe_filters(universe_filter) -> bool:
    filters = getattr(universe_filter, "filters", None)
    if filters is None:
        return bool(getattr(universe_filter, "use_full_universe", False))
    return any(bool(getattr(f, "use_full_universe", False)) for f in filters)


def _persistence_status(rank: Optional[int]) -> str:
    if rank is None:
        return "Missing data"
    if rank <= 80:
        return "Still Top80"
    if rank <= 90:
        return "Ranks 81-90"
    if rank <= 100:
        return "Ranks 91-100"
    return "Below100"


def _is_null(value) -> bool:
    try:
        return bool(value is None or str(value) == "NaT" or math.isnan(float(value)))
    except (TypeError, ValueError):
        return False


def _fmt_float(value: Optional[float]) -> str:
    if value is None:
        return ""
    try:
        if math.isnan(float(value)):
            return ""
    except (TypeError, ValueError):
        return ""
    return f"{float(value):.6f}"


def _fmt_int(value: Optional[int]) -> str:
    return "" if value is None else str(int(value))
