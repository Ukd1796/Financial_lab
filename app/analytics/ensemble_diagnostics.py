# app/analytics/ensemble_diagnostics.py
#
# Ensemble-level participation and diversity metrics computed from
# MultiStrategyRouter.diag_counters and per-strategy universe filters.
#
# All functions are pure / post-hoc — no backtest behavior is affected.

import math


def compute_ensemble_metrics(diag_counters: dict) -> dict:
    """
    Compute ensemble-level participation and concentration metrics from
    MultiStrategyRouter.diag_counters.

    Returns
    -------
    dict with keys:
      participation_pct      : {strategy → won_merge / signals_issued}
      signal_passthrough_pct : {strategy → (won_merge - buy_rejected) / signals_issued}
      execution_entropy      : Shannon entropy of won_merge distribution (nats)
      router_concentration   : HHI of won_merge shares (0=fully distributed, 1=monopoly)
      total_issued           : sum of signals_issued across all strategies
      total_won              : sum of won_merge across all strategies
    """
    participation_pct      = {}
    signal_passthrough_pct = {}
    per_strategy_issued    = {}
    per_strategy_won       = {}

    for name, c in diag_counters.items():
        issued   = c.get("signals_issued", 0)
        won      = c.get("won_merge", 0)
        buy_rej  = c.get("buy_rejected", 0)
        survivors = max(won - buy_rej, 0)

        per_strategy_issued[name]    = issued
        per_strategy_won[name]       = won
        participation_pct[name]      = (won / issued) if issued > 0 else 0.0
        signal_passthrough_pct[name] = (survivors / issued) if issued > 0 else 0.0

    total_won = sum(c.get("won_merge", 0) for c in diag_counters.values())

    # Shannon entropy of won_merge distribution
    entropy = 0.0
    for c in diag_counters.values():
        won = c.get("won_merge", 0)
        if total_won > 0 and won > 0:
            p = won / total_won
            entropy -= p * math.log(p)

    # Herfindahl-Hirschman Index of won_merge shares
    hhi = sum(
        (c.get("won_merge", 0) / total_won) ** 2
        for c in diag_counters.values()
        if total_won > 0
    )

    return {
        "participation_pct":      participation_pct,
        "signal_passthrough_pct": signal_passthrough_pct,
        "per_strategy_issued":    per_strategy_issued,
        "per_strategy_won":       per_strategy_won,
        "execution_entropy":      round(entropy, 4),
        "router_concentration":   round(hhi, 4),
        "total_issued":           sum(per_strategy_issued.values()),
        "total_won":              total_won,
    }


def compute_universe_overlap(union_filter, broad_candidates, all_candidates=None) -> dict:
    """
    Measure per-strategy candidate set sizes and cross-strategy overlap.

    Parameters
    ----------
    union_filter    : UnionUniverseFilter instance
    broad_candidates: top-80 activity-biased candidates (from DynamicUniverseAgent)
    all_candidates  : full-150 candidates (from select_all_candidates); optional

    Returns
    -------
    dict with keys:
      per_strategy_count : {filter_idx → count} — number of candidates each filter selected
      unique_total       : total unique symbols across all filters
      diversity_score    : unique_total / sum(per_strategy_count) — 1.0 means no overlap
      overlap_pairs      : list of (filter_i, filter_j, overlap_count) for all pairs
    """
    full_pool = all_candidates if all_candidates is not None else broad_candidates

    filter_symbols: list[set] = []
    per_strategy_count: dict[int, int] = {}

    for i, f in enumerate(union_filter.filters):
        src = full_pool if getattr(f, "use_full_universe", False) else broad_candidates
        selected = {c.symbol for c in f.select_universe(src)}
        filter_symbols.append(selected)
        per_strategy_count[i] = len(selected)

    unique_total = len(set().union(*filter_symbols)) if filter_symbols else 0
    total_count  = sum(per_strategy_count.values())
    diversity    = (unique_total / total_count) if total_count > 0 else 0.0

    overlap_pairs = []
    n = len(filter_symbols)
    for i in range(n):
        for j in range(i + 1, n):
            overlap = len(filter_symbols[i] & filter_symbols[j])
            overlap_pairs.append((i, j, overlap))

    return {
        "per_strategy_count": per_strategy_count,
        "unique_total":       unique_total,
        "diversity_score":    round(diversity, 4),
        "overlap_pairs":      overlap_pairs,
    }


def print_ensemble_summary(
    metrics: dict,
    overlap: dict,
    period_label: str,
    strategy_names: list[str] | None = None,
) -> None:
    """Print a compact ensemble diagnostics summary."""
    divider = "  " + "-" * 70

    print(f"\n{divider}")
    print(f"  Ensemble Diagnostics — {period_label.strip()}")
    print(divider)

    # Participation table
    print(
        f"  {'Strategy':<12}"
        f"{'issued':>9}"
        f"{'won':>8}"
        f"{'particip%':>11}"
        f"{'pass-thru%':>12}"
    )
    for name, part_pct in metrics["participation_pct"].items():
        pass_pct = metrics["signal_passthrough_pct"].get(name, 0.0)
        issued   = metrics["per_strategy_issued"].get(name, 0)
        won      = metrics["per_strategy_won"].get(name, 0)
        print(
            f"  {name:<12}"
            f"{issued:>9}"
            f"{won:>8}"
            f"{part_pct * 100:>10.1f}%"
            f"{pass_pct * 100:>11.1f}%"
        )

    print(
        f"\n  Execution entropy : {metrics['execution_entropy']:.4f} nats"
        f"  (max={round(math.log(max(len(metrics['participation_pct']), 1)), 4)} for equal share)"
    )
    print(f"  Router concentration (HHI): {metrics['router_concentration']:.4f}"
          f"  (0=distributed · 1=monopoly)")

    # Universe overlap
    total = overlap["unique_total"]
    divers = overlap["diversity_score"]
    print(f"\n  Universe unique symbols : {total}")
    print(f"  Diversity score         : {divers:.4f}  (1.0 = zero overlap between filters)")
    if overlap["overlap_pairs"]:
        max_pair = max(overlap["overlap_pairs"], key=lambda x: x[2])
        print(f"  Highest pairwise overlap: filters {max_pair[0]}↔{max_pair[1]} "
              f"share {max_pair[2]} symbols")

    print(divider)
