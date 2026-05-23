"""
Opportunity Quality Engine (OQE)
---------------------------------
Computes signal quality and market opportunity metrics from enriched trades
and universe diagnostics.  Designed as a reusable standalone module — no
imports from backtest engine or strategy code.

Printed at the end of each backtest period in run_experiments.py.
"""

from __future__ import annotations

from typing import List, Optional


# ---------------------------------------------------------------------------
# Core computation
# ---------------------------------------------------------------------------

def compute_opportunity_quality_metrics(
    enriched_trades,
    universe_records=None,
) -> dict:
    """
    Compute all OQE metrics.

    Parameters
    ----------
    enriched_trades : list[EnrichedTrade]
    universe_records : list[DailyUniverseRecord], optional

    Returns
    -------
    dict with flat metrics + nested sub-dicts for continuation_decay and
    per-regime breakdowns.
    """
    if not enriched_trades:
        return {}

    n = len(enriched_trades)

    # ── Breakout quality ────────────────────────────────────────────────
    follow_through = sum(1 for t in enriched_trades if t.continuation_success)
    # False breakout: price initially moved > 2% in-trade (MFE > 2%)
    # but the final return was negative — promising setup that reversed.
    false_breakouts = sum(
        1 for t in enriched_trades
        if t.final_return_pct < 0 and t.mfe_pct > 0.02
    )
    breakout_follow_through_rate = follow_through / n
    false_breakout_rate          = false_breakouts / n

    # ── Persistence half-life: median breakout survival days ────────────
    survival = sorted(t.breakout_survival_days for t in enriched_trades)
    persistence_half_life = float(survival[len(survival) // 2]) if survival else 0.0

    # ── MFE efficiency ───────────────────────────────────────────────────
    effs = [
        t.mfe_efficiency
        for t in enriched_trades
        if -1.0 <= t.mfe_efficiency <= 2.0
    ]
    avg_mfe_efficiency = sum(effs) / len(effs) if effs else 0.0

    # ── Continuation decay curves ────────────────────────────────────────
    winners = [t for t in enriched_trades if t.final_return_pct > 0]
    losers  = [t for t in enriched_trades if t.final_return_pct <= 0]

    def _avg(trades, attr):
        vals = [getattr(t, attr) for t in trades if getattr(t, attr) is not None]
        return sum(vals) / len(vals) if vals else None

    continuation_decay = {
        "winner_drift_1d": _avg(winners, "drift_1d"),
        "winner_drift_3d": _avg(winners, "drift_3d"),
        "winner_drift_5d": _avg(winners, "drift_5d"),
        "loser_drift_1d":  _avg(losers,  "drift_1d"),
        "loser_drift_3d":  _avg(losers,  "drift_3d"),
        "loser_drift_5d":  _avg(losers,  "drift_5d"),
    }

    # ── Universe stability vs PnL / turnover vs success ─────────────────
    stability_vs_pnl_corr    = None
    turnover_vs_success_corr = None

    if universe_records:
        stab_by_date = {r.date.date(): r.stability_score     for r in universe_records}
        turn_by_date = {r.date.date(): r.daily_turnover_pct  for r in universe_records}

        pairs_stab, pairs_turn = [], []
        for t in enriched_trades:
            d = t.entry_date.date()
            if d in stab_by_date:
                pairs_stab.append((stab_by_date[d], t.pnl))
            if d in turn_by_date:
                pairs_turn.append((turn_by_date[d], int(t.continuation_success)))

        if len(pairs_stab) >= 10:
            stability_vs_pnl_corr = _pearson_r(
                [p[0] for p in pairs_stab],
                [p[1] for p in pairs_stab],
            )
        if len(pairs_turn) >= 10:
            turnover_vs_success_corr = _pearson_r(
                [p[0] for p in pairs_turn],
                [p[1] for p in pairs_turn],
            )

    # ── Per-regime breakdown ─────────────────────────────────────────────
    regime_breakdown = _regime_breakdown(enriched_trades)

    # ── Universe summary stats ───────────────────────────────────────────
    universe_summary = {}
    if universe_records:
        nd = len(universe_records)
        universe_summary = {
            "trading_days":            nd,
            "avg_stability_score":     sum(r.stability_score for r in universe_records) / nd,
            "avg_daily_turnover_pct":  sum(r.daily_turnover_pct for r in universe_records) / nd,
            "avg_leader_half_life":    sum(r.leader_half_life_days for r in universe_records) / nd,
        }

    return {
        "n_trades":                        n,
        "n_winners":                       len(winners),
        "n_losers":                        len(losers),
        "breakout_follow_through_rate":    breakout_follow_through_rate,
        "false_breakout_rate":             false_breakout_rate,
        "persistence_half_life_days":      persistence_half_life,
        "avg_mfe_efficiency":              avg_mfe_efficiency,
        "continuation_decay":              continuation_decay,
        "stability_vs_pnl_corr":           stability_vs_pnl_corr,
        "turnover_vs_success_corr":        turnover_vs_success_corr,
        "regime_breakdown":                regime_breakdown,
        "universe_summary":                universe_summary,
    }


def _regime_breakdown(enriched_trades) -> dict:
    """Win rate and avg return grouped by regime_at_entry."""
    buckets: dict[str, list] = {}
    for t in enriched_trades:
        key = t.regime_at_entry or "UNKNOWN"
        buckets.setdefault(key, [])
        buckets[key].append(t)

    result = {}
    for regime, trades in sorted(buckets.items()):
        n = len(trades)
        wins = sum(1 for t in trades if t.final_return_pct > 0)
        avg_ret = sum(t.final_return_pct for t in trades) / n
        result[regime] = {
            "n_trades":    n,
            "win_rate":    wins / n,
            "avg_return":  avg_ret,
        }
    return result


def _pearson_r(xs: list, ys: list) -> Optional[float]:
    n = len(xs)
    if n < 2:
        return None
    mx = sum(xs) / n
    my = sum(ys) / n
    num = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    dx  = (sum((x - mx) ** 2 for x in xs)) ** 0.5
    dy  = (sum((y - my) ** 2 for y in ys)) ** 0.5
    if dx < 1e-10 or dy < 1e-10:
        return None
    return num / (dx * dy)


# ---------------------------------------------------------------------------
# Print summary
# ---------------------------------------------------------------------------

_W = 66   # print width

def print_opportunity_quality_summary(
    metrics: dict,
    label: str = "",
    show_regime_breakdown: bool = True,
) -> None:
    """
    Print a formatted OPPORTUNITY QUALITY SUMMARY block.
    Printed after existing backtest metrics in run_experiments.py.
    """
    if not metrics:
        print(f"\n  {'─' * _W}")
        print(f"  OPPORTUNITY QUALITY SUMMARY — no trade data")
        print(f"  {'─' * _W}")
        return

    title = "OPPORTUNITY QUALITY SUMMARY"
    if label:
        title += f"  [{label}]"

    print(f"\n  {'═' * _W}")
    print(f"  {title}")
    print(f"  {'═' * _W}")

    n   = metrics["n_trades"]
    nw  = metrics["n_winners"]
    nl  = metrics["n_losers"]
    bfr = metrics["breakout_follow_through_rate"]
    fbr = metrics["false_breakout_rate"]
    phl = metrics["persistence_half_life_days"]
    eff = metrics["avg_mfe_efficiency"]

    print(f"  Trades analyzed  : {n}  ({nw} winners / {nl} losers)")
    print(f"  {'─' * _W}")
    print(f"  Breakout quality:")
    print(f"    Follow-through rate  : {bfr * 100:>6.1f}%   (price continued post-exit)")
    print(f"    False breakout rate  : {fbr * 100:>6.1f}%   (MFE>2% but final return <0)")
    print(f"    Persistence half-life: {phl:>6.1f} days (median survival above entry)")
    print(f"    Avg MFE efficiency   : {eff:>6.3f}      (1.00 = exit at peak)")
    print(f"  {'─' * _W}")

    # Continuation decay curves
    cd = metrics.get("continuation_decay", {})
    def _fmt(v):
        return f"{v * 100:>+7.2f}%" if v is not None else "    N/A"

    print(f"  Continuation decay (post-exit drift):")
    print(f"    {'':10}  {'1D':>8}  {'3D':>8}  {'5D':>8}")
    print(f"    Winners    {_fmt(cd.get('winner_drift_1d'))}  {_fmt(cd.get('winner_drift_3d'))}  {_fmt(cd.get('winner_drift_5d'))}")
    print(f"    Losers     {_fmt(cd.get('loser_drift_1d'))}  {_fmt(cd.get('loser_drift_3d'))}  {_fmt(cd.get('loser_drift_5d'))}")
    print(f"  {'─' * _W}")

    # Universe diagnostics
    us = metrics.get("universe_summary", {})
    if us:
        print(f"  Universe diagnostics ({us.get('trading_days', 0)} days):")
        print(f"    Avg stability score  : {us.get('avg_stability_score', 0):.3f}  (0=fully churning, 1=static)")
        print(f"    Avg daily turnover   : {us.get('avg_daily_turnover_pct', 0) * 100:.1f}%")
        print(f"    Avg leader half-life : {us.get('avg_leader_half_life', 0):.1f} days")

    corr_s = metrics.get("stability_vs_pnl_corr")
    corr_t = metrics.get("turnover_vs_success_corr")
    if corr_s is not None:
        print(f"    Stability vs PnL corr: {corr_s:>+.3f}  (>0 = stable universe → better trades)")
    if corr_t is not None:
        print(f"    Turnover vs success  : {corr_t:>+.3f}  (<0 = higher churn → fewer successes)")
    if us or corr_s is not None or corr_t is not None:
        print(f"  {'─' * _W}")

    # Per-regime breakdown
    regime_bd = metrics.get("regime_breakdown", {})
    if show_regime_breakdown and regime_bd:
        print(f"  Per-regime breakdown (entry regime):")
        print(f"    {'Regime':<28} {'N':>5} {'WinRate':>8} {'AvgRet':>9}")
        for regime, stats in sorted(regime_bd.items()):
            print(
                f"    {regime:<28} "
                f"{stats['n_trades']:>5} "
                f"{stats['win_rate'] * 100:>7.1f}% "
                f"{stats['avg_return'] * 100:>8.2f}%"
            )
        print(f"  {'─' * _W}")

    print(f"  {'═' * _W}")
