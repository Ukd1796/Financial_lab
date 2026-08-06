"""
Universe Stability Analytics — standalone extractor.

Runs ONLY the universe diagnostics layer (no strategies, no RiskAgent, no LLM).
Re-selects the universe on every trading day of each period and emits the full
stability metric set for the Universe Stability Thesis:

  Composition (per day)  → daily/weekly turnover, stability score, leader
                           half-life, promotions, demotions, universe entropy.
  Trajectory (per tenure)→ tenure days, entry/exit rank, rank slope, rank std,
                           entry/exit/min/max score, score volatility (std).

Reuses run_ujjwal_baseline's PeriodContext / OHLCCache / PERIODS / universe so
the diagnostic universe matches the traded universe exactly (broad-80 for
Breakout/QuietBrk + all-150 for TrendPB/RSI-MR/DualMA).

Usage:
  finance/bin/python3 -m scripts.run_universe_analytics
  finance/bin/python3 -m scripts.run_universe_analytics --period "Live"
  finance/bin/python3 -m scripts.run_universe_analytics --outdir docs/series

Outputs (appended, so delete first for a clean run):
  <outdir>/universe_daily_metrics.csv    — one row per (period, trading day)
  <outdir>/universe_trajectories.csv     — one row per (period, symbol tenure)
  <outdir>/universe_symbol_diagnostics.csv
  <outdir>/universe_boundary_metrics.csv
  <outdir>/universe_rank_delta_histogram.csv
  <outdir>/universe_eviction_attribution.csv
  <outdir>/universe_rank_persistence.csv
  <outdir>/universe_strategy_filter_diagnostics.csv
  + a per-period stability summary printed to console.
"""

import argparse
import os

from dotenv import load_dotenv
load_dotenv()

from run_ujjwal_baseline import (
    PeriodContext,
    OHLCCache,
    PERIODS,
    BROAD_UNIVERSE,
    MarketDataRepository,
)
from app.analytics.universe_tracker import compute_universe_diagnostics
from app.analytics.universe_diagnostics import compute_research_universe_diagnostics
from app.analytics.strategy_filter_diagnostics import compute_strategy_filter_diagnostics


def main():
    ap = argparse.ArgumentParser(description="Universe stability analytics extractor")
    ap.add_argument("--period", default=None,
                    help="Substring filter on period label (e.g. 'Live', 'Crash'). Default: all.")
    ap.add_argument("--outdir", default="docs/series",
                    help="Directory for CSV output (default: docs/series).")
    ap.add_argument("--fresh", action="store_true",
                    help="Delete existing CSVs before running (avoids append-stacking).")
    args = ap.parse_args()

    os.makedirs(args.outdir, exist_ok=True)
    daily_path = os.path.join(args.outdir, "universe_daily_metrics.csv")
    traj_path  = os.path.join(args.outdir, "universe_trajectories.csv")
    symbol_diag_path = os.path.join(args.outdir, "universe_symbol_diagnostics.csv")
    boundary_path = os.path.join(args.outdir, "universe_boundary_metrics.csv")
    rank_delta_path = os.path.join(args.outdir, "universe_rank_delta_histogram.csv")
    eviction_attr_path = os.path.join(args.outdir, "universe_eviction_attribution.csv")
    persistence_path = os.path.join(args.outdir, "universe_rank_persistence.csv")
    strategy_filter_path = os.path.join(args.outdir, "universe_strategy_filter_diagnostics.csv")
    if args.fresh:
        for p in (
            daily_path,
            traj_path,
            symbol_diag_path,
            boundary_path,
            rank_delta_path,
            eviction_attr_path,
            persistence_path,
            strategy_filter_path,
        ):
            if os.path.exists(p):
                os.remove(p)

    periods = {
        k: v for k, v in PERIODS.items()
        if args.period is None or args.period.lower() in k.lower()
    }
    if not periods:
        print(f"No period matched '{args.period}'. Available: {list(PERIODS.keys())}")
        return

    print("Warming OHLC cache ...")
    repository = OHLCCache(MarketDataRepository())
    repository.warm_all(BROAD_UNIVERSE)

    summary_rows = []
    for label, (start, end) in periods.items():
        lbl = label.strip()
        print(f"\n{'='*70}\n  Period: {lbl}   ({start.date()} → {end.date()})\n{'='*70}")
        ctx = PeriodContext(repository, start, end)
        tracker = compute_universe_diagnostics(ctx, ctx.universe_filter)
        tracker.print_summary(f"[{lbl}]")
        tracker.export_csv(daily_path, period_label=lbl, run_label="universe")
        tracker.export_trajectories_csv(traj_path, period_label=lbl, run_label="universe")
        why = compute_research_universe_diagnostics(ctx, ctx.universe_filter)
        why.print_summary(f"[{lbl}]")
        why.export_symbol_csv(symbol_diag_path, period_label=lbl, run_label="universe")
        why.export_boundary_csv(boundary_path, period_label=lbl, run_label="universe")
        why.export_rank_delta_histogram_csv(rank_delta_path, period_label=lbl, run_label="universe")
        why.export_eviction_attribution_csv(eviction_attr_path, period_label=lbl, run_label="universe")
        why.export_rank_persistence_csv(persistence_path, period_label=lbl, run_label="universe")
        strategy_filters = compute_strategy_filter_diagnostics(ctx, ctx.universe_filter)
        strategy_filters.print_summary(f"[{lbl}]")
        strategy_filters.export_csv(strategy_filter_path)
        s = tracker.summary_stats()
        s["period"] = lbl
        summary_rows.append(s)

    # Cross-period comparison table — the key view for the stability thesis.
    if summary_rows:
        print(f"\n{'='*100}\n  CROSS-PERIOD UNIVERSE STABILITY SUMMARY\n{'='*100}")
        hdr = (f"  {'Period':<16}{'Turn%':>7}{'Stab':>7}{'HalfLife':>9}"
               f"{'Promo':>7}{'Demo':>7}{'Entropy':>8}{'ScoreVol':>9}"
               f"{'RankVol':>8}{'RankSlp':>8}{'1dTen%':>8}")
        print(hdr)
        print(f"  {'-'*96}")
        for s in summary_rows:
            print(
                f"  {s['period']:<16}"
                f"{s['avg_daily_turnover_pct']*100:>6.1f}%"
                f"{s['avg_stability_score']:>7.3f}"
                f"{s['avg_leader_half_life_days']:>8.1f}d"
                f"{s['avg_promotions_per_day']:>7.1f}"
                f"{s['avg_demotions_per_day']:>7.1f}"
                f"{s['avg_universe_entropy']:>8.3f}"
                f"{s.get('avg_score_volatility', 0):>9.4f}"
                f"{s.get('avg_rank_volatility', 0):>8.2f}"
                f"{s.get('avg_rank_slope', 0):>+8.3f}"
                f"{s.get('pct_single_day_tenures', 0):>7.1f}%"
            )
        print(f"\n  Daily metrics  → {daily_path}")
        print(f"  Trajectories   → {traj_path}")
        print(f"  Symbol WHY     → {symbol_diag_path}")
        print(f"  Boundaries     → {boundary_path}")
        print(f"  Rank deltas    → {rank_delta_path}")
        print(f"  Evictions      → {eviction_attr_path}")
        print(f"  Persistence    → {persistence_path}")
        print(f"  Strategy gates → {strategy_filter_path}")


if __name__ == "__main__":
    main()
