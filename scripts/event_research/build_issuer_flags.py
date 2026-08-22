"""Cache each issuer's NSE bank/financial classification, once, for every fold.

Why this exists as a separate artefact rather than a lookup inside the cohort
builder: the classification is only *available* in the legacy filings index,
which stops carrying bulk rows after ~Feb 2025 (docs/research_log.md,
2026-08-10).  Resolving it live therefore excludes ~25 banks per quarter in
2023-2024 and **zero** in 2025-2026 — folds A, B and C would be built from
different universes, and the fold comparison that charter §8 rests on would be
comparing a non-financial cohort against a mixed one.

Charter v3 rule (chosen 2026-08-14): resolve the flag once from the era where
it exists, key it on the ISIN issuer prefix, and apply it to every quarter.

What this does and does not assume.  Bank status is a *stable structural*
attribute, not an outcome: HDFCBANK is a bank in 2023 and in 2026, and nothing
about its future return is encoded in the flag.  That is what makes reusing a
later-resolved value acceptable here when it would not be for, say, a sector
weight or a fundamental ratio.  It is still not strictly point-in-time, which
is why unresolved issuers are recorded UNKNOWN and **kept**, never guessed —
an issuer that listed after the index went quiet is mostly a recent IPO, and
silently dropping it would reintroduce exactly the size- and age-correlated
exclusion that keying on the full ISIN already caused once.

    finance/bin/python3 -m scripts.event_research.build_issuer_flags \
        --from 2023-01-01 --to 2025-02-28 \
        --output data/event_research/issuer_flags.csv
"""

from __future__ import annotations

import argparse
import csv
from collections import Counter
from datetime import date, timedelta
from pathlib import Path

from app.event_research.nse_client import NSEResearchClient, NSEUnavailable

ISIN_ISSUER_LENGTH = 9
FLAG_COLUMNS = ("issuer_prefix", "bank_flag", "symbol", "company_name", "first_seen_window")

# NSE returns 'B' for banks, 'F' for other financials, 'N' for neither.  'Y'
# never appears — the original code tested for it and so excluded nobody.
KNOWN_FLAGS = frozenset({"B", "F", "N"})


def sweep(
    client: NSEResearchClient, start: date, end: date, window_days: int, log=print
) -> dict[str, dict[str, str]]:
    """Union the legacy index across consecutive windows.

    Windows rather than one huge request because the endpoint's response size
    is not documented; a silent truncation would look exactly like a market
    with fewer issuers in it.
    """
    flags: dict[str, dict[str, str]] = {}
    cursor = start
    while cursor <= end:
        window_end = min(cursor + timedelta(days=window_days), end)
        try:
            records = client.fetch_result_index(cursor, window_end)
        except NSEUnavailable as exc:
            log(f"  {cursor} .. {window_end}: UNAVAILABLE ({exc})")
            cursor = window_end + timedelta(days=1)
            continue

        added = 0
        for record in records:
            isin = (record.get("isin") or "").strip().upper()
            if not isin:
                continue
            issuer = isin[:ISIN_ISSUER_LENGTH]
            if issuer in flags:
                continue
            flag = (record.get("bank") or "").strip().upper()
            flags[issuer] = {
                "issuer_prefix": issuer,
                "bank_flag": flag if flag in KNOWN_FLAGS else "UNKNOWN",
                "symbol": (record.get("symbol") or "").strip().upper(),
                "company_name": (record.get("companyName") or "").strip(),
                "first_seen_window": f"{cursor}..{window_end}",
            }
            added += 1
        log(f"  {cursor} .. {window_end}: {len(records)} rows, {added} new issuers")
        cursor = window_end + timedelta(days=1)
    return flags


def load_issuer_flags(path: Path) -> dict[str, dict[str, str]]:
    """Read the cache; an absent file is not an error, it is 'nothing known'."""
    if not path.exists():
        return {}
    with path.open(newline="") as handle:
        return {row["issuer_prefix"]: row for row in csv.DictReader(handle)}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--from", dest="start", type=date.fromisoformat,
                        default=date(2023, 1, 1))
    parser.add_argument("--to", dest="end", type=date.fromisoformat,
                        default=date(2025, 2, 28),
                        help="Legacy index stops carrying bulk filings after ~Feb 2025")
    parser.add_argument("--window-days", type=int, default=120)
    parser.add_argument("--request-delay", type=float, default=1.0)
    parser.add_argument("--output", type=Path,
                        default=Path("data/event_research/issuer_flags.csv"))
    args = parser.parse_args()

    client = NSEResearchClient(request_delay_seconds=args.request_delay)
    print(f"Sweeping legacy filings index {args.start} .. {args.end}")
    flags = sweep(client, args.start, args.end, args.window_days)

    if not flags:
        raise SystemExit(
            "No issuers resolved. The legacy index returns nothing rather than "
            "erroring when it is deprecated, so treat an empty sweep as a "
            "suspected endpoint migration before trusting it."
        )

    counts = Counter(entry["bank_flag"] for entry in flags.values())
    print(f"\nIssuers resolved: {len(flags)}")
    for flag, count in counts.most_common():
        print(f"  {flag:<10}{count:>6}")

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FLAG_COLUMNS)
        writer.writeheader()
        for issuer in sorted(flags):
            writer.writerow(flags[issuer])
    print(f"\nWrote {args.output}")
    print("Pass it to build_pilot_cohort with --issuer-flags so every fold "
          "shares one universe rule.")


if __name__ == "__main__":
    main()
