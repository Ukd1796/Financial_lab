"""
Universe Diagnostics Layer
--------------------------
Post-hoc analysis of daily universe selections.
Called by re-running the universe filter on ctx.historical_dates
after each experiment — zero behavior change, no engine modifications.

All computation is in-memory using already-loaded DynamicUniverseAgent cache.
"""

from __future__ import annotations

import csv
from collections import deque
from dataclasses import dataclass
from datetime import datetime
from typing import List


@dataclass
class DailyUniverseRecord:
    date: datetime
    symbols: List[str]
    n_selected: int
    daily_turnover_pct: float     # fraction of symbols that changed vs yesterday
    overlap_count: int            # symbols shared with yesterday's universe
    weekly_turnover_pct: float    # fraction that changed vs 5 days ago
    stability_score: float        # 1 - rolling_avg(daily_turnover, 10d)
    leader_half_life_days: float  # mean consecutive-day tenure of current members


class UniverseTracker:
    """
    Records daily universe selections and computes stability/turnover metrics.

    Usage
    -----
    tracker = UniverseTracker()
    for date in ctx.historical_dates:
        broad = ctx.dynamic_universe_agent.select_candidates(date)
        symbols = universe_filter.select_symbols(broad)
        tracker.record(date, symbols)
    tracker.export_csv("daily_universe_metrics.csv")
    """

    def __init__(self):
        self.daily_records: List[DailyUniverseRecord] = []
        # Rolling history for turnover/stability — keep last 10 entries
        self._history: deque = deque(maxlen=10)
        # Tracks when each symbol first appeared (for half-life calculation).
        # Resets when a symbol leaves the universe and re-enters.
        self._symbol_streak: dict[str, tuple[datetime, int]] = {}  # sym → (first_date, days)

    def record(self, date: datetime, symbols: List[str]) -> None:
        """Ingest one day of universe selection and compute metrics."""
        sym_set = frozenset(symbols)

        # --- Daily turnover / overlap vs yesterday ---
        if self._history:
            prev_set = self._history[-1][1]
            entries   = sym_set - prev_set
            daily_turnover_pct = len(entries) / max(len(sym_set), 1)
            overlap_count      = len(sym_set & prev_set)
        else:
            daily_turnover_pct = 1.0
            overlap_count      = 0

        # --- Weekly turnover vs 5 days ago ---
        if len(self._history) >= 5:
            week_ago = self._history[-5][1]
            weekly_turnover_pct = len(sym_set - week_ago) / max(len(sym_set), 1)
        else:
            weekly_turnover_pct = daily_turnover_pct

        # --- Stability score: 1 - rolling avg daily turnover (last 10d) ---
        recent_turnovers = [
            len(sym_set - s) / max(len(sym_set), 1)
            for (_, s) in self._history
        ]
        if recent_turnovers:
            stability_score = 1.0 - sum(recent_turnovers) / len(recent_turnovers)
        else:
            stability_score = 0.0

        # --- Leader half-life: mean streak length of current universe members ---
        # Symbols that left the universe reset their streak counter.
        all_known = set(self._symbol_streak.keys())
        exited = all_known - sym_set
        for sym in exited:
            del self._symbol_streak[sym]   # streak resets on exit

        for sym in sym_set:
            if sym in self._symbol_streak:
                first_dt, days = self._symbol_streak[sym]
                self._symbol_streak[sym] = (first_dt, days + 1)
            else:
                self._symbol_streak[sym] = (date, 1)

        streaks = [days for (_, days) in self._symbol_streak.values()]
        leader_half_life = sum(streaks) / len(streaks) if streaks else 0.0

        self.daily_records.append(DailyUniverseRecord(
            date=date,
            symbols=list(symbols),
            n_selected=len(symbols),
            daily_turnover_pct=daily_turnover_pct,
            overlap_count=overlap_count,
            weekly_turnover_pct=weekly_turnover_pct,
            stability_score=stability_score,
            leader_half_life_days=leader_half_life,
        ))
        self._history.append((date, sym_set))

    def summary_stats(self) -> dict:
        """Aggregate stats across all recorded days."""
        if not self.daily_records:
            return {}
        n = len(self.daily_records)
        return {
            "trading_days":           n,
            "avg_daily_turnover_pct": sum(r.daily_turnover_pct  for r in self.daily_records) / n,
            "avg_weekly_turnover_pct": sum(r.weekly_turnover_pct for r in self.daily_records) / n,
            "avg_stability_score":    sum(r.stability_score      for r in self.daily_records) / n,
            "avg_leader_half_life_days": sum(r.leader_half_life_days for r in self.daily_records) / n,
        }

    def export_csv(self, path: str, period_label: str = "", run_label: str = "") -> None:
        """Append (or create) a CSV at `path` with one row per trading day."""
        if not self.daily_records:
            return
        import os
        write_header = not os.path.exists(path) or os.path.getsize(path) == 0
        with open(path, "a", newline="") as f:
            w = csv.writer(f)
            if write_header:
                w.writerow([
                    "period", "run",
                    "date", "n_selected",
                    "daily_turnover_pct", "overlap_count",
                    "weekly_turnover_pct", "stability_score",
                    "leader_half_life_days", "symbols",
                ])
            for r in self.daily_records:
                w.writerow([
                    period_label, run_label,
                    r.date.date(),
                    r.n_selected,
                    f"{r.daily_turnover_pct:.4f}",
                    r.overlap_count,
                    f"{r.weekly_turnover_pct:.4f}",
                    f"{r.stability_score:.4f}",
                    f"{r.leader_half_life_days:.1f}",
                    "|".join(r.symbols),
                ])


def compute_universe_diagnostics(ctx, universe_filter) -> UniverseTracker:
    """
    Re-run universe selection on all historical dates from ctx.
    No DB queries — all data is in DynamicUniverseAgent._cache.
    Returns a populated UniverseTracker.
    """
    tracker = UniverseTracker()
    for date in ctx.historical_dates:
        try:
            broad   = ctx.dynamic_universe_agent.select_candidates(date)
            symbols = universe_filter.select_symbols(broad)
            tracker.record(date, symbols)
        except Exception:
            pass   # tolerate missing data on a date
    return tracker
