"""Backfill the daily NSE+BSE price panel — the V2 outcome variable.

Charter §8 is stated in 20-session sector-adjusted return; until this exists,
no result the study is designed to produce can be computed at all.

Resumable by design: every session is recorded in ``price_sessions`` as either
LOADED or NO_SESSION, so re-running downloads only what is missing.  Interrupt
it freely.

    finance/bin/python3 -m scripts.analysis.backfill_daily_prices \
        --start 2023-06-01 --end today

A weekend is skipped without a request.  A weekday absent from the archive is
recorded as NO_SESSION -- an exchange holiday -- but *only* when the client has
exhausted every known URL format, so an endpoint migration cannot be mistaken
for a market holiday (``docs/research_log.md`` 2026-08-12).
"""

from __future__ import annotations

import argparse
import sys
from datetime import date, datetime
from pathlib import Path

from app.analysis.prices import (
    BSE_UDIFF_FROM,
    STATUS_FAILED,
    STATUS_NO_SESSION,
    BSEClient,
    bse_rows_to_prices,
    connect,
    coverage,
    daterange,
    nse_rows_to_prices,
    recorded_sessions,
    store_session,
)
from app.event_research.nse_client import NSEDocumentNotFound, NSEResearchClient


def _parse_date(value: str) -> date:
    if value == "today":
        return date.today()
    return datetime.strptime(value, "%Y-%m-%d").date()


def run(
    start: date,
    end: date,
    *,
    db_path: Path,
    exchanges: list[str],
    stop_after_failures: int,
) -> int:
    conn = connect(db_path)
    clients: dict[str, object] = {}
    if "NSE" in exchanges:
        clients["NSE"] = NSEResearchClient()
    if "BSE" in exchanges:
        clients["BSE"] = BSEClient()

    already = {ex: recorded_sessions(conn, ex) for ex in exchanges}
    consecutive_failures = {ex: 0 for ex in exchanges}
    totals = {ex: {"loaded": 0, "no_session": 0, "failed": 0, "rows": 0} for ex in exchanges}

    # BSE answers dates before its UDiFF archive with HTTP 200 and an HTML
    # landing page.  Those requests cannot succeed, so they are not attempted --
    # recording them would either write false holidays into the trading calendar
    # or bury real failures under expected ones.
    earliest = {ex: start for ex in exchanges}
    if "BSE" in earliest and start < BSE_UDIFF_FROM:
        earliest["BSE"] = BSE_UDIFF_FROM
        print(
            f"NOTE: BSE archive begins {BSE_UDIFF_FROM}; "
            f"BSE will be skipped for {start} .. {BSE_UDIFF_FROM}. "
            "NSE covers that span alone."
        )

    # Every calendar day is attempted, weekends included.  NSE and BSE hold
    # occasional Saturday sessions -- Union Budget day (2025-02-01), disaster-
    # recovery drills (2024-01-20, 2024-05-18), muhurat trading -- and skipping
    # them silently corrupts three things at once: the trading calendar, the
    # length of any N-session window spanning one, and corporate-action
    # detection, which reads a missing session as a PREVCLOSE restatement for
    # every security that traded.  Weekend misses cost one cached NO_SESSION
    # marker each and are never re-fetched.
    sessions = list(daterange(start, end))
    print(
        f"Window {start} .. {end}: {len(sessions)} weekdays, "
        f"exchanges={','.join(exchanges)}, db={db_path}"
    )
    for exchange in exchanges:
        print(f"  {exchange}: {len(already[exchange])} sessions already recorded")

    # NSE is fetched first so its answer can arbitrate BSE's, below.
    ordered = sorted(exchanges, key=lambda e: e != "NSE")

    # NSE's verdict may come from this run or from a previous one.  Reading the
    # recorded status matters: on a resumed run NSE is skipped as already-known,
    # and without this BSE would lose its arbiter and fail every weekend.
    nse_recorded: dict[str, str] = {
        row["session"]: row["status"]
        for row in conn.execute(
            "SELECT session, status FROM price_sessions WHERE exchange = 'NSE'"
        )
    }

    for session in sessions:
        iso = session.isoformat()
        nse_verdict: str | None = nse_recorded.get(iso)
        for exchange in ordered:
            if iso in already[exchange] or session < earliest[exchange]:
                continue
            client = clients[exchange]
            try:
                rows = client.fetch_bhavcopy(session)  # type: ignore[attr-defined]
            except NSEDocumentNotFound:
                # Absence *is* information: no session that day.  Only reachable
                # after every URL candidate 404s.
                store_session(conn, exchange, session, [], status=STATUS_NO_SESSION)
                totals[exchange]["no_session"] += 1
                consecutive_failures[exchange] = 0
                if exchange == "NSE":
                    nse_verdict = STATUS_NO_SESSION
                continue
            except Exception as exc:  # noqa: BLE001 - recorded as FAILED, never as NO_SESSION
                # BSE cannot distinguish a holiday from a broken fetch: it
                # answers both with HTTP 200 and an HTML landing page.  NSE can
                # -- it 404s honestly -- and the two exchanges keep the same
                # holiday calendar, so NSE's silence is the evidence that turns
                # BSE's ambiguous answer into a holiday.  Without this every
                # weekend would count as a failure and trip the abort guard.
                if exchange == "BSE" and nse_verdict == STATUS_NO_SESSION:
                    store_session(
                        conn, exchange, session, [], status=STATUS_NO_SESSION,
                        note="NSE recorded no session on this date (exchange holiday)",
                    )
                    totals[exchange]["no_session"] += 1
                    consecutive_failures[exchange] = 0
                    continue
                store_session(
                    conn, exchange, session, [], status=STATUS_FAILED, note=str(exc)[:500]
                )
                totals[exchange]["failed"] += 1
                consecutive_failures[exchange] += 1
                print(f"  {iso} {exchange}: FAILED {exc}", flush=True)
                if consecutive_failures[exchange] >= stop_after_failures:
                    print(
                        f"\nAborting: {exchange} failed {stop_after_failures} sessions in a "
                        "row. That pattern is a migration or a block, not bad luck — "
                        "investigate before re-running.",
                        file=sys.stderr,
                    )
                    return 1
                continue

            prices = (
                nse_rows_to_prices(rows, session)
                if exchange == "NSE"
                else bse_rows_to_prices(rows, session)
            )
            stored = store_session(conn, exchange, session, prices)
            totals[exchange]["loaded"] += 1
            totals[exchange]["rows"] += stored
            consecutive_failures[exchange] = 0
            if exchange == "NSE":
                nse_verdict = "LOADED"
            if totals[exchange]["loaded"] % 20 == 0:
                print(
                    f"  {iso} {exchange}: {stored} rows "
                    f"({totals[exchange]['loaded']} sessions loaded)",
                    flush=True,
                )

    print("\n--- backfill summary ---")
    for exchange in exchanges:
        t = totals[exchange]
        print(
            f"{exchange}: loaded={t['loaded']} no_session={t['no_session']} "
            f"failed={t['failed']} rows={t['rows']:,}"
        )

    print("\n--- store coverage ---")
    for row in coverage(conn):
        print(
            f"{row['exchange']:<4} {row['status']:<11} sessions={row['sessions']:<5} "
            f"{row['first_session']} .. {row['last_session']}  rows={row['rows_stored'] or 0:,}"
        )
    return 0


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--start", type=_parse_date, default=_parse_date("2023-06-01"))
    parser.add_argument("--end", type=_parse_date, default=_parse_date("today"))
    parser.add_argument("--db", type=Path, default=Path("data/analysis/prices.sqlite"))
    parser.add_argument(
        "--exchanges",
        default="NSE,BSE",
        help="comma-separated; NSE alone is enough to start measuring returns",
    )
    parser.add_argument(
        "--stop-after-failures",
        type=int,
        default=10,
        help="abort after this many consecutive failures on one exchange",
    )
    args = parser.parse_args()

    exchanges = [e.strip().upper() for e in args.exchanges.split(",") if e.strip()]
    raise SystemExit(
        run(
            args.start,
            args.end,
            db_path=args.db,
            exchanges=exchanges,
            stop_after_failures=args.stop_after_failures,
        )
    )


if __name__ == "__main__":
    main()
