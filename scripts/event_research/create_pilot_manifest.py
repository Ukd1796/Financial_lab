"""Create an empty, historically dated pilot-manifest template.

The template intentionally contains no current Nifty constituents.  Populate it
only from an archived report whose date predates the research interval.

Usage:
  finance/bin/python3 -m scripts.event_research.create_pilot_manifest \
      --output data_cache/event_research/pilot_manifest.csv
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


HEADERS = [
    "cohort_id", "as_of_date", "isin", "nse_symbol", "issuer_name", "sector",
    "selection_reason", "source_url", "source_hash",
]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()

    if args.output.exists():
        raise SystemExit(f"Refusing to overwrite existing manifest: {args.output}")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=HEADERS)
        writer.writeheader()
    print(f"Created empty pilot manifest: {args.output}")
    print("Populate it from one archived, pre-research NSE cohort report. Do not use today's constituents.")


if __name__ == "__main__":
    main()
