"""Ingest the pilot cohort's original NSE result filings.

For every cohort ISIN this retrieves the filings NSE disseminated inside the
requested window, archives each original document under its content hash, and
records the event with the exchange's own dissemination clock.

Three rules from the charter shape the behaviour:

* A filing whose facts cannot be proved from the document is still stored,
  with its parse status, and an exception is logged.  Events are never dropped
  because their data is inconvenient.
* Revisions never overwrite an original; they are linked by their predecessor's
  content hash.
* Nothing here reads prices or computes a surprise, response, score or return.

Usage:
  finance/bin/python3 -m scripts.event_research.fetch_cohort_filings \
      --cohort-id pilot-liquid-2018-12-31 --from 2019-01-01 --to 2019-06-30
  ... add --commit to persist.
"""

from __future__ import annotations

import argparse
import tempfile
from collections import Counter
from datetime import date, datetime
from pathlib import Path

from dotenv import load_dotenv

from app.event_research.nse_client import (
    NSEDocumentNotFound,
    NSEResearchClient,
    NSEUnavailable,
    parse_nse_timestamp,
)
from app.event_research.validation import archive_raw_filing, validate_filing_payload
from app.event_research.xbrl_parser import (
    VALIDATION_VALID,
    parse_result_xbrl,
    to_fact_payload,
)


def _parse_index_date(text: str | None) -> date | None:
    for fmt in ("%d-%b-%Y", "%d-%m-%Y"):
        try:
            return datetime.strptime((text or "").strip(), fmt).date()
        except ValueError:
            continue
    return None


# NSE writes a literal "-" in the xbrl column when a filing has no XBRL
# document.  It is a placeholder, not a URL, but it is truthy -- so a plain
# `if row["xbrl"]` builds ".../corporate/xbrl/-", fetches it, takes three 404s
# and logs a failure that never had a document behind it.  23 of the first 36
# recorded exceptions were this.
_NO_DOCUMENT_PLACEHOLDERS = {"", "-", "na", "n/a", "null", "none"}

# A run that loses the network should stop, not consume its whole plan.  On
# 2026-08-18 a closed lid took DNS away and the driver walked all seven legacy
# windows and 597 symbols failing every request, so a resumable job burned its
# entire schedule and recorded nothing.  Only transport/status failures count
# toward this -- a 404 is a real, permanent answer from a healthy connection.
MAX_CONSECUTIVE_FAILURES = 15


def document_url(row: dict) -> str | None:
    """The filing's XBRL URL, or None when NSE published no document.

    "No document was published" and "we could not fetch the document" are
    different facts and must not be counted as the same one.
    """
    value = (row.get("xbrl") or "").strip()
    if value.lower() in _NO_DOCUMENT_PLACEHOLDERS:
        return None
    return value


def ingested_source_urls() -> set[str]:
    """Source URLs already present, so a resumed run skips them before download."""
    from sqlalchemy import select

    from app.event_research.database import new_session
    from app.event_research.models import FinancialResultEvent

    session = new_session()
    try:
        return set(session.execute(select(FinancialResultEvent.source_url)).scalars().all())
    finally:
        session.close()


def _fiscal_quarter(period_end: date | None, relating_to: str | None) -> str:
    """Label the reported quarter, preferring NSE's own description."""
    mapping = {
        "first quarter": "Q1", "second quarter": "Q2",
        "third quarter": "Q3", "fourth quarter": "Q4",
    }
    label = mapping.get((relating_to or "").strip().lower())
    if label:
        return label
    if period_end is None:
        return "UNKNOWN"
    # Indian fiscal year starts in April.
    return {1: "Q4", 2: "Q1", 3: "Q2", 4: "Q3"}[(period_end.month - 1) // 3 + 1]


def build_payload(record: dict, cohort_member: dict, raw_path: Path) -> tuple[dict, object]:
    """Turn one NSE index record plus its document into an import payload."""
    period_start = _parse_index_date(record.get("fromDate"))
    period_end = _parse_index_date(record.get("toDate"))
    parse_result = parse_result_xbrl(
        raw_path, expected_period_start=period_start, expected_period_end=period_end
    )
    disseminated = parse_nse_timestamp(record.get("exchdisstime")) or parse_nse_timestamp(
        record.get("broadCastDate")
    )
    payload = {
        "event": {
            "isin": (record.get("isin") or "").upper(),
            "nse_symbol": (record.get("symbol") or "").upper(),
            "issuer_name": record.get("companyName") or cohort_member["fallback_name"],
            "instrument_valid_from": cohort_member["as_of_date"],
            "instrument_source_url": cohort_member["source_url"],
            "result_period_end": period_end.isoformat() if period_end else None,
            "fiscal_quarter": _fiscal_quarter(period_end, record.get("relatingTo")),
            "source_exchange": "NSE",
            "source_url": record.get("xbrl") or "",
            "source_format": "xbrl",
            "disseminated_at": disseminated.isoformat() if disseminated else None,
            "is_revision": False,
        },
        "facts": to_fact_payload(
            parse_result,
            reporting_scope="consolidated"
            if record.get("consolidated") == "Consolidated" else "standalone",
            is_cumulative=record.get("cumulative") != "Non-cumulative",
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
    parser.add_argument("--limit", type=int, default=None, help="Cap filings processed (smoke tests)")
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
        # Keyed on the **issuer prefix**, not the full ISIN: the result index
        # keeps quoting an ISIN that a face-value change retired years earlier
        # (NESTLEIND's 2025 filings still carry its pre-2024 code), so a
        # full-code join silently finds nothing for exactly the largest and
        # oldest issuers -- the same defect the cohort builder and the
        # corporate-action detector each hit.
        #
        # The snapshot table keys identity on ISIN and does not store a name,
        # so the symbol is only a fallback label when a filing omits one.
        # Later snapshots overwrite earlier ones, so an issuer carries its most
        # recent symbol and as-of date.
        cohort = {
            m.isin[:9]: {
                "fallback_name": m.nse_symbol,
                "symbol": m.nse_symbol,
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

    print(f"Fetching NSE result index {args.from_date} .. {args.to_date} ...")
    try:
        index = client.fetch_result_index(args.from_date, args.to_date)
    except NSEUnavailable as exc:
        raise SystemExit(f"Result index unavailable: {exc}")

    in_cohort = [r for r in index if (r.get("isin") or "").upper()[:9] in cohort]
    relevant = [r for r in in_cohort if document_url(r)]
    no_document = len(in_cohort) - len(relevant)
    print(f"  {len(index)} filings in window; {len(in_cohort)} belong to the cohort")
    if no_document:
        # Counted, not silently dropped: charter §6's missing-data gate wants
        # every absence visible, and this one is NSE's own "no XBRL" marker
        # rather than anything that went wrong at our end.
        print(f"  {no_document} carry no XBRL document (NSE placeholder), skipped before fetch")

    # Resume: a filing already ingested is skipped before it is downloaded.
    # `import_validated_filing` already no-ops on a duplicate content hash, but
    # that check happens *after* the document has been fetched, so without this
    # a restart re-downloads everything it already has.  Keyed on the source
    # URL, which is recorded on the event and known from the index alone.
    if not args.no_resume:
        already = ingested_source_urls()
        before = len(relevant)
        relevant = [r for r in relevant if r["xbrl"] not in already]
        if before != len(relevant):
            print(f"  resuming: {before - len(relevant)} already ingested, {len(relevant)} to fetch")

    if args.limit:
        relevant = relevant[: args.limit]

    statuses: Counter[str] = Counter()
    imported = duplicates = failed = 0
    consecutive_failures = 0
    with tempfile.TemporaryDirectory() as tmpdir:
        for position, record in enumerate(relevant, start=1):
            isin = (record.get("isin") or "").upper()
            url = record["xbrl"]
            try:
                blob = client.fetch_document(url)
            except NSEDocumentNotFound as exc:
                # NSE's index lists a document the archive no longer serves.
                # That is a permanent, factual absence and must not be filed as
                # a fetch failure -- "the exchange does not have it" and "we
                # could not get it" call for different responses, and conflating
                # them is how a retryable problem hides inside a coverage
                # statistic.  Retrying will never help.
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
                        "This is what a lost network looks like. Nothing is corrupted -- "
                        "re-run the same command once connectivity is back and resume will "
                        "skip everything already ingested."
                    )
                continue

            consecutive_failures = 0
            raw_path = Path(tmpdir) / f"filing_{position}.xml"
            raw_path.write_bytes(blob)
            payload, parse_result = build_payload(record, cohort[isin[:9]], raw_path)
            statuses[parse_result.validation_status] += 1

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

            # The document-level parse status is authoritative for the facts;
            # payload validation only checks the envelope around them.
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
                # See the integrated fetcher: an unlinkable revision is recorded,
                # not fatal.
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

    print("\nParse status across cohort filings:")
    for status, count in statuses.most_common():
        print(f"  {status}: {count}")
    if args.commit:
        print(f"\nImported {imported} new events; {duplicates} already present; {failed} failed")
    else:
        print(f"\nDry run only ({failed} would fail). Re-run with --commit to persist.")


if __name__ == "__main__":
    main()
