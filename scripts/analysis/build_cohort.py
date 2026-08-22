"""Select the ingestion cohort from NSE bhavcopies. Costs zero indianapi calls.

Membership is reconstructed from the exchange's own end-of-day records rather
than from a current index list: a security qualifies only if it actually traded
in the ``EQ`` series through the whole lookback, and it is ranked on the traded
value it genuinely printed.  Names that later delist are therefore included on
equal terms.

Two jobs, not one.  The obvious one is picking which symbols to fetch.  The
second matters more later: a cohort built at two different dates is a
**delisting record**.  A symbol present in an older snapshot and absent from a
newer one stopped trading, with a date attached — and that is the outcome label
the red-flag work needs.  indianapi will never supply it; it simply stops
returning a company, undated.

The selection logic is shared with the event-research pilot
(``scripts/event_research/build_pilot_cohort.py``) so both lanes define
liquidity the same way.

Usage::

    PYTHONPATH=. finance/bin/python3 -m scripts.analysis.build_cohort \\
        --as-of 2026-08-08 --top 500 --output data/analysis/cohort_2026-08-08.csv
"""

from __future__ import annotations

import argparse
import csv
from datetime import date
from pathlib import Path

from dotenv import load_dotenv

from app.event_research.nse_client import NSEResearchClient
from scripts.event_research.build_pilot_cohort import collect_sessions, rank_liquid_universe

COLUMNS = ("cohort_id", "as_of_date", "rank", "symbol", "isin",
           "avg_daily_value_60d", "sessions_traded", "selection_reason")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--as-of", required=True, type=date.fromisoformat)
    parser.add_argument("--lookback-sessions", type=int, default=60)
    parser.add_argument("--top", type=int, default=500)
    parser.add_argument("--cohort-id", default=None, help="Defaults to liquid-<as_of>")
    parser.add_argument("--output", type=Path, default=None)
    parser.add_argument("--request-delay", type=float, default=1.5)
    parser.add_argument("--no-store", action="store_true",
                        help="Write the CSV only; skip the cohort_snapshots table")
    args = parser.parse_args()

    load_dotenv()

    cohort_id = args.cohort_id or f"liquid-{args.as_of.isoformat()}"
    output = args.output or Path(f"data/analysis/cohort_{args.as_of.isoformat()}.csv")

    client = NSEResearchClient(request_delay_seconds=args.request_delay)
    print(f"Collecting {args.lookback_sessions} sessions ending {args.as_of} ...")
    sessions, rows, failures = collect_sessions(client, args.as_of, args.lookback_sessions)
    if len(sessions) < args.lookback_sessions:
        raise SystemExit(
            f"Only {len(sessions)} of {args.lookback_sessions} sessions retrieved; "
            f"failures={failures or 'none'}. Fix retrieval before selecting a cohort — "
            "a short lookback silently changes who qualifies."
        )
    print(f"  sessions {sessions[-1]} .. {sessions[0]}")

    ranked, stats = rank_liquid_universe(rows, sessions, args.top)
    selected = ranked[: args.top]

    reason = (
        f"top {args.top} by mean daily traded value over {len(sessions)} sessions "
        f"ending {args.as_of.isoformat()}; EQ series, traded every session"
    )

    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=COLUMNS)
        writer.writeheader()
        for position, entry in enumerate(selected, start=1):
            writer.writerow({
                "cohort_id": cohort_id,
                "as_of_date": args.as_of.isoformat(),
                "rank": position,
                "symbol": entry["nse_symbol"],
                "isin": entry["isin"],
                "avg_daily_value_60d": f"{entry['avg_daily_value_60d']:.2f}",
                "sessions_traded": entry["sessions_traded"],
                "selection_reason": reason,
            })

    print(f"\nEQ securities seen   : {stats['eq_securities_seen']}")
    print(f"Traded every session : {stats['traded_every_session']}")
    print(f"Selected             : {len(selected)}")
    print(f"Wrote                : {output}")

    if not args.no_store:
        from app.analysis.database import initialize_schema
        from app.analysis.repository import AnalysisRepository

        initialize_schema()
        stored = AnalysisRepository().save_cohort(
            cohort_id,
            [
                {
                    "as_of_date": args.as_of,
                    "symbol": entry["nse_symbol"],
                    "isin": entry["isin"],
                    "rank": position,
                    "avg_daily_value_60d": entry["avg_daily_value_60d"],
                    "sessions_traded": entry["sessions_traded"],
                    "selection_reason": reason,
                }
                for position, entry in enumerate(selected, start=1)
            ],
        )
        print(f"Stored               : {stored} new rows in cohort_snapshots ({cohort_id})")

    print(
        "\nCommit the CSV: the cohort is a reproducible input, and comparing it "
        "against a later one is how delistings get their date."
    )


if __name__ == "__main__":
    main()
