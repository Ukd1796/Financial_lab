"""Populate the traded-value columns the peer-basket rule reads.

`eligible_universe_snapshots` has carried `avg_daily_value_20d` and
`avg_daily_value_60d` since the Phase-1 schema, and nothing has ever written
them -- the cohort builder embedded the figure in the prose of
`selection_reason` instead.  Charter v3 §1 keys the peer basket on the 20-day
traded value, so it needs the number, not a sentence.

Both windows are measured **strictly at or before the snapshot's as-of date**,
from sessions already in the local panel, so the value is point-in-time by
construction and the backfill makes no network call.

Keyed on the issuer prefix: a face-value change mints a new ISIN, and the
snapshot may hold either side of one.

Usage:
  finance/bin/python3 -m scripts.event_research.backfill_cohort_liquidity --commit
"""

from __future__ import annotations

import argparse
import sqlite3
from pathlib import Path

from dotenv import load_dotenv

SHORT_WINDOW = 20
LONG_WINDOW = 60


def traded_value(
    conn: sqlite3.Connection, isin: str, as_of: str, sessions: int, *, exchange: str = "NSE"
) -> float | None:
    """Mean daily traded value over the N sessions ending at `as_of`.

    Turnover is summed per session first: an issuer trading under two codes
    across a face-value change would otherwise contribute two half-days.
    """
    rows = conn.execute(
        """
        SELECT SUM(turnover) FROM daily_prices
        WHERE exchange = ? AND substr(isin, 1, 9) = substr(?, 1, 9)
          AND series = 'EQ' AND session <= ?
        GROUP BY session
        ORDER BY session DESC
        LIMIT ?
        """,
        (exchange, isin, as_of, sessions),
    ).fetchall()
    values = [row[0] for row in rows if row[0] is not None]
    if len(values) < sessions:
        # Fewer sessions than the window means the issuer was not continuously
        # tradeable; report nothing rather than a mean over a short stub.
        return None
    return sum(values) / len(values)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--panel-db", type=Path, default=Path("data/analysis/prices.sqlite"))
    parser.add_argument("--cohort-like", default="liquid-%")
    parser.add_argument("--commit", action="store_true")
    args = parser.parse_args()

    load_dotenv()
    from sqlalchemy import select

    from app.event_research.database import new_session
    from app.event_research.models import EligibleUniverseSnapshot

    panel = sqlite3.connect(f"file:{args.panel_db}?mode=ro", uri=True)
    session = new_session()
    try:
        members = session.execute(
            select(EligibleUniverseSnapshot).where(
                EligibleUniverseSnapshot.cohort_id.like(args.cohort_like)
            )
        ).scalars().all()
        print(f"{len(members)} snapshot rows to price")

        resolved = missing_short = missing_long = 0
        for member in members:
            as_of = member.as_of_date.isoformat()
            short = traded_value(panel, member.isin, as_of, SHORT_WINDOW)
            long = traded_value(panel, member.isin, as_of, LONG_WINDOW)
            member.avg_daily_value_20d = short
            member.avg_daily_value_60d = long
            resolved += 1
            missing_short += short is None
            missing_long += long is None

        print(f"  {resolved - missing_short} of {resolved} have a {SHORT_WINDOW}-session value")
        print(f"  {resolved - missing_long} of {resolved} have a {LONG_WINDOW}-session value")
        if missing_short:
            print(f"  {missing_short} lack a full {SHORT_WINDOW}-session history (recorded NULL)")

        if args.commit:
            session.commit()
            print("Committed.")
        else:
            session.rollback()
            print("Dry run only. Re-run with --commit to persist.")
    finally:
        session.close()
        panel.close()


if __name__ == "__main__":
    main()
