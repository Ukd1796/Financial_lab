"""Build the ex-ante pilot cohort from historical NSE bhavcopies.

The charter forbids selecting a historical cohort from today's index
membership.  This command instead reconstructs the cohort from the exchange's
own end-of-day records as they stood on a chosen past date: a security is
eligible only if it actually traded in the ``EQ`` series through the whole
lookback, and it is ranked on the traded value it genuinely printed then.
Names that later delisted or were renamed are therefore included on equal
terms, and no future information enters the selection.

Bhavcopy availability doubles as the point-in-time trading calendar, so no
holiday table is assumed for historical years.

The command writes a manifest CSV for ``import_pilot_manifest`` and computes
no return, score, or outcome of any kind.

Usage:
  finance/bin/python3 -m scripts.event_research.build_pilot_cohort \
      --as-of 2018-12-31 --lookback-sessions 60 --top 20 \
      --output data/event_research/pilot_manifest.csv
"""

from __future__ import annotations

import argparse
import csv
import statistics
from collections import defaultdict
from datetime import date, timedelta
from pathlib import Path

from app.event_research.nse_client import (
    BHAVCOPY_TEMPLATE,
    NSEDocumentNotFound,
    NSEResearchClient,
    NSEUnavailable,
)


MANIFEST_COLUMNS = (
    "cohort_id", "as_of_date", "isin", "nse_symbol", "issuer_name", "sector",
    "selection_reason", "source_url", "source_hash",
)
# A calendar-day ceiling so a long exchange closure cannot loop indefinitely.
_MAX_CALENDAR_LOOKBACK_DAYS = 400

# First nine characters identify the issuer; the last three the instrument.
ISIN_ISSUER_LENGTH = 9

# NSE's `bank` field on the filings index.  'B' = bank, 'F' = other financial,
# 'N' = neither.  Banks file to a different XBRL taxonomy, which is why the
# charter's Track A pilot specified non-financial issuers.
BANK_FLAGS = frozenset({"B"})
FINANCIAL_FLAGS = frozenset({"B", "F"})


def _bhavcopy_url(trade_date: date) -> str:
    return BHAVCOPY_TEMPLATE.format(
        year=trade_date.strftime("%Y"),
        month=trade_date.strftime("%b").upper(),
        day=trade_date.strftime("%d"),
    )


def collect_sessions_from_panel(
    db_path: Path, as_of: date, lookback_sessions: int
) -> tuple[list[date], list[dict[str, str]], list[str]]:
    """Read the lookback from the local NSE price panel instead of the network.

    The panel is the same exchange bhavcopy data already downloaded for the
    outcome variable, so a rolled cohort — one snapshot per quarter — costs
    nothing and is reproducible offline.  Rows are shaped to the legacy column
    names ``rank_liquid_universe`` expects, so the selection logic is shared
    with the network path rather than reimplemented beside it.

    Sessions are whatever the panel recorded as LOADED, which is the same
    point-in-time trading calendar the network path derives from bhavcopy
    availability.
    """
    import sqlite3

    if not db_path.exists():
        raise SystemExit(f"No price panel at {db_path}; run backfill_daily_prices first")

    connection = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
    try:
        sessions = [
            date.fromisoformat(s)
            for (s,) in connection.execute(
                "select session from price_sessions "
                "where exchange='NSE' and status='LOADED' and session <= ? "
                "order by session desc limit ?",
                (as_of.isoformat(), int(lookback_sessions)),
            )
        ]
        if len(sessions) < lookback_sessions:
            raise SystemExit(
                f"Panel holds only {len(sessions)} NSE sessions on or before {as_of}, "
                f"need {lookback_sessions}. Extend it with backfill_daily_prices "
                f"rather than shortening the liquidity rule."
            )
        wanted = {d.isoformat() for d in sessions}
        placeholders = ",".join("?" * len(wanted))
        rows = [
            {
                "SYMBOL": symbol,
                "SERIES": series,
                "ISIN": isin,
                "TOTTRDVAL": turnover,
                "_session": session,
            }
            for session, isin, symbol, series, turnover in connection.execute(
                "select session, isin, symbol, series, turnover from daily_prices "
                f"where exchange='NSE' and session in ({placeholders})",
                tuple(sorted(wanted)),
            )
        ]
        return sessions, rows, []
    finally:
        connection.close()


def collect_sessions(
    client: NSEResearchClient, as_of: date, lookback_sessions: int
) -> tuple[list[date], list[dict[str, str]], list[str]]:
    """Walk back from ``as_of`` collecting real trading sessions.

    Returns the session dates (newest first), their concatenated rows, and any
    non-404 retrieval failures, which are reported rather than silently
    treated as non-trading days.
    """
    sessions: list[date] = []
    rows: list[dict[str, str]] = []
    failures: list[str] = []
    cursor = as_of
    while len(sessions) < lookback_sessions and (as_of - cursor).days < _MAX_CALENDAR_LOOKBACK_DAYS:
        try:
            day_rows = client.fetch_bhavcopy(cursor)
        except NSEDocumentNotFound:
            pass  # No session that day (weekend or exchange holiday).
        except NSEUnavailable as exc:
            failures.append(f"{cursor}: {exc}")
        else:
            sessions.append(cursor)
            for row in day_rows:
                row["_session"] = cursor.isoformat()
            rows.extend(day_rows)
        cursor -= timedelta(days=1)
    return sessions, rows, failures


def rank_liquid_universe(
    rows: list[dict[str, str]], sessions: list[date], top: int
) -> tuple[list[dict], dict]:
    """Rank EQ-series securities by traded value over the collected sessions."""
    session_count = len(sessions)
    recent_20 = {d.isoformat() for d in sorted(sessions, reverse=True)[:20]}

    by_isin_values: dict[str, list[float]] = defaultdict(list)
    by_isin_values_20: dict[str, list[float]] = defaultdict(list)
    symbols: dict[str, str] = {}
    for row in rows:
        if row.get("SERIES") != "EQ":
            continue
        isin = (row.get("ISIN") or "").strip().upper()
        if not isin:
            continue
        try:
            traded_value = float(row.get("TOTTRDVAL") or 0.0)
        except ValueError:
            continue
        by_isin_values[isin].append(traded_value)
        if row.get("_session") in recent_20:
            by_isin_values_20[isin].append(traded_value)
        symbols[isin] = (row.get("SYMBOL") or "").strip().upper()

    # Continuous trading through the whole lookback is the ex-ante listing and
    # liquidity rule; a partially traded line is excluded and counted.
    continuous = {i: v for i, v in by_isin_values.items() if len(v) == session_count}
    ranked = sorted(
        (
            {
                "isin": isin,
                "nse_symbol": symbols[isin],
                "avg_daily_value_60d": statistics.fmean(values),
                "avg_daily_value_20d": (
                    statistics.fmean(by_isin_values_20[isin]) if by_isin_values_20.get(isin) else None
                ),
                "sessions_traded": len(values),
            }
            for isin, values in continuous.items()
        ),
        key=lambda entry: entry["avg_daily_value_60d"],
        reverse=True,
    )
    stats = {
        "sessions": session_count,
        "eq_securities_seen": len(by_isin_values),
        "traded_every_session": len(continuous),
        "selected": min(top, len(ranked)),
    }
    return ranked, stats


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--as-of", required=True, type=date.fromisoformat,
                        help="Cohort snapshot date; must precede the study window")
    parser.add_argument("--lookback-sessions", type=int, default=60)
    parser.add_argument("--top", type=int, default=20)
    parser.add_argument("--cohort-id", default=None,
                        help="Defaults to pilot-liquid-<as_of>")
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--name-window-days", type=int, default=120,
                        help="Days after --as-of searched for issuer names in NSE filings")
    parser.add_argument("--include-banks", action="store_true",
                        help="Keep issuers NSE flags as banks (excluded by default)")
    parser.add_argument("--exclude-financials", action="store_true",
                        help="Also exclude NSE's 'F' (non-bank financial) issuers")
    parser.add_argument("--issuer-flags", type=Path,
                        default=Path("data/event_research/issuer_flags.csv"),
                        help="Cached bank/financial classification; see build_issuer_flags")
    parser.add_argument("--request-delay", type=float, default=1.5)
    parser.add_argument("--from-panel", action="store_true",
                        help="Read the lookback from the local price panel instead of NSE")
    parser.add_argument("--panel-db", type=Path, default=Path("data/analysis/prices.sqlite"))
    args = parser.parse_args()

    cohort_id = args.cohort_id or f"pilot-liquid-{args.as_of.isoformat()}"
    client = NSEResearchClient(request_delay_seconds=args.request_delay)

    print(f"Collecting {args.lookback_sessions} sessions ending {args.as_of} ...")
    if args.from_panel:
        print(f"  source: local price panel {args.panel_db} (no network)")
        sessions, rows, failures = collect_sessions_from_panel(
            args.panel_db, args.as_of, args.lookback_sessions
        )
    else:
        sessions, rows, failures = collect_sessions(client, args.as_of, args.lookback_sessions)
    if len(sessions) < args.lookback_sessions:
        raise SystemExit(
            f"Only {len(sessions)} of {args.lookback_sessions} sessions retrieved; "
            f"failures={failures or 'none'}. Fix retrieval before selecting a cohort."
        )
    print(f"  sessions {sessions[-1]} .. {sessions[0]}")

    ranked, stats = rank_liquid_universe(rows, sessions, args.top)
    print(f"  EQ securities seen: {stats['eq_securities_seen']}, "
          f"traded every session: {stats['traded_every_session']}")

    # Issuer names and the bank flag come from NSE's own filing index just
    # after the snapshot: descriptive labelling, never a selection input.
    bank_flags = FINANCIAL_FLAGS if args.exclude_financials else BANK_FLAGS
    names: dict[str, str] = {}
    banks: set[str] = set()

    # The cached classification comes first and covers every fold.  Resolving
    # it live only works until ~Feb 2025, so a live-only rule would exclude
    # banks from fold A and none from folds B and C — three folds, two
    # different universes, and a §8 comparison that is not like-for-like.
    from scripts.event_research.build_issuer_flags import load_issuer_flags

    cached = load_issuer_flags(args.issuer_flags)
    if cached:
        print(f"Issuer flags: {len(cached)} cached from {args.issuer_flags}")
        for issuer, row in cached.items():
            if row.get("company_name"):
                names.setdefault(issuer, row["company_name"])
            if (row.get("bank_flag") or "").upper() in bank_flags:
                banks.add(issuer)
    else:
        print(f"! No issuer-flag cache at {args.issuer_flags} — bank exclusion will "
              f"apply only where this window's index resolves it, which makes the "
              f"universe rule differ across folds. Run build_issuer_flags.")

    print("Resolving issuer names from NSE filing index ...")
    try:
        index = client.fetch_result_index(args.as_of, args.as_of + timedelta(days=args.name_window_days))
    except NSEUnavailable as exc:
        raise SystemExit(f"Could not resolve issuer names: {exc}")
    # Keyed on the ISIN ISSUER PREFIX, never the full ISIN.  The bhavcopy and
    # the filings index disagree on the last three characters whenever a name
    # has had a face-value change: the panel carries the live instrument
    # (HDFCBANK INE040A01034) while the index still quotes the retired one
    # (INE040A01018), indefinitely — the same behaviour the corporate-action
    # work hit on NESTLEIND.  Matching on the full ISIN dropped 21 of the top
    # 60 by traded value, including HDFCBANK, SBIN, TATASTEEL and ONGC, and it
    # dropped them in proportion to how long a company has existed, which is a
    # size-correlated exclusion wearing a liquidity rule's clothes.
    for record in index:
        isin = (record.get("isin") or "").strip().upper()
        if not isin:
            continue
        issuer = isin[:ISIN_ISSUER_LENGTH]
        names.setdefault(issuer, (record.get("companyName") or "").strip())
        # NSE flags 'B' for banks and 'F' for other financials; 'Y' never
        # appears, so the previous check silently excluded nobody.
        if (record.get("bank") or "").upper() in bank_flags:
            banks.add(issuer)

    selected: list[dict] = []
    skipped_bank = 0
    unnamed = 0
    for entry in ranked:
        if len(selected) >= args.top:
            break
        issuer = entry["isin"][:ISIN_ISSUER_LENGTH]
        if not args.include_banks and issuer in banks:
            skipped_bank += 1
            continue
        # A missing issuer name does NOT exclude a member.  Eligibility is an
        # ex-ante liquidity and listing rule (charter §6); whether a name later
        # produced a parseable filing is a *coverage* fact to report, not a
        # selection input — using it here would define the universe by data
        # availability and quietly delete the members hardest to collect.
        # It also breaks on a schedule: the legacy filings index stops carrying
        # bulk rows after ~Feb 2025, which emptied every 2025+ cohort to one
        # member before this was fixed.
        issuer_name = names.get(issuer, "")
        if not issuer_name:
            unnamed += 1
        selected.append({
            "cohort_id": cohort_id,
            "as_of_date": args.as_of.isoformat(),
            "isin": entry["isin"],
            "nse_symbol": entry["nse_symbol"],
            "issuer_name": issuer_name,
            "sector": "",
            "selection_reason": (
                f"traded EQ every one of {stats['sessions']} sessions to {args.as_of}; "
                f"rank by mean daily traded value ({entry['avg_daily_value_60d']:.0f} INR)"
            ),
            "source_url": _bhavcopy_url(args.as_of),
            "source_hash": "",
        })

    if not selected:
        raise SystemExit("No cohort members survived the selection rules")

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=MANIFEST_COLUMNS)
        writer.writeheader()
        writer.writerows(selected)

    print(f"\nWrote {len(selected)} cohort members to {args.output}")
    print(f"  excluded as bank: {skipped_bank}")
    print(f"  kept without an issuer name (no filing found in window): {unnamed}"
          f" — descriptive gap, not a selection rule")
    print(f"  cohort_id: {cohort_id}")
    print("\nSector is intentionally blank: no point-in-time sector source is wired yet.")
    print("Next: download the as-of bhavcopy and commit the snapshot, e.g.")
    print(f"  curl -o cohort.zip '{_bhavcopy_url(args.as_of)}'")
    print(f"  finance/bin/python3 -m scripts.event_research.import_pilot_manifest \\")
    print(f"      --manifest {args.output} --source-file cohort.zip --commit")


if __name__ == "__main__":
    main()
