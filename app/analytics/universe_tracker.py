"""
Universe Diagnostics Layer
--------------------------
Post-hoc analysis of daily universe selections.
Called by re-running the universe filter on ctx.historical_dates
after each experiment — zero behavior change, no engine modifications.

All computation is in-memory using already-loaded DynamicUniverseAgent cache.

Two tiers of metrics
--------------------
1. Composition metrics (per trading day) — turnover, promotions/demotions,
   stability, leader half-life, universe entropy.
2. Trajectory metrics (per symbol-tenure segment) — score/rank paths, score
   volatility, rank slope. These answer *why* the universe churns: are names
   flickering across the top-N cliff (high score volatility, high entropy),
   or decaying out slowly (negative rank slope)?
"""

from __future__ import annotations

import csv
import math
from collections import deque
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional, Tuple


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
    # --- extended composition metrics (default 0 → backward compatible) ---
    promotions: int = 0           # symbols entering the universe today (vs yesterday)
    demotions: int = 0            # symbols leaving the universe today (vs yesterday)
    universe_entropy: float = 0.0  # normalized Shannon entropy of opportunity scores
                                   # 1.0 = uniform (ambiguous cutoff, churn-prone);
                                   # low = a few clear leaders separate from the pack


@dataclass
class TrajectorySegment:
    """One continuous tenure of a symbol inside the universe."""
    symbol: str
    streak_id: int
    first_date: datetime
    last_date: datetime
    tenure_days: int
    entry_rank: int
    exit_rank: int
    entry_score: float
    exit_score: float
    score_min: float
    score_max: float
    score_std: float      # volatility of opportunity_score over the tenure
    rank_std: float        # volatility of daily rank over the tenure
    rank_slope: float      # (exit_rank - entry_rank) / tenure; >0 = decaying out


class UniverseTracker:
    """
    Records daily universe selections and computes stability/turnover +
    trajectory metrics.

    Usage
    -----
    tracker = UniverseTracker()
    for date in ctx.historical_dates:
        broad   = ctx.dynamic_universe_agent.select_candidates(date)
        scores  = {c.symbol: c.score for c in broad}
        symbols = universe_filter.select_symbols(broad)
        tracker.record(date, symbols, scores={s: scores[s] for s in symbols})
    tracker.finalize()
    tracker.export_csv("daily_universe_metrics.csv")
    tracker.export_trajectories_csv("universe_trajectories.csv")
    """

    def __init__(self):
        self.daily_records: List[DailyUniverseRecord] = []
        # Rolling history for turnover/stability — keep last 10 entries
        self._history: deque = deque(maxlen=10)
        # Tracks when each symbol first appeared (for half-life calculation).
        # Resets when a symbol leaves the universe and re-enters.
        self._symbol_streak: dict[str, tuple[datetime, int]] = {}  # sym → (first_date, days)

        # --- trajectory bookkeeping ---
        # Active per-symbol streak of (date, score, rank) observations.
        self._traj_active: Dict[str, List[Tuple[datetime, float, int]]] = {}
        self._streak_seq: int = 0
        self._streak_id: Dict[str, int] = {}
        self.segments: List[TrajectorySegment] = []

    def record(
        self,
        date: datetime,
        symbols: List[str],
        scores: Optional[Dict[str, float]] = None,
    ) -> None:
        """
        Ingest one day of universe selection and compute metrics.

        `scores` (symbol → opportunity_score) is optional. When supplied it
        unlocks the entropy metric and the per-symbol trajectory segments.
        When omitted the tracker behaves exactly as before.
        """
        sym_set = frozenset(symbols)

        # Rank within today's selected universe (1 = highest opportunity score).
        rank_map: Dict[str, int] = {}
        if scores:
            ordered = sorted(symbols, key=lambda s: scores.get(s, 0.0), reverse=True)
            rank_map = {s: i + 1 for i, s in enumerate(ordered)}

        # --- Daily turnover / overlap / promotions / demotions vs yesterday ---
        if self._history:
            prev_set = self._history[-1][1]
            entries  = sym_set - prev_set
            exits    = prev_set - sym_set
            promotions = len(entries)
            demotions  = len(exits)
            daily_turnover_pct = promotions / max(len(sym_set), 1)
            overlap_count      = len(sym_set & prev_set)
        else:
            promotions = len(sym_set)
            demotions  = 0
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

        # --- Universe entropy: normalized Shannon entropy of opportunity scores ---
        # Measures how separable the top-N is from the pack. Scores bunched near
        # the cutoff (uniform) → high entropy → tiny noise flips membership.
        universe_entropy = 0.0
        if scores:
            vals = [max(scores.get(s, 0.0), 0.0) for s in symbols]
            total = sum(vals)
            if total > 0 and len(vals) > 1:
                ent = 0.0
                for v in vals:
                    if v > 0:
                        p = v / total
                        ent -= p * math.log(p)
                universe_entropy = ent / math.log(len(vals))  # normalize to 0..1

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

        # --- Trajectory segments (only when scores provided) ---
        if scores:
            self._update_trajectories(date, sym_set, scores, rank_map)

        self.daily_records.append(DailyUniverseRecord(
            date=date,
            symbols=list(symbols),
            n_selected=len(symbols),
            daily_turnover_pct=daily_turnover_pct,
            overlap_count=overlap_count,
            weekly_turnover_pct=weekly_turnover_pct,
            stability_score=stability_score,
            leader_half_life_days=leader_half_life,
            promotions=promotions,
            demotions=demotions,
            universe_entropy=universe_entropy,
        ))
        self._history.append((date, sym_set))

    def _update_trajectories(self, date, sym_set, scores, rank_map) -> None:
        """Append today's (score, rank) to each active streak; close exited ones."""
        # Close streaks for symbols that left the universe today.
        exited = set(self._traj_active.keys()) - sym_set
        for sym in exited:
            self._finalize_segment(sym)

        for sym in sym_set:
            obs = (date, float(scores.get(sym, 0.0)), rank_map.get(sym, 0))
            if sym in self._traj_active:
                self._traj_active[sym].append(obs)
            else:
                self._streak_seq += 1
                self._streak_id[sym] = self._streak_seq
                self._traj_active[sym] = [obs]

    def _finalize_segment(self, sym: str) -> None:
        obs = self._traj_active.pop(sym, None)
        if not obs:
            return
        dates  = [o[0] for o in obs]
        vals   = [o[1] for o in obs]
        ranks  = [o[2] for o in obs]
        n      = len(obs)
        tenure = n
        score_std = _std(vals)
        rank_std  = _std([float(r) for r in ranks])
        rank_slope = (ranks[-1] - ranks[0]) / tenure if tenure else 0.0
        self.segments.append(TrajectorySegment(
            symbol=sym,
            streak_id=self._streak_id.get(sym, 0),
            first_date=dates[0],
            last_date=dates[-1],
            tenure_days=tenure,
            entry_rank=ranks[0],
            exit_rank=ranks[-1],
            entry_score=vals[0],
            exit_score=vals[-1],
            score_min=min(vals),
            score_max=max(vals),
            score_std=score_std,
            rank_std=rank_std,
            rank_slope=rank_slope,
        ))

    def finalize(self) -> None:
        """Flush all still-open trajectory streaks into segments. Call once after the loop."""
        for sym in list(self._traj_active.keys()):
            self._finalize_segment(sym)

    def summary_stats(self) -> dict:
        """Aggregate stats across all recorded days + trajectory segments."""
        if not self.daily_records:
            return {}
        n = len(self.daily_records)
        base = {
            "trading_days":           n,
            "avg_daily_turnover_pct": sum(r.daily_turnover_pct  for r in self.daily_records) / n,
            "avg_weekly_turnover_pct": sum(r.weekly_turnover_pct for r in self.daily_records) / n,
            "avg_stability_score":    sum(r.stability_score      for r in self.daily_records) / n,
            "avg_leader_half_life_days": sum(r.leader_half_life_days for r in self.daily_records) / n,
            "avg_promotions_per_day": sum(r.promotions for r in self.daily_records) / n,
            "avg_demotions_per_day":  sum(r.demotions  for r in self.daily_records) / n,
            "avg_universe_entropy":   sum(r.universe_entropy for r in self.daily_records) / n,
        }
        if self.segments:
            segs = self.segments
            m = len(segs)
            base.update({
                "trajectory_segments":     m,
                "avg_tenure_days":         sum(s.tenure_days for s in segs) / m,
                "median_tenure_days":      _median([s.tenure_days for s in segs]),
                "avg_score_volatility":    sum(s.score_std for s in segs) / m,
                "avg_rank_volatility":     sum(s.rank_std for s in segs) / m,
                "avg_rank_slope":          sum(s.rank_slope for s in segs) / m,
                "pct_single_day_tenures":  100.0 * sum(1 for s in segs if s.tenure_days == 1) / m,
            })
        return base

    def print_summary(self, label: str = "") -> None:
        s = self.summary_stats()
        if not s:
            return
        print(f"\n  ── Universe Stability Diagnostics {label} ──")
        print(f"    Trading days              : {s['trading_days']}")
        print(f"    Avg daily turnover        : {s['avg_daily_turnover_pct']*100:>6.1f}%")
        print(f"    Avg weekly turnover       : {s['avg_weekly_turnover_pct']*100:>6.1f}%")
        print(f"    Avg stability score       : {s['avg_stability_score']:>6.3f}  (1=static)")
        print(f"    Avg leader half-life      : {s['avg_leader_half_life_days']:>6.1f} days")
        print(f"    Avg promotions / day      : {s['avg_promotions_per_day']:>6.1f}")
        print(f"    Avg demotions / day       : {s['avg_demotions_per_day']:>6.1f}")
        print(f"    Avg universe entropy      : {s['avg_universe_entropy']:>6.3f}  (1=uniform/churn-prone)")
        if "trajectory_segments" in s:
            print(f"    Tenure segments           : {s['trajectory_segments']}")
            print(f"    Avg / median tenure       : {s['avg_tenure_days']:>6.1f} / {s['median_tenure_days']:.0f} days")
            print(f"    Single-day tenures        : {s['pct_single_day_tenures']:>6.1f}%  (in-and-out same-day churn)")
            print(f"    Avg score volatility      : {s['avg_score_volatility']:>6.4f}  (per-tenure std of opp_score)")
            print(f"    Avg rank volatility       : {s['avg_rank_volatility']:>6.2f}  (per-tenure std of daily rank)")
            print(f"    Avg rank slope            : {s['avg_rank_slope']:>+6.3f}  (>0 = names decay out over tenure)")

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
                    "leader_half_life_days",
                    "promotions", "demotions", "universe_entropy",
                    "symbols",
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
                    r.promotions, r.demotions,
                    f"{r.universe_entropy:.4f}",
                    "|".join(r.symbols),
                ])

    def export_trajectories_csv(self, path: str, period_label: str = "", run_label: str = "") -> None:
        """Append (or create) a CSV with one row per symbol-tenure segment."""
        if not self.segments:
            return
        import os
        write_header = not os.path.exists(path) or os.path.getsize(path) == 0
        with open(path, "a", newline="") as f:
            w = csv.writer(f)
            if write_header:
                w.writerow([
                    "period", "run", "symbol", "streak_id",
                    "first_date", "last_date", "tenure_days",
                    "entry_rank", "exit_rank", "rank_slope", "rank_std",
                    "entry_score", "exit_score", "score_min", "score_max", "score_std",
                ])
            for s in self.segments:
                w.writerow([
                    period_label, run_label, s.symbol, s.streak_id,
                    s.first_date.date(), s.last_date.date(), s.tenure_days,
                    s.entry_rank, s.exit_rank, f"{s.rank_slope:.3f}", f"{s.rank_std:.2f}",
                    f"{s.entry_score:.4f}", f"{s.exit_score:.4f}",
                    f"{s.score_min:.4f}", f"{s.score_max:.4f}", f"{s.score_std:.4f}",
                ])


def _std(xs: List[float]) -> float:
    n = len(xs)
    if n < 2:
        return 0.0
    mean = sum(xs) / n
    return math.sqrt(sum((x - mean) ** 2 for x in xs) / (n - 1))


def _median(xs: List[float]) -> float:
    if not xs:
        return 0.0
    s = sorted(xs)
    mid = len(s) // 2
    if len(s) % 2:
        return float(s[mid])
    return (s[mid - 1] + s[mid]) / 2.0


def compute_universe_diagnostics(ctx, universe_filter) -> UniverseTracker:
    """
    Re-run universe selection on all historical dates from ctx.
    No DB queries — all data is in DynamicUniverseAgent._cache.
    Returns a populated, finalized UniverseTracker (trajectory segments closed).
    """
    tracker = UniverseTracker()
    for date in ctx.historical_dates:
        try:
            # Mirror BacktestEngine exactly: full-universe filters (TrendPB /
            # RSI-MR / DualMA) receive all_candidates; Breakout/QuietBrk get the
            # activity-biased top-80. Score map is built from the union so every
            # traded symbol has its opportunity_score.
            broad = ctx.dynamic_universe_agent.select_candidates(date)
            all_c = ctx.dynamic_universe_agent.select_all_candidates(date)
            score_map = {c.symbol: c.score for c in all_c}
            for c in broad:
                score_map.setdefault(c.symbol, c.score)
            symbols = universe_filter.select_symbols(broad, all_candidates=all_c)
            tracker.record(
                date, symbols,
                scores={s: score_map.get(s, 0.0) for s in symbols},
            )
        except TypeError:
            # Filter without the all_candidates kwarg — fall back to top-80 only.
            broad = ctx.dynamic_universe_agent.select_candidates(date)
            score_map = {c.symbol: c.score for c in broad}
            symbols = universe_filter.select_symbols(broad)
            tracker.record(
                date, symbols,
                scores={s: score_map.get(s, 0.0) for s in symbols},
            )
        except Exception:
            pass   # tolerate missing data on a date
    tracker.finalize()
    return tracker
