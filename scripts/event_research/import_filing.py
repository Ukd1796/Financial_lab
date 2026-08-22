"""Validate and optionally import one original NSE financial-result filing.

This script has no downloader by design.  Save the original attachment/XBRL,
normalise its fields into JSON, review the dry-run output, then pass --commit.
It never computes a score, forward return, or trading decision.

Usage:
  finance/bin/python3 -m scripts.event_research.import_filing \
      --payload sample.json --raw-file original-filing.html
  finance/bin/python3 -m scripts.event_research.import_filing \
      --payload sample.json --raw-file original-filing.html --commit
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from dotenv import load_dotenv


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--payload", required=True, type=Path)
    parser.add_argument("--raw-file", required=True, type=Path)
    parser.add_argument(
        "--raw-store", type=Path, default=Path("data/event_research/raw"),
        help="Content-addressed local archive for original filings (default: data/event_research/raw)",
    )
    parser.add_argument("--commit", action="store_true", help="Write the validated record to the research tables")
    args = parser.parse_args()

    try:
        payload = json.loads(args.payload.read_text())
    except (OSError, json.JSONDecodeError) as exc:
        raise SystemExit(f"Unable to read payload: {exc}") from exc

    from app.event_research.validation import archive_raw_filing, validate_filing_payload

    result = validate_filing_payload(payload, args.raw_file)
    print(json.dumps({
        "valid": result.is_valid,
        "errors": result.errors,
        "warnings": result.warnings,
        "source_sha256": result.normalized["event"]["raw_sha256"],
        "available_at": result.normalized["event"]["available_at"].isoformat()
        if result.normalized["event"]["available_at"] else None,
    }, indent=2))
    if not result.is_valid:
        raise SystemExit(2)
    if not args.commit:
        print("Dry run only. Review the source and re-run with --commit to persist it.")
        return

    try:
        archived = archive_raw_filing(
            args.raw_file, args.raw_store, result.normalized["event"]["raw_sha256"]
        )
    except (OSError, ValueError) as exc:
        raise SystemExit(f"Unable to archive original filing: {exc}") from exc
    result.normalized["event"]["raw_storage_path"] = str(archived)

    load_dotenv()
    from app.event_research.repository import EventResearchRepository

    event, created = EventResearchRepository().import_validated_filing(result.normalized)
    print(f"{'Imported' if created else 'Already present'} event {event.id}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(130)
