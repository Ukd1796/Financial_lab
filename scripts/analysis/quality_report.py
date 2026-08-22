"""Report what the fundamentals feed actually delivers, before anything uses it.

This is the analysis layer's equivalent of
``scripts/event_research/coverage_report.py``: it measures the data and stops.
Coverage is reported before any metric is interpreted, so a thin or holed feed
is visible as a data problem rather than surfacing later as a weak result.

``--from-store`` reads what the backfill already fetched and therefore costs
**zero** API calls; without it the report queries the feed live and spends one
call per symbol.  Prefer the stored form for anything routine — a quota is
spent permanently, and re-reading data already on disk should never cost twice.

Usage::

    PYTHONPATH=. finance/bin/python3 -m scripts.analysis.quality_report \\
        --symbols RELIANCE.NS TCS.NS INFY.NS
    PYTHONPATH=. finance/bin/python3 -m scripts.analysis.quality_report \\
        --from-store --source indianapi
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

from app.analysis.fundamentals import (
    FIELDS,
    STATUS_VALID,
    FundamentalsSeries,
    load_series,
    normalise,
)
from app.analysis.metrics import latest_metrics
from app.analysis.sources import SOURCES, get_source

DEFAULT_SYMBOLS = [
    "RELIANCE.NS",
    "TCS.NS",
    "INFY.NS",
    "HINDUNILVR.NS",
    "ITC.NS",
    "LT.NS",
    "MARUTI.NS",
    "TATASTEEL.NS",
]


def load_from_store(symbol: str, stats: str = "quarter_results") -> FundamentalsSeries:
    """Rebuild a series from stored facts. Costs no API calls.

    The store keeps every vintage; :meth:`AnalysisRepository.series` resolves to
    the most recent one per period, so this reports the current view while the
    earlier vintages stay on disk as the restatement record.
    """
    from app.analysis.repository import AnalysisRepository

    rows = AnalysisRepository().series(symbol, stats)
    raw: dict = {}
    for row in rows:
        raw.setdefault(row["period_end"], {})[row["metric"]] = row["value"]

    retrieved = max((r["retrieved_at"] for r in rows), default=None)
    return normalise(
        symbol,
        raw,
        source="indianapi",
        is_point_in_time=False,
        retrieved_at=retrieved or datetime.now(timezone.utc),
    )


def describe(series: FundamentalsSeries) -> dict:
    metrics = latest_metrics(series)
    field_gaps = Counter()
    for quarter in series.quarters:
        field_gaps.update(quarter.missing_fields)

    return {
        "symbol": series.symbol,
        "status": series.status,
        "quarters": len(series.quarters),
        "first_period": str(series.quarters[0].period_end) if series.quarters else None,
        "last_period": str(series.latest.period_end) if series.latest else None,
        "missing_quarters": len(series.missing_buckets),
        "empty_quarters": len(series.empty_buckets),
        "unusable_quarters": len(series.unusable_buckets),
        "coverage": round(series.coverage, 3),
        "effective_coverage": round(series.effective_coverage, 3),
        "reported_fields": list(series.reported_fields),
        "point_in_time": series.is_point_in_time,
        "fields_never_reported": sorted(
            f for f in FIELDS if field_gaps[f] == len(series.quarters) and series.quarters
        ),
        "metrics_computable": sum(1 for m in metrics.values() if m.ok),
        "metrics_total": len(metrics),
        "metric_failures": {
            name: m.status for name, m in metrics.items() if not m.ok
        },
        "notes": list(series.notes),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--symbols", nargs="*", help="Ticker symbols, e.g. TCS.NS")
    parser.add_argument("--symbols-file", type=Path, help="One symbol per line")
    parser.add_argument("--json", type=Path, help="Write the full report here")
    parser.add_argument(
        "--source",
        default="yfinance",
        choices=sorted(SOURCES),
        help="Which feed to measure; the report is identical across sources",
    )
    parser.add_argument(
        "--from-store",
        action="store_true",
        help="Read stored facts instead of the network. Costs zero API calls.",
    )
    parser.add_argument("--stats", default="quarter_results",
                        help="Which stored vocabulary to report (with --from-store)")
    parser.add_argument("--cohort-id", help="Report this cohort's symbols (with --from-store)")
    args = parser.parse_args()

    symbols = list(args.symbols or [])
    if args.symbols_file:
        symbols += [
            line.strip()
            for line in args.symbols_file.read_text().splitlines()
            if line.strip() and not line.startswith("#")
        ]

    if args.from_store:
        from app.analysis.repository import AnalysisRepository

        repo = AnalysisRepository()
        if args.cohort_id:
            symbols += repo.cohort_symbols(args.cohort_id)
        if not symbols:
            symbols = repo.symbols_with_stats(args.stats)
        if not symbols:
            raise SystemExit(
                f"the store holds no {args.stats!r} facts yet — run "
                "scripts.analysis.backfill first"
            )
        rows = [describe(load_from_store(s, args.stats)) for s in symbols]
    else:
        symbols = symbols or DEFAULT_SYMBOLS
        source = get_source(args.source)
        rows = [describe(load_series(s, source)) for s in symbols]

    print(f"{'symbol':<16}{'status':<22}{'qtrs':>5}{'absent':>7}{'empty':>6}{'cover':>8}{'eff':>7}{'metrics':>9}")
    for r in rows:
        print(
            f"{r['symbol']:<16}{r['status']:<22}{r['quarters']:>5}"
            f"{r['missing_quarters']:>7}{r['empty_quarters']:>6}{r['coverage']:>8.0%}{r['effective_coverage']:>7.0%}"
            f"{r['metrics_computable']:>5}/{r['metrics_total']:<3}"
        )

    statuses = Counter(r["status"] for r in rows)
    usable = sum(1 for r in rows if r["status"] == STATUS_VALID)
    total_metrics = sum(r["metrics_total"] for r in rows)
    ok_metrics = sum(r["metrics_computable"] for r in rows)

    print(f"\nSource             : {args.source}")
    print(f"Symbols            : {len(rows)}")
    print(f"Unbroken series    : {usable} ({usable / len(rows):.0%})")
    print(f"Status breakdown   : {dict(statuses)}")
    print(f"Metrics computable : {ok_metrics}/{total_metrics}")
    depths = [r["quarters"] for r in rows if r["quarters"]]
    if depths:
        print(f"Quarters per symbol: min {min(depths)}, median "
              f"{sorted(depths)[len(depths) // 2]}, max {max(depths)}")

    failures = Counter()
    for r in rows:
        failures.update(r["metric_failures"].values())
    if failures:
        print(f"Metric failures    : {dict(failures)}")

    never = Counter()
    for r in rows:
        never.update(r["fields_never_reported"])
    if never:
        print(f"Fields never reported: {dict(never)}")

    if not any(r["point_in_time"] for r in rows):
        print(
            "\nSource is restated and carries no publication timestamps. "
            "Suitable for building and inspecting the analysis layer; "
            "not suitable for measuring a historical edge."
        )

    if args.from_store:
        from app.analysis.repository import AnalysisRepository

        repo = AnalysisRepository()
        summary = repo.coverage_summary()
        print("\nStore")
        print(f"  Snapshots (vintages) : {summary['snapshots']}")
        print(f"  Facts stored         : {summary['facts']}")
        if summary["exceptions"]:
            print(f"  Exceptions           : {dict((e['failure_type'], e['count']) for e in summary['exceptions'])}")

        print("\nSpend  (billed = reached the provider; reconcile against the dashboard)")
        print(f"  {'period':<10}{'endpoint':<28}{'billed':>8}{'cached':>8}")
        billed_total = 0
        for row in repo.spend_summary():
            billed_total += row["billed"]
            print(f"  {row['period']:<10}{row['endpoint']:<28}"
                  f"{row['billed']:>8}{row['cache_hits']:>8}")
        print(f"  {'':<38}{billed_total:>8}  total billed, all periods")
        print(f"\n  This report itself cost 0 calls (--from-store).")

    if args.json:
        args.json.write_text(json.dumps(rows, indent=2))
        print(f"\nWrote {args.json}")


if __name__ == "__main__":
    main()
