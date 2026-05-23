"""
Continuation Quality Engine (CQE)
-----------------------------------
Measures whether the current market environment rewards continuation after
signal activation and classifies the type of continuation present.

OBSERVATIONAL ONLY — no trading decisions are affected.
Designed for future integration into:
  - Participation scaling
  - Dynamic breakout amplification
  - Adaptive strategy weighting

Inputs
------
List[EnrichedTrade] from TradeAnnotator (already produced by analytics pipeline).

Outputs
-------
  - DailyCQERecord per active trading day (rolling 1D / 10D / 20D windows)
  - cqe_metrics.csv
  - cqe_regime_summary.csv
  - Console CONTINUATION QUALITY ENGINE SUMMARY block
"""

from __future__ import annotations

import csv
import os
from collections import defaultdict
from dataclasses import dataclass
from datetime import date, datetime
from typing import Dict, List, Optional


# ──────────────────────────────────────────────────────────────────────────────
# Window metrics — raw aggregates for one rolling window of trades
# ──────────────────────────────────────────────────────────────────────────────

@dataclass
class WindowMetrics:
    n: int
    # Magnitude
    avg_mfe_pct: float
    avg_mae_pct: float
    avg_final_return: float
    avg_drift_1d: Optional[float]
    avg_drift_3d: Optional[float]
    avg_drift_5d: Optional[float]
    continuation_strength: float      # composite [0, 1]
    # Efficiency
    avg_mfe_efficiency: float
    excursion_decay_rate: float       # (avg_mfe − avg_final_return) / avg_mfe
    drift_retention_quality: float    # avg(final_return / mfe) for positive-mfe trades
    # Persistence
    continuation_survival_pct: float  # fraction with continuation_success=True
    half_life_days: float             # median breakout_survival_days
    avg_holding_days: float
    # Speed
    fast_breakout_pct: float          # fraction with drift_1d > 1%
    acceleration_score: Optional[float]  # avg(drift_3d / drift_5d)
    early_move_pct: float             # avg(drift_3d / final_return)


# ──────────────────────────────────────────────────────────────────────────────
# Daily CQE record — one row per active trading day
# ──────────────────────────────────────────────────────────────────────────────

@dataclass
class DailyCQERecord:
    date: date
    window_1d_count: int
    window_10d_count: int
    window_20d_count: int
    # Primary window (10D rolling)
    m10: WindowMetrics
    # 20D comparison
    m20_mfe_efficiency: float
    # Classification
    morphology_10d: str
    morphology_20d: str
    cqe_state: str        # HIGH_QUALITY / MEDIUM_QUALITY / LOW_QUALITY
    participation: str    # FULL / REDUCED / DEFENSIVE


# ──────────────────────────────────────────────────────────────────────────────
# Morphology labels
# ──────────────────────────────────────────────────────────────────────────────

MORPHOLOGIES = (
    "explosive_continuation",
    "stable_continuation",
    "slow_drift",
    "noisy_rotation",
    "weak_continuation",
    "mean_reverting",
)


def _classify_morphology(m: WindowMetrics) -> str:
    """
    Rule-based classification of the continuation environment.
    Rules are evaluated in priority order (first match wins).
    """
    if m.n < 2:
        return "weak_continuation"

    d5 = m.avg_drift_5d or 0.0

    # mean_reverting: sustained negative drift + negative final return
    if d5 < -0.005 and m.avg_final_return < -0.005:
        return "mean_reverting"

    # explosive_continuation: large moves, high capture, high survival
    if (m.avg_mfe_pct > 0.04
            and m.avg_mfe_efficiency > 0.65
            and m.continuation_survival_pct > 0.60):
        return "explosive_continuation"

    # stable_continuation: moderate moves, good efficiency, good survival
    if (m.avg_mfe_efficiency > 0.50
            and m.continuation_survival_pct > 0.50
            and m.avg_mfe_pct > 0.015):
        return "stable_continuation"

    # noisy_rotation: large excursions but poor capture (in-and-out churn)
    if m.avg_mfe_pct > 0.03 and m.avg_mfe_efficiency < 0.40:
        return "noisy_rotation"

    # slow_drift: small, positive, persistent movement
    if m.avg_final_return > 0 and d5 > 0 and m.avg_mfe_efficiency > 0.35:
        return "slow_drift"

    return "weak_continuation"


def _cqe_state(m: WindowMetrics, morphology: str) -> str:
    high_morphs = {"explosive_continuation", "stable_continuation"}
    low_morphs  = {"noisy_rotation", "weak_continuation", "mean_reverting"}

    if (morphology in high_morphs
            and m.avg_mfe_efficiency > 0.52
            and m.continuation_survival_pct > 0.52):
        return "HIGH_QUALITY"
    if morphology in low_morphs or m.avg_mfe_efficiency < 0.35:
        return "LOW_QUALITY"
    return "MEDIUM_QUALITY"


def _participation(state: str) -> str:
    return {"HIGH_QUALITY": "FULL", "MEDIUM_QUALITY": "REDUCED"}.get(state, "DEFENSIVE")


# ──────────────────────────────────────────────────────────────────────────────
# Window metrics computation
# ──────────────────────────────────────────────────────────────────────────────

def _empty() -> WindowMetrics:
    return WindowMetrics(
        n=0, avg_mfe_pct=0.0, avg_mae_pct=0.0, avg_final_return=0.0,
        avg_drift_1d=None, avg_drift_3d=None, avg_drift_5d=None,
        continuation_strength=0.0, avg_mfe_efficiency=0.0,
        excursion_decay_rate=0.0, drift_retention_quality=0.0,
        continuation_survival_pct=0.0, half_life_days=0.0,
        avg_holding_days=0.0, fast_breakout_pct=0.0,
        acceleration_score=None, early_move_pct=0.0,
    )


def _compute_window(trades: list) -> WindowMetrics:
    if not trades:
        return _empty()
    n = len(trades)

    # ── Magnitude ────────────────────────────────────────────────────────────
    avg_mfe  = sum(t.mfe_pct for t in trades) / n
    avg_mae  = sum(t.mae_pct for t in trades) / n
    avg_ret  = sum(t.final_return_pct for t in trades) / n

    d1v = [t.drift_1d for t in trades if t.drift_1d is not None]
    d3v = [t.drift_3d for t in trades if t.drift_3d is not None]
    d5v = [t.drift_5d for t in trades if t.drift_5d is not None]
    avg_d1 = sum(d1v) / len(d1v) if d1v else None
    avg_d3 = sum(d3v) / len(d3v) if d3v else None
    avg_d5 = sum(d5v) / len(d5v) if d5v else None

    # ── Efficiency ───────────────────────────────────────────────────────────
    effs = [t.mfe_efficiency for t in trades if -1.0 <= t.mfe_efficiency <= 2.0]
    avg_eff = sum(effs) / len(effs) if effs else 0.0
    decay   = max(0.0, (avg_mfe - avg_ret) / avg_mfe) if avg_mfe > 0.001 else 0.0

    pos_mfe = [(t.final_return_pct, t.mfe_pct) for t in trades if t.mfe_pct > 0.001]
    drift_ret = (
        sum(fr / mfe for fr, mfe in pos_mfe) / len(pos_mfe) if pos_mfe else 0.0
    )

    # ── Persistence ──────────────────────────────────────────────────────────
    cont_surv = sum(1 for t in trades if t.continuation_success) / n
    surv_sorted = sorted(t.breakout_survival_days for t in trades)
    half_life = float(surv_sorted[len(surv_sorted) // 2])
    avg_hold  = sum(t.holding_days for t in trades) / n

    # ── Speed ────────────────────────────────────────────────────────────────
    fast_brk = sum(1 for v in d1v if v > 0.01) / max(len(d1v), 1)

    accel_pairs = [
        (t.drift_3d, t.drift_5d) for t in trades
        if t.drift_3d is not None and t.drift_5d is not None
        and abs(t.drift_5d) > 0.001
    ]
    accel = (
        sum(d3 / d5 for d3, d5 in accel_pairs) / len(accel_pairs)
        if accel_pairs else None
    )

    early_pairs = [
        (t.drift_3d, t.final_return_pct) for t in trades
        if t.drift_3d is not None and abs(t.final_return_pct) > 0.001
    ]
    early_move = max(-2.0, min(2.0, (
        sum(d3 / fr for d3, fr in early_pairs) / len(early_pairs)
        if early_pairs else 0.0
    )))

    # ── Composite continuation strength ──────────────────────────────────────
    # Average of: efficiency, normalised 5D drift contribution, survival rate
    d5_norm = min(max((avg_d5 or 0.0) / 0.05 + 0.5, 0.0), 1.0)
    strength = (min(avg_eff, 1.0) + d5_norm + cont_surv) / 3.0

    return WindowMetrics(
        n=n,
        avg_mfe_pct=avg_mfe,
        avg_mae_pct=avg_mae,
        avg_final_return=avg_ret,
        avg_drift_1d=avg_d1,
        avg_drift_3d=avg_d3,
        avg_drift_5d=avg_d5,
        continuation_strength=strength,
        avg_mfe_efficiency=avg_eff,
        excursion_decay_rate=decay,
        drift_retention_quality=drift_ret,
        continuation_survival_pct=cont_surv,
        half_life_days=half_life,
        avg_holding_days=avg_hold,
        fast_breakout_pct=fast_brk,
        acceleration_score=accel,
        early_move_pct=early_move,
    )


# ──────────────────────────────────────────────────────────────────────────────
# Core engine
# ──────────────────────────────────────────────────────────────────────────────

class CQEEngine:
    """
    Continuation Quality Engine.

    Usage
    -----
    cqe = CQEEngine(enriched_trades)
    cqe.print_summary("Full 2018-2024")
    cqe.export_cqe_csv("cqe_metrics.csv", period_label="Full 2018-2024")
    cqe.export_regime_summary_csv("cqe_regime_summary.csv", period_label="Full 2018-2024")
    """

    def __init__(self, enriched_trades: list):
        # Filter out empty strategy labels for a cleaner per-strategy breakdown
        self.trades = sorted(enriched_trades, key=lambda t: t.entry_date)
        self._by_date: Dict[date, list] = defaultdict(list)
        for t in self.trades:
            self._by_date[t.entry_date.date()].append(t)
        self._trading_days: List[date] = sorted(self._by_date.keys())
        self._records: Optional[List[DailyCQERecord]] = None

    # ── Rolling record computation ────────────────────────────────────────────

    def compute_daily_records(self) -> List[DailyCQERecord]:
        if self._records is not None:
            return self._records

        records = []
        for i, day in enumerate(self._trading_days):
            window_10 = self._window(i, 10)
            window_20 = self._window(i, 20)

            m10 = _compute_window(window_10)
            m20 = _compute_window(window_20)

            morph10 = _classify_morphology(m10)
            morph20 = _classify_morphology(m20)
            state   = _cqe_state(m10, morph10)

            records.append(DailyCQERecord(
                date=day,
                window_1d_count=len(self._by_date[day]),
                window_10d_count=len(window_10),
                window_20d_count=len(window_20),
                m10=m10,
                m20_mfe_efficiency=m20.avg_mfe_efficiency,
                morphology_10d=morph10,
                morphology_20d=morph20,
                cqe_state=state,
                participation=_participation(state),
            ))

        self._records = records
        return records

    def _window(self, day_idx: int, n: int) -> list:
        start = max(0, day_idx - n + 1)
        out = []
        for d in self._trading_days[start:day_idx + 1]:
            out.extend(self._by_date[d])
        return out

    # ── Aggregates ───────────────────────────────────────────────────────────

    def period_metrics(self) -> WindowMetrics:
        """Period-level metrics across ALL trades."""
        return _compute_window(self.trades)

    def final_state(self) -> Optional[DailyCQERecord]:
        records = self.compute_daily_records()
        return records[-1] if records else None

    def dominant_morphology(self, window: int = 10) -> str:
        """Mode of daily morphology labels across the full period."""
        records = self.compute_daily_records()
        attr = "morphology_10d" if window <= 10 else "morphology_20d"
        morphs = [getattr(r, attr) for r in records]
        return max(set(morphs), key=morphs.count) if morphs else "weak_continuation"

    def per_strategy_metrics(self) -> Dict[str, WindowMetrics]:
        """Period-level metrics keyed by strategy name."""
        by_strat: Dict[str, list] = defaultdict(list)
        for t in self.trades:
            name = (t.strategy or "").strip() or "unknown"
            by_strat[name].append(t)
        return {s: _compute_window(ts) for s, ts in sorted(by_strat.items())}

    # ── Console summary ──────────────────────────────────────────────────────

    def print_summary(self, label: str = "") -> None:
        _print_summary(self, label)

    # ── CSV export ───────────────────────────────────────────────────────────

    def export_cqe_csv(self, path: str, period_label: str = "") -> None:
        records = self.compute_daily_records()
        if not records:
            return
        write_header = not os.path.exists(path) or os.path.getsize(path) == 0
        with open(path, "a", newline="") as f:
            w = csv.writer(f)
            if write_header:
                w.writerow([
                    "period", "date",
                    "n_1d", "n_10d", "n_20d",
                    # magnitude
                    "avg_final_return", "avg_drift_3d", "avg_drift_5d",
                    "continuation_strength",
                    # efficiency
                    "mfe_efficiency_10d", "mfe_efficiency_20d",
                    "excursion_decay_rate", "drift_retention_quality",
                    # persistence
                    "continuation_survival_pct", "half_life_days", "avg_holding_days",
                    # speed
                    "acceleration_score", "fast_breakout_pct", "early_move_pct",
                    # classification
                    "morphology_10d", "morphology_20d", "cqe_state", "participation",
                ])
            for r in records:
                m = r.m10

                def _f(v, d=4):
                    return f"{v:.{d}f}" if v is not None else "N/A"

                w.writerow([
                    period_label, r.date,
                    r.window_1d_count, r.window_10d_count, r.window_20d_count,
                    _f(m.avg_final_return), _f(m.avg_drift_3d), _f(m.avg_drift_5d),
                    _f(m.continuation_strength),
                    _f(m.avg_mfe_efficiency), _f(r.m20_mfe_efficiency),
                    _f(m.excursion_decay_rate), _f(m.drift_retention_quality),
                    _f(m.continuation_survival_pct), _f(m.half_life_days, 1),
                    _f(m.avg_holding_days, 1),
                    _f(m.acceleration_score), _f(m.fast_breakout_pct),
                    _f(m.early_move_pct),
                    r.morphology_10d, r.morphology_20d,
                    r.cqe_state, r.participation,
                ])

    def export_regime_summary_csv(self, path: str, period_label: str = "") -> None:
        records = self.compute_daily_records()
        if not records:
            return
        morph_counts: Dict[str, int] = defaultdict(int)
        state_counts: Dict[str, int] = defaultdict(int)
        for r in records:
            morph_counts[r.morphology_10d] += 1
            state_counts[r.cqe_state] += 1
        n_days = len(records)

        write_header = not os.path.exists(path) or os.path.getsize(path) == 0
        with open(path, "a", newline="") as f:
            w = csv.writer(f)
            if write_header:
                w.writerow([
                    "period",
                    "morphology", "morph_days", "morph_pct",
                    "cqe_state", "state_days", "state_pct",
                ])
            morphs = sorted(morph_counts.items(), key=lambda x: -x[1])
            states = sorted(state_counts.items())
            for i in range(max(len(morphs), len(states))):
                mo, mc = morphs[i] if i < len(morphs) else ("", "")
                st, sc = states[i] if i < len(states) else ("", "")
                w.writerow([
                    period_label,
                    mo, mc, f"{mc / n_days * 100:.1f}%" if mc else "",
                    st, sc, f"{sc / n_days * 100:.1f}%" if sc else "",
                ])


# ──────────────────────────────────────────────────────────────────────────────
# Console print
# ──────────────────────────────────────────────────────────────────────────────

_W = 66

_STATE_LABEL = {
    "HIGH_QUALITY":   "●●● HIGH_QUALITY",
    "MEDIUM_QUALITY": "●●○ MEDIUM_QUALITY",
    "LOW_QUALITY":    "●○○ LOW_QUALITY",
}
_PART_LABEL = {
    "FULL":      "■■■ FULL",
    "REDUCED":   "■■□ REDUCED",
    "DEFENSIVE": "■□□ DEFENSIVE",
}
_STATE_ABBREV = {
    "HIGH_QUALITY": "HIGH", "MEDIUM_QUALITY": "MED", "LOW_QUALITY": "LOW",
}


def _print_summary(engine: CQEEngine, label: str = "") -> None:
    m     = engine.period_metrics()
    fs    = engine.final_state()
    dom10 = engine.dominant_morphology(10)
    dom20 = engine.dominant_morphology(20)
    strat = engine.per_strategy_metrics()

    end_state = fs.cqe_state if fs else "UNKNOWN"
    end_part  = fs.participation if fs else "UNKNOWN"

    title = "CONTINUATION QUALITY ENGINE SUMMARY"
    if label:
        title += f"  [{label}]"

    def _pct(v):
        return f"{v * 100:>+7.2f}%" if v is not None else "    N/A"

    def _f(v, d=3):
        return f"{v:>{d + 4}.{d}f}" if v is not None else "    N/A"

    print(f"\n  {'═' * _W}")
    print(f"  {title}")
    print(f"  {'═' * _W}")
    print(f"  Trades analyzed: {m.n}")
    print(f"  {'─' * _W}")

    print(f"  Continuation Magnitude:")
    print(f"    Avg forward 3D drift    :{_pct(m.avg_drift_3d)}")
    print(f"    Avg forward 5D drift    :{_pct(m.avg_drift_5d)}")
    print(f"    Avg final return        :{_pct(m.avg_final_return)}")
    print(f"    Continuation strength   : {m.continuation_strength:>6.3f}  (0=none → 1=strong)")
    print(f"  {'─' * _W}")

    print(f"  Continuation Efficiency:")
    print(f"    Avg MFE efficiency      : {m.avg_mfe_efficiency:>6.3f}  (1.00=exit at peak)")
    print(f"    Excursion decay rate    : {m.excursion_decay_rate:>6.3f}  (lower=better retention)")
    print(f"    Drift retention quality : {m.drift_retention_quality:>6.3f}")
    print(f"  {'─' * _W}")

    print(f"  Drift Persistence:")
    print(f"    Continuation survival   : {m.continuation_survival_pct * 100:>6.1f}%  (% continued post-exit)")
    print(f"    Rolling half-life       : {m.half_life_days:>6.1f} days (median above entry)")
    print(f"    Avg hold duration       : {m.avg_holding_days:>6.1f} days")
    print(f"  {'─' * _W}")

    print(f"  Continuation Speed:")
    accel = (f"{m.acceleration_score:>6.3f}×  (>1=front-loaded, <1=delayed)"
             if m.acceleration_score is not None else "    N/A")
    print(f"    Acceleration score      : {accel}")
    print(f"    Fast breakout %         : {m.fast_breakout_pct * 100:>6.1f}%  (>1% move day-1 post-exit)")
    print(f"    Early move capture      : {m.early_move_pct:>6.3f}  (3D/final-return ratio)")
    print(f"  {'─' * _W}")

    print(f"  Dominant Morphology (10D) : {dom10}")
    print(f"  Dominant Morphology (20D) : {dom20}")
    print(f"  {'─' * _W}")
    print(f"  CQE State (end of period) : {_STATE_LABEL.get(end_state, end_state)}")
    print(f"  Recommended Participation : {_PART_LABEL.get(end_part, end_part)}")
    print(f"  {'─' * _W}")

    # Per-strategy breakdown — skip "unknown" if real strategies are present
    named = {k: v for k, v in strat.items() if k != "unknown"} or strat
    if named:
        print(f"  Per-strategy CQE:")
        print(f"    {'Strategy':<18} {'MFE_Eff':>8} {'Survival':>9} "
              f"{'Half-life':>10} {'Morphology':<24} State")
        print(f"    {'─' * 64}")
        for sname, sm in named.items():
            smorph = _classify_morphology(sm)
            sstate = _STATE_ABBREV.get(_cqe_state(sm, smorph), "?")
            print(
                f"    {sname:<18} "
                f"{sm.avg_mfe_efficiency:>8.3f} "
                f"{sm.continuation_survival_pct * 100:>8.1f}% "
                f"{sm.half_life_days:>9.1f}d "
                f"{smorph:<24} "
                f"{sstate}"
            )

    print(f"  {'═' * _W}")
