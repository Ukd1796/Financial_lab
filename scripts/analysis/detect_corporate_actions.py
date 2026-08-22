"""Ingest NSE's announced corporate actions and validate them against prices.

The exchange does **not** restate PREVCLOSE on an ex-date, so actions cannot be
recovered from the price panel alone (see ``app/analysis/corporate_actions.py``
for the measurement that killed that approach).  They come from NSE's public
corporate-action feed instead: free, bulk, one request per window for the whole
market.

The headline number is the **agreement rate** between the announced ratio and
the price move actually observed on the ex-date.  Those are independent
systems, so agreement is the evidence that both the feed and our parse are
right; disagreements are printed rather than smoothed away.

    finance/bin/python3 -m scripts.analysis.detect_corporate_actions \
        --start 2023-06-01 --end today --commit
"""

from __future__ import annotations

import argparse
from collections import Counter
from datetime import date, datetime, timedelta
from pathlib import Path

from app.analysis.corporate_actions import (
    PRICE_SCALING_KINDS,
    ensure_schema,
    fetch_corporate_actions,
    store_actions,
    validate_against_prices,
)
from app.analysis.prices import connect
from app.event_research.nse_client import NSEResearchClient, NSEUnavailable


# The feed is windowed; NSE rejects very long spans, so it is walked in chunks.
WINDOW_DAYS = 30


def _parse_date(value: str) -> date:
    return date.today() if value == "today" else datetime.strptime(value, "%Y-%m-%d").date()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--start", type=_parse_date, default=_parse_date("2023-06-01"))
    parser.add_argument("--end", type=_parse_date, default=_parse_date("today"))
    parser.add_argument("--db", type=Path, default=Path("data/analysis/prices.sqlite"))
    parser.add_argument("--commit", action="store_true")
    args = parser.parse_args()

    conn = connect(args.db)
    ensure_schema(conn)
    client = NSEResearchClient()

    collected = []
    cursor = args.start
    while cursor <= args.end:
        window_end = min(cursor + timedelta(days=WINDOW_DAYS - 1), args.end)
        try:
            actions = fetch_corporate_actions(client, cursor, window_end)
        except NSEUnavailable as exc:
            print(f"  {cursor} .. {window_end}: unavailable ({exc})")
            cursor = window_end + timedelta(days=1)
            continue
        collected.extend(actions)
        print(f"  {cursor} .. {window_end}: {len(actions)} actions", flush=True)
        cursor = window_end + timedelta(days=1)

    # The feed repeats an action across overlapping windows; identity is the
    # primary key (isin, ex_date, subject).
    unique = {(a.isin, a.ex_date, a.subject): a for a in collected}
    print(f"\n{len(collected)} rows fetched, {len(unique)} unique actions")

    checked = validate_against_prices(conn, unique.values())

    kinds = Counter(a.kind for a in checked)
    print("\nBy kind:")
    for kind, count in kinds.most_common():
        print(f"  {kind:<16} {count:,}")

    scaling = [a for a in checked if a.kind in PRICE_SCALING_KINDS]
    verdicts = Counter(a.validation for a in scaling)
    print(f"\nPrice-scaling actions (the ones that matter): {len(scaling):,}")
    for verdict, count in verdicts.most_common():
        print(f"  {verdict:<16} {count:,}")
    comparable = verdicts["AGREE"] + verdicts["DISAGREE"]
    if comparable:
        print(f"  agreement rate : {verdicts['AGREE'] / comparable:.1%}")

    disagreements = [a for a in scaling if a.validation == "DISAGREE"]
    if disagreements:
        print("\nDisagreements (announced vs observed) — inspect, do not smooth:")
        for a in disagreements[:15]:
            print(
                f"  {a.symbol or a.isin:<14} {a.ex_date}  announced={a.announced_ratio:.4f} "
                f"observed={a.observed_ratio:.4f}  {a.subject[:52]}"
            )

    unparsed = [a for a in checked if a.kind == "UNPARSED"]
    if unparsed:
        print(f"\nUNPARSED subjects ({len(unparsed)}) — stored, not silently dropped:")
        for a in unparsed[:10]:
            print(f"  {a.symbol or a.isin:<14} {a.ex_date}  {a.subject[:70]}")

    if args.commit:
        stored = store_actions(conn, checked)
        print(f"\nStored {stored:,} actions")
    else:
        print("\nDry run. Re-run with --commit to persist.")


if __name__ == "__main__":
    main()
