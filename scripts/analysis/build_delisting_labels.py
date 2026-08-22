"""Label every ISIN's fate from NSE bhavcopies. Zero vendor API calls.

This is the outcome half of the dataset.  The feature side (indianapi) can only
describe companies that still exist; a failed one is simply absent from it, so a
red-flag model trained on the vendor alone would never see a single failure.
Here the exit date comes from the last session a security actually traded, and
the price path into that session says whether the exit was a collapse or a
buyout — measured, not looked up.

It also answers OQ5 ("how big is survivorship bias, quantitatively?"), open in
docs/research_log.md since 2026-08-06.

Downloads are cached, so re-running with a different threshold costs nothing —
which is the point: a free re-run removes any incentive to settle for the first
cut of the thresholds.

Usage::

    PYTHONPATH=. finance/bin/python3 -m scripts.analysis.build_delisting_labels \\
        --start 2018-01-01 --end 2026-08-11
    PYTHONPATH=. finance/bin/python3 -m scripts.analysis.build_delisting_labels \\
        --start 2018-01-01 --end 2026-08-11 --csv data/analysis/outcomes.csv
"""

from __future__ import annotations

import argparse
import csv
from collections import Counter
from datetime import date
from pathlib import Path

from dotenv import load_dotenv

from app.analysis.delisting import (
    COLLAPSE_DRAWDOWN,
    LISTING_ABSENT,
    LISTING_UNCHECKED,
    STATUS_ACTIVE,
    STATUS_EXIT_AFTER_COLLAPSE,
    STATUS_INSTRUMENT_CHANGED,
    CachedBhavcopyClient,
    annotate_listed_elsewhere,
    build_outcomes,
    collect_monthly_snapshots,
    month_ends,
)

CSV_COLUMNS = (
    "isin", "symbol", "status", "listed_elsewhere", "first_seen", "last_seen",
    "months_observed", "gap_months", "last_close", "close_12m_before", "return_12m",
    "return_6m", "peak_close", "drawdown_from_peak", "notes",
)

# One recent BSE snapshot answers "is it still alive somewhere", which is the
# question mortality asks.  A trailing window rather than a single session, so
# an illiquid name that simply did not trade on the reference day is not read
# as dead.
BSE_LOOKBACK_DAYS = 30


def bse_listed_isins(db_path: Path, lookback_days: int = BSE_LOOKBACK_DAYS) -> set[str] | None:
    """ISINs seen trading on BSE in the most recent window of the price panel.

    Returns ``None`` when the panel is unavailable, so the caller leaves rows
    UNCHECKED rather than silently labelling every exit ABSENT — a missing file
    must never manufacture 646 confirmed deaths.
    """
    import sqlite3

    if not db_path.exists():
        return None
    connection = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
    try:
        latest = connection.execute(
            "select max(session) from price_sessions where exchange='BSE' and status='LOADED'"
        ).fetchone()[0]
        if not latest:
            return None
        rows = connection.execute(
            "select distinct isin from daily_prices "
            "where exchange='BSE' and session >= date(?, ?)",
            (latest, f"-{int(lookback_days)} day"),
        )
        return {isin for (isin,) in rows if isin}
    finally:
        connection.close()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--start", required=True, type=date.fromisoformat)
    parser.add_argument("--end", required=True, type=date.fromisoformat)
    parser.add_argument("--collapse-drawdown", type=float, default=COLLAPSE_DRAWDOWN,
                        help="Fall from lifetime peak at or below which an exit is a collapse")
    parser.add_argument("--csv", type=Path, help="Also write the full table here")
    parser.add_argument("--cache-dir", default="data/analysis/bhavcopy")
    parser.add_argument("--bse-prices", type=Path, default=Path("data/analysis/prices.sqlite"),
                        help="Price panel used to test BSE listing survival")
    parser.add_argument("--no-bse", action="store_true",
                        help="Skip the BSE check; every exit stays UNCHECKED")
    parser.add_argument("--request-delay", type=float, default=0.8)
    parser.add_argument("--no-store", action="store_true")
    args = parser.parse_args()

    load_dotenv()

    from app.analysis.database import initialize_schema
    from app.analysis.repository import AnalysisRepository
    from app.event_research.nse_client import NSEResearchClient

    months = month_ends(args.start, args.end)
    print(f"Window        : {args.start} .. {args.end}  ({len(months)} monthly samples)")
    print(f"Cache         : {args.cache_dir}\n")

    client = CachedBhavcopyClient(
        NSEResearchClient(request_delay_seconds=args.request_delay), args.cache_dir
    )
    snapshots = collect_monthly_snapshots(client, args.start, args.end, log=print)

    if not snapshots:
        raise SystemExit(
            "No bhavcopies retrieved. NSE deprecates endpoints by deleting files "
            "rather than erroring, so treat this as a suspected format migration "
            "and verify the URL against a known-good recent date before rerunning."
        )

    print(f"\nSnapshots     : {len(snapshots)} of {len(months)} months")
    print(f"Downloaded    : {client.downloads}   (cache hits {client.cache_hits})")

    outcomes = build_outcomes(snapshots, collapse_drawdown=args.collapse_drawdown)

    # Charter amendment v2 §4: delisted means absent from NSE *and* BSE.  Read
    # from the local price panel, so this costs nothing and needs no network.
    reference = None if args.no_bse else bse_listed_isins(args.bse_prices)
    if reference is None and not args.no_bse:
        print(f"\n! No BSE panel at {args.bse_prices} — listing survival left UNCHECKED")
    outcomes = annotate_listed_elsewhere(outcomes, reference)

    counts = Counter(o.status for o in outcomes)
    total = len(outcomes)
    # An ISIN that stops while a sibling instrument of the same issuer keeps
    # trading is a face-value change, not an exit; counting it would overstate
    # survivorship by half.
    exits = total - counts[STATUS_ACTIVE] - counts[STATUS_INSTRUMENT_CHANGED]

    print(f"\nISINs observed: {total}")
    print(f"{'status':<24}{'count':>7}{'of all':>9}{'of exits':>10}")
    for status, count in counts.most_common():
        counted = status not in (STATUS_ACTIVE, STATUS_INSTRUMENT_CHANGED)
        share_exits = f"{count / exits:>9.0%}" if exits and counted else " " * 9
        print(f"{status:<24}{count:>7}{count / total:>9.0%}{share_exits}")

    changed = counts[STATUS_INSTRUMENT_CHANGED]
    print(f"\nInstrument chg: {changed} ISINs retired while the issuer kept trading "
          f"(face-value change or split) — NOT deaths")
    print(f"Survivorship  : {exits} of {total} ISINs ({exits / total:.0%}) genuinely stopped "
          f"trading inside the window")
    collapses = counts[STATUS_EXIT_AFTER_COLLAPSE]
    if exits:
        print(f"                of those exits, {collapses} ({collapses / exits:.0%}) died "
              f"{args.collapse_drawdown:.0%} or more below their lifetime peak — the "
              f"population a red-flag screen must catch")

    listing = Counter(o.listed_elsewhere for o in outcomes if o.status.startswith("EXIT"))
    if listing and listing.get(LISTING_UNCHECKED, 0) != exits:
        gone = listing.get(LISTING_ABSENT, 0)
        print(f"\nListing survival of those {exits} NSE exits (charter amendment v2 §4)")
        for value, count in listing.most_common():
            print(f"  {value:<16}{count:>6}{count / exits:>7.0%}")
        print(f"  -> {gone} ({gone / exits:.0%}) are absent from NSE and BSE: genuinely delisted")
        # The two dimensions disagree on purpose, and that disagreement is the
        # finding: a name can be a total loss and still be quoted daily.
        survived = [
            o for o in outcomes
            if o.status == STATUS_EXIT_AFTER_COLLAPSE and o.listed_elsewhere != LISTING_ABSENT
        ]
        if survived:
            print(f"\n  {len(survived)} of {collapses} collapses still trade elsewhere — "
                  f"the loss was real, the death was not:")
            print("   ", ", ".join(sorted(o.symbol for o in survived)[:10]), "...")

    worst = sorted(
        (o for o in outcomes
         if o.status == STATUS_EXIT_AFTER_COLLAPSE and o.drawdown_from_peak is not None),
        key=lambda o: o.drawdown_from_peak,
    )[:15]
    if worst:
        print("\nWorst exits by fall from lifetime peak (split-adjusted)")
        print(f"  {'symbol':<14}{'last seen':<12}{'peak DD':>9}{'ret 12m':>9}")
        for o in worst:
            r12 = f"{o.return_12m:>8.0%}" if o.return_12m is not None else "        -"
            print(f"  {o.symbol:<14}{str(o.last_seen):<12}{o.drawdown_from_peak:>8.0%}{r12:>9}")

    if args.csv:
        args.csv.parent.mkdir(parents=True, exist_ok=True)
        with args.csv.open("w", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=CSV_COLUMNS)
            writer.writeheader()
            for o in outcomes:
                writer.writerow({c: getattr(o, c) for c in CSV_COLUMNS})
        print(f"\nWrote {args.csv}")

    if not args.no_store:
        initialize_schema()
        stored = AnalysisRepository().save_outcomes(
            outcomes, window_start=args.start, window_end=args.end
        )
        print(f"Stored {stored} new outcome rows (existing rows for this window updated)")

    print(
        "\nLabels use fall from lifetime peak on a split-adjusted series. Both the "
        "drawdown and the trailing returns are stored per row, so re-thresholding "
        "either one is a re-run with no downloads."
    )


if __name__ == "__main__":
    main()
