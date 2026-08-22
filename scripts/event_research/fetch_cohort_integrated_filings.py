"""Ingest cohort result filings from NSE's Integrated Filing endpoint.

The legacy result index stops carrying bulk filings after ~Feb 2025
(``docs/research_log.md`` 2026-08-10), which left fold B (2025) and the forward
run with no source.  This is the replacement path.

Two findings from the 2026-08-14 probe shape it:

* **No iXBRL parser is needed.** The endpoint advertises an ``ixbrl`` link but
  also publishes a plain ``xbrl`` document, and the existing Phase-1 parser
  reads it unchanged -- same ``OneD`` context convention, VALID first try.
* **``symbol`` filters server-side**, so a cohort costs one index request per
  member instead of a walk over ~29,000 market-wide rows.

Same charter rules as the legacy fetcher: unprovable filings are still stored
with their parse status and an exception, revisions never overwrite originals,
and nothing here reads prices or computes a surprise, response or return.

Usage:
  finance/bin/python3 -m scripts.event_research.fetch_cohort_integrated_filings \
      --cohort-id pilot-liquid-2018-12-31 --from 2025-01-01 --to 2026-08-14
  ... add --commit to persist.
"""

from __future__ import annotations

import argparse
import tempfile
from collections import Counter
from datetime import date
from pathlib import Path

from dotenv import load_dotenv

from app.event_research.nse_client import (
    NSEDocumentNotFound,
    NSEResearchClient,
    NSEUnavailable,
    normalise_integrated_filing_row,
    parse_nse_timestamp,
)
from app.event_research.validation import archive_raw_filing, validate_filing_payload
from app.event_research.xbrl_parser import (
    VALIDATION_VALID,
    parse_result_xbrl,
    to_fact_payload,
)
from scripts.event_research.fetch_cohort_filings import (
    MAX_CONSECUTIVE_FAILURES,
    _fiscal_quarter,
    _parse_index_date,
    document_url,
    ingested_source_urls,
)


# A discrete quarter is ~3 months.  Anything materially longer is a cumulative
# year-to-date period.  Derived from the document's own resolved context rather
# than defaulted, because the legacy caller's default (anything that is not
# "Non-cumulative" is cumulative) would mark every integrated filing cumulative
# and silently exclude the whole 2025+ era from seasonal chaining.
_DISCRETE_PERIOD_MAX_DAYS = 115


def _is_cumulative(parse_result) -> bool | None:
    if parse_result.period_start is None or parse_result.period_end is None:
        return None
    span = (parse_result.period_end - parse_result.period_start).days
    return span > _DISCRETE_PERIOD_MAX_DAYS


def find_superseded_sha256(isin: str, period_end: str | None, scope: str) -> str | None:
    """The content hash of the original filing a revision replaces.

    The charter requires a revision to point at its predecessor rather than
    overwrite it, so the original's as-filed numbers stay recoverable -- that
    original is what the market actually traded on, and it is the only version
    admissible for a point-in-time study.

    Matched on issuer, reported period and reporting scope: a company files
    standalone and consolidated results separately, and a revision to one is
    not a revision to the other.
    """
    if not period_end:
        return None
    from sqlalchemy import select

    from app.event_research.database import new_session
    from app.event_research.models import (
        EventResearchInstrument,
        FinancialResultEvent,
        FinancialResultFact,
    )

    session = new_session()
    try:
        row = session.execute(
            select(FinancialResultEvent.source_sha256)
            .join(
                EventResearchInstrument,
                EventResearchInstrument.id == FinancialResultEvent.instrument_id,
            )
            .join(
                FinancialResultFact,
                FinancialResultFact.event_id == FinancialResultEvent.id,
            )
            .where(
                EventResearchInstrument.isin == isin.upper(),
                FinancialResultEvent.result_period_end == date.fromisoformat(period_end),
                FinancialResultFact.reporting_scope == scope,
                FinancialResultEvent.is_revision.is_(False),
            )
            .order_by(FinancialResultEvent.disseminated_at.desc())
        ).scalars().first()
        return row
    finally:
        session.close()


def build_payload(record: dict, cohort_member: dict, raw_path: Path) -> tuple[dict, object]:
    period_end = _parse_index_date(record.get("toDate"))
    # No period start is published here; the document is the stronger source and
    # the parser resolves the period from it.
    parse_result = parse_result_xbrl(raw_path, expected_period_end=period_end)
    disseminated = parse_nse_timestamp(record.get("exchdisstime"))

    cumulative = _is_cumulative(parse_result)
    payload = {
        "event": {
            "isin": (record.get("isin") or "").upper(),
            "nse_symbol": (record.get("symbol") or "").upper(),
            "issuer_name": record.get("companyName") or cohort_member["fallback_name"],
            "instrument_valid_from": cohort_member["as_of_date"],
            "instrument_source_url": cohort_member["source_url"],
            "result_period_end": period_end.isoformat() if period_end else None,
            "fiscal_quarter": _fiscal_quarter(period_end, None),
            "source_exchange": "NSE",
            "source_url": record.get("xbrl") or "",
            "source_format": "xbrl",
            "disseminated_at": disseminated.isoformat() if disseminated else None,
            "is_revision": bool(record.get("isRevision")),
            "supersedes_source_sha256": (
                find_superseded_sha256(
                    record.get("isin") or "",
                    period_end.isoformat() if period_end else None,
                    "consolidated"
                    if record.get("consolidated") == "Consolidated" else "standalone",
                )
                if record.get("isRevision") else None
            ),
        },
        "facts": to_fact_payload(
            parse_result,
            reporting_scope="consolidated"
            if record.get("consolidated") == "Consolidated" else "standalone",
            # An unresolvable period means the span is unknown; treating it as
            # discrete would be a guess, so it inherits the conservative flag
            # and the filing is already carrying a non-VALID parse status.
            is_cumulative=True if cumulative is None else cumulative,
            audit_status=(record.get("audited") or "UNKNOWN").replace("-", "").upper(),
        ),
    }
    return payload, parse_result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument(
        "--cohort-id", required=True, nargs="+",
        help="One or more cohort ids; the union is fetched in a single pass",
    )
    parser.add_argument("--from", dest="from_date", required=True, type=date.fromisoformat)
    parser.add_argument("--to", dest="to_date", required=True, type=date.fromisoformat)
    parser.add_argument("--raw-store", type=Path, default=Path("data/event_research/raw"))
    parser.add_argument("--request-delay", type=float, default=1.5)
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument(
        "--no-resume", action="store_true",
        help="Re-fetch filings already ingested (default is to skip them)",
    )
    parser.add_argument("--commit", action="store_true")
    args = parser.parse_args()

    load_dotenv()
    from sqlalchemy import select

    from app.event_research.database import new_session
    from app.event_research.models import EligibleUniverseSnapshot
    from app.event_research.repository import EventResearchRepository

    session = new_session()
    try:
        members = session.execute(
            select(EligibleUniverseSnapshot)
            .where(EligibleUniverseSnapshot.cohort_id.in_(args.cohort_id))
            .order_by(EligibleUniverseSnapshot.as_of_date)
        ).scalars().all()
        # Keyed on the issuer prefix so an issuer whose face value changed
        # mid-window is fetched once, under its latest ISIN and symbol, rather
        # than twice under codes the endpoint may no longer recognise.
        cohort = {
            m.isin[:9]: {
                "isin": m.isin,
                "symbol": m.nse_symbol,
                "fallback_name": m.nse_symbol,
                "as_of_date": m.as_of_date.isoformat(),
                "source_url": m.source_url,
            }
            for m in members
        }
    finally:
        session.close()

    if not cohort:
        raise SystemExit(
            f"Cohort {', '.join(args.cohort_id)} has no members; build and import it first"
        )
    print(f"Cohort {', '.join(args.cohort_id)}: {len(cohort)} issuers ({len(members)} snapshot rows)")

    client = NSEResearchClient(request_delay_seconds=args.request_delay)
    repository = EventResearchRepository()

    print(f"Fetching integrated filing index {args.from_date} .. {args.to_date} (per symbol) ...")
    relevant: list[tuple[str, dict]] = []
    index_failures = 0
    for prefix, member in cohort.items():
        symbol = member["symbol"]
        try:
            rows = client.fetch_integrated_filing_index(
                args.from_date, args.to_date, symbol=symbol
            )
        except NSEUnavailable as exc:
            print(f"  ! {symbol}: index unavailable ({exc})")
            index_failures += 1
            if index_failures >= MAX_CONSECUTIVE_FAILURES:
                raise SystemExit(
                    f"\nAborting: {index_failures} consecutive index failures.\n"
                    f"  last error: {exc}\n"
                    "Re-run once connectivity is back; resume skips what is ingested."
                )
            continue
        index_failures = 0
        # The full ISIN, not the prefix key: this value is stored on the event
        # and must remain a real instrument identifier.
        normalised = [
            normalise_integrated_filing_row(r, isin=member["isin"]) for r in rows
        ]
        # Governance filings share the endpoint and parse to a valid period but
        # carry no EPS or revenue.  They are counted, not silently dropped --
        # they are the half-yearly balance-sheet/cash-flow source the charter
        # defers to V2.1.
        financial = [r for r in normalised if r.get("isFinancialResult")]
        results = [r for r in financial if document_url(r)]
        no_document = len(financial) - len(results)
        governance = sum(1 for r in normalised if not r.get("isFinancialResult"))
        print(
            f"  {symbol:<12} {len(rows):>3} filings, {len(results):>3} financial results, "
            f"{governance:>3} governance (skipped)"
            + (f", {no_document} with no XBRL" if no_document else "")
        )
        relevant.extend((prefix, r) for r in results)

    # Originals first: a revision can only be linked once its predecessor is
    # stored, and both can arrive in the same run.
    relevant.sort(key=lambda pair: bool(pair[1].get("isRevision")))

    # Resume before downloading, not after: the duplicate-hash check inside
    # import_validated_filing only fires once the document is already fetched.
    if not args.no_resume:
        already = ingested_source_urls()
        before = len(relevant)
        relevant = [pair for pair in relevant if pair[1]["xbrl"] not in already]
        if before != len(relevant):
            print(f"\nResuming: {before - len(relevant)} already ingested")

    if args.limit:
        relevant = relevant[: args.limit]
    print(f"\n{len(relevant)} cohort filings to process")

    statuses: Counter[str] = Counter()
    scopes: Counter[str] = Counter()
    imported = duplicates = failed = 0
    consecutive_failures = 0
    with tempfile.TemporaryDirectory() as tmpdir:
        for position, (prefix, record) in enumerate(relevant, start=1):
            url = record["xbrl"]
            try:
                blob = client.fetch_document(url)
            except NSEDocumentNotFound as exc:
                # A permanent absence in the archive, not a failure on our side.
                statuses["DOCUMENT_ABSENT"] += 1
                failed += 1
                if args.commit:
                    repository.record_exception(
                        source_url=url, exception_type="DOCUMENT_ABSENT", details=str(exc)
                    )
                continue
            except NSEUnavailable as exc:
                statuses["FETCH_FAILED"] += 1
                failed += 1
                consecutive_failures += 1
                if args.commit:
                    repository.record_exception(
                        source_url=url, exception_type="FETCH_FAILED", details=str(exc)
                    )
                if consecutive_failures >= MAX_CONSECUTIVE_FAILURES:
                    raise SystemExit(
                        f"\nAborting: {consecutive_failures} consecutive fetch failures.\n"
                        f"  last error: {exc}\n"
                        "Re-run once connectivity is back; resume skips what is ingested."
                    )
                continue
            consecutive_failures = 0

            raw_path = Path(tmpdir) / f"integrated_{position}.xml"
            raw_path.write_bytes(blob)
            payload, parse_result = build_payload(record, cohort[prefix], raw_path)
            statuses[parse_result.validation_status] += 1
            scopes[
                f"{payload['facts']['reporting_scope']}/"
                f"{'cumulative' if payload['facts']['is_cumulative'] else 'discrete'}"
            ] += 1

            result = validate_filing_payload(payload, raw_path)
            if not result.is_valid:
                failed += 1
                print(f"  ! {record.get('symbol')} {record.get('toDate')}: {'; '.join(result.errors)}")
                if args.commit:
                    repository.record_exception(
                        source_url=url,
                        exception_type="PAYLOAD_INVALID",
                        details="; ".join(result.errors),
                    )
                continue

            result.normalized["facts"]["validation_status"] = payload["facts"]["validation_status"]
            result.normalized["facts"]["validation_notes"] = payload["facts"]["validation_notes"]

            if not args.commit:
                continue

            archived = archive_raw_filing(
                raw_path, args.raw_store, result.normalized["event"]["raw_sha256"]
            )
            result.normalized["event"]["raw_storage_path"] = str(archived)
            try:
                _event, created = repository.import_validated_filing(result.normalized)
            except ValueError as exc:
                # A revision whose original is not in the corpus -- the original
                # may sit outside this window, or have carried no XBRL.  The
                # charter's rule is that an inconvenient filing is recorded with
                # its problem, never dropped and never fatal; letting this
                # propagate aborted an entire 7,056-filing run over one row.
                statuses["REVISION_PREDECESSOR_MISSING"] += 1
                failed += 1
                repository.record_exception(
                    source_url=url,
                    exception_type="REVISION_PREDECESSOR_MISSING",
                    details=str(exc),
                )
                continue
            imported += created
            duplicates += 0 if created else 1
            if parse_result.validation_status != VALIDATION_VALID:
                repository.record_exception(
                    source_url=url,
                    exception_type=parse_result.validation_status,
                    details="; ".join(parse_result.notes),
                )

    print("\nParse status:")
    for status, count in statuses.most_common():
        print(f"  {status}: {count}")
    print("\nScope / period shape:")
    for scope, count in scopes.most_common():
        print(f"  {scope}: {count}")
    if args.commit:
        print(f"\nImported {imported} new events; {duplicates} already present; {failed} failed")
    else:
        print(f"\nDry run only ({failed} would fail). Re-run with --commit to persist.")


if __name__ == "__main__":
    main()
