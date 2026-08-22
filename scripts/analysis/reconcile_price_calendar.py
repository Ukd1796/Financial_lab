"""Resolve BSE sessions that failed, using NSE's calendar as the arbiter.

BSE answers a date it has no file for with **HTTP 200 and its HTML landing
page** rather than a 404, so the client cannot tell "exchange holiday" from
"archive does not reach here" from "something is broken".  It therefore records
every such response as ``FAILED`` -- deliberately the pessimistic reading, since
the alternative is writing phantom holidays into the trading calendar.

That leaves real holidays sitting in the store as failures.  This resolves them
with evidence rather than with the response shape:

* NSE also recorded ``NO_SESSION`` that day  -> a genuine market holiday.
  The two exchanges observe the same holiday calendar, and NSE *does* 404
  honestly, so its silence is trustworthy where BSE's is not.
* NSE recorded ``LOADED`` that day           -> **an anomaly.** The market was
  open and BSE served nothing. Reported, never auto-resolved.

Dry-run by default; pass ``--commit`` to write.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pathlib import Path

from app.analysis.prices import STATUS_FAILED, STATUS_NO_SESSION, connect


def reconcile(db_path: Path, *, commit: bool) -> int:
    conn = connect(db_path)
    rows = conn.execute(
        """
        SELECT bse.session      AS session,
               bse.note         AS note,
               nse.status       AS nse_status,
               nse.row_count    AS nse_rows
        FROM price_sessions bse
        LEFT JOIN price_sessions nse
               ON nse.session = bse.session AND nse.exchange = 'NSE'
        WHERE bse.exchange = 'BSE' AND bse.status = ?
        ORDER BY bse.session
        """,
        (STATUS_FAILED,),
    ).fetchall()

    holidays = [r for r in rows if r["nse_status"] == STATUS_NO_SESSION]
    anomalies = [r for r in rows if r["nse_status"] not in (STATUS_NO_SESSION, None)]
    unknown = [r for r in rows if r["nse_status"] is None]

    print(f"BSE sessions marked {STATUS_FAILED}: {len(rows)}")
    print(f"  NSE also had no session (holiday)     : {len(holidays)}")
    print(f"  NSE traded that day (ANOMALY)         : {len(anomalies)}")
    print(f"  NSE not recorded for that date        : {len(unknown)}")

    for row in anomalies:
        print(
            f"    ANOMALY {row['session']}: NSE {row['nse_status']} "
            f"({row['nse_rows']} rows) but BSE failed — {(row['note'] or '')[:90]}"
        )
    for row in unknown:
        print(f"    UNKNOWN {row['session']}: no NSE record to compare against")

    if not commit:
        print(f"\nDry run. {len(holidays)} session(s) would be reclassified as {STATUS_NO_SESSION}.")
        return 0

    now = datetime.now(timezone.utc).isoformat()
    with conn:
        conn.executemany(
            """
            UPDATE price_sessions
               SET status = ?, note = ?, fetched_at = ?
             WHERE exchange = 'BSE' AND session = ?
            """,
            [
                (
                    STATUS_NO_SESSION,
                    "reclassified: NSE recorded no session on this date (exchange holiday)",
                    now,
                    row["session"],
                )
                for row in holidays
            ],
        )
    print(f"\nReclassified {len(holidays)} BSE session(s) as {STATUS_NO_SESSION}.")
    if anomalies:
        print(
            f"{len(anomalies)} anomaly/anomalies left as {STATUS_FAILED} — "
            "these are not holidays and need investigating before the panel is trusted."
        )
    return 0


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--db", type=Path, default=Path("data/analysis/prices.sqlite"))
    parser.add_argument("--commit", action="store_true")
    args = parser.parse_args()
    raise SystemExit(reconcile(args.db, commit=args.commit))


if __name__ == "__main__":
    main()
