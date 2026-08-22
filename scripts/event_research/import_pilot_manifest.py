"""Validate and optionally import an ex-ante pilot-universe manifest.

The manifest must come from an archived report dated before the research
interval.  This command accepts no current-index shortcut and performs no
market-data or return lookup.
"""

from __future__ import annotations

import argparse
import csv
from datetime import date
from pathlib import Path
from urllib.parse import urlparse

from dotenv import load_dotenv

from app.event_research.validation import archive_raw_filing, sha256_file


# Eligibility inputs.  `issuer_name` is deliberately absent: it is a
# descriptive label, and `build_pilot_cohort` already treats it as one
# ("descriptive labelling, never a selection input").  Requiring it here
# rejected 188 of the 3,900 rolled-cohort rows, rising from 9 in 2023-06 to 29
# in 2026-06 because the legacy name index goes quiet after ~Feb 2025 -- an
# exclusion that correlates with issuer age and would have thinned exactly the
# later cohorts.  A missing name is recorded, not acted on.
REQUIRED = (
    "cohort_id", "as_of_date", "isin", "nse_symbol",
    "selection_reason", "source_url",
)

UNKNOWN_ISSUER_NAME = "UNKNOWN"


def _issuer_label(row: dict[str, str]) -> str:
    """The issuer's descriptive name, or UNKNOWN.

    `eligible_universe_snapshots` has no issuer-name column, so this value is
    reported and then discarded -- which is the whole point: the importer was
    rejecting rows over a field it does not store.
    """
    return (row.get("issuer_name") or "").strip() or UNKNOWN_ISSUER_NAME


def _normalise(row: dict[str, str], line: int) -> dict:
    missing = [field for field in REQUIRED if not (row.get(field) or "").strip()]
    if missing:
        raise ValueError(f"row {line}: missing {', '.join(missing)}")
    try:
        as_of_date = date.fromisoformat(row["as_of_date"])
    except ValueError as exc:
        raise ValueError(f"row {line}: as_of_date must be YYYY-MM-DD") from exc
    url = urlparse(row["source_url"])
    if url.scheme != "https" or not url.netloc:
        raise ValueError(f"row {line}: source_url must be https")
    return {
        "cohort_id": row["cohort_id"].strip(),
        "as_of_date": as_of_date,
        "isin": row["isin"].strip().upper(),
        "nse_symbol": row["nse_symbol"].strip().upper(),
        "sector": row.get("sector", "").strip() or None,
        "selection_reason": row["selection_reason"].strip(),
        "source_url": row["source_url"].strip(),
        "source_hash": row.get("source_hash", "").strip() or None,
        "listing_status": "ACTIVE",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--manifest", required=True, type=Path)
    parser.add_argument(
        "--source-file", type=Path,
        help="Original archived NSE cohort report; required with --commit",
    )
    parser.add_argument("--raw-store", type=Path, default=Path("data/event_research/raw"))
    parser.add_argument(
        "--panel-derived", action="store_true",
        help=(
            "The cohort was built by build_pilot_cohort --from-panel, so there is no "
            "single archived report to hash; provenance is the per-row bhavcopy URL"
        ),
    )
    parser.add_argument("--commit", action="store_true")
    args = parser.parse_args()
    with args.manifest.open(newline="") as handle:
        raw_rows = list(csv.DictReader(handle))
    rows = [_normalise(row, line) for line, row in enumerate(raw_rows, start=2)]
    if not rows:
        raise SystemExit("Manifest has no cohort rows")
    unnamed = sum(1 for row in raw_rows if _issuer_label(row) == UNKNOWN_ISSUER_NAME)
    if unnamed:
        # Reported so the gap stays visible, but never a reason to drop a member.
        print(f"{unnamed} of {len(rows)} members have no issuer name (recorded, not excluded)")
    cohort_dates = {(row["cohort_id"], row["as_of_date"]) for row in rows}
    if len(cohort_dates) != 1:
        raise SystemExit("Manifest must contain exactly one cohort_id/as_of_date snapshot")
    if len({row["isin"] for row in rows}) != len(rows):
        raise SystemExit("Manifest contains duplicate ISINs")
    print(f"Validated {len(rows)} manifest members for {next(iter(cohort_dates))}")
    if not args.commit:
        print("Dry run only. Re-run with --commit to persist the cohort snapshot.")
        return
    if args.panel_derived:
        if args.source_file is not None:
            raise SystemExit("--panel-derived and --source-file are mutually exclusive")
        # A panel-derived cohort has no single archived report behind it: it is
        # computed from many daily bhavcopies already verified in the price
        # panel, and each row carries the bhavcopy URL for its as-of date.
        # Recording a hash of something else would be worse than recording none,
        # so source_hash stays NULL and the per-row URL is the provenance.
        print("Panel-derived cohort: provenance is the per-row bhavcopy URL, source_hash NULL")
    else:
        if args.source_file is None:
            raise SystemExit("--source-file is required with --commit (or pass --panel-derived)")
        source_hash = sha256_file(args.source_file)
        for row in rows:
            declared = row["source_hash"]
            if declared and declared != source_hash:
                raise SystemExit("Manifest source_hash does not match --source-file")
            row["source_hash"] = source_hash
        archive_raw_filing(args.source_file, args.raw_store, source_hash)
    load_dotenv()
    from app.event_research.repository import EventResearchRepository

    repository = EventResearchRepository()
    added = sum(repository.import_universe_member(row) for row in rows)
    print(f"Imported {added} new members; {len(rows) - added} already existed")


if __name__ == "__main__":
    main()
