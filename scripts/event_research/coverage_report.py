"""Print Phase-1 data coverage only; this command never reads prices or returns.

Usage:
  finance/bin/python3 -m scripts.event_research.coverage_report
  finance/bin/python3 -m scripts.event_research.coverage_report --cohort-id pilot-liquid-2018-12-31
"""

from __future__ import annotations

import argparse
import json

from dotenv import load_dotenv


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--cohort-id", default=None,
                        help="Also report how many cohort members produced no event at all")
    parser.add_argument("--json", action="store_true", help="Emit raw JSON instead of a table")
    args = parser.parse_args()

    load_dotenv()
    from app.event_research.repository import EventResearchRepository

    summary = EventResearchRepository().coverage_summary(cohort_id=args.cohort_id)
    if args.json:
        print(json.dumps(summary, indent=2))
        return

    print(f"Events stored        : {summary['events']}")
    print(f"Issuers with events  : {summary['issuers_with_events']}")
    if summary.get("cohort_members"):
        print(f"Cohort members       : {summary['cohort_members']} "
              f"({summary['cohort_members_without_events']} produced no event)")
    print(f"Exceptions logged    : {summary['exceptions']} {summary['exceptions_by_type'] or ''}")

    print("\nBy dissemination year")
    print(f"  {'year':<6}{'events':>8}{'primary':>9}{'usable':>8}{'usable%':>9}  statuses")
    for row in summary["by_year"]:
        eligible = row["primary_eligible"]
        usable = row["primary_with_eps"]
        share = f"{(usable / eligible * 100):.0f}%" if eligible else "-"
        print(f"  {row['year']:<6}{row['events']:>8}{eligible:>9}{usable:>8}{share:>9}  "
              f"{row['validation_status']}")
        if row["missing_available_at"]:
            print(f"    !! {row['missing_available_at']} events lack a dissemination timestamp")

    print("\nBy issuer (primary-eligible filings with a proved EPS)")
    for row in summary["by_issuer"]:
        flag = "  <-- no usable EPS" if row["primary_with_eps"] == 0 else ""
        print(f"  {row['nse_symbol']:<12}{row['isin']:<14}"
              f"events={row['events']:<4}usable={row['primary_with_eps']}{flag}")

    print("\n'primary' = original consolidated non-cumulative filings; 'usable' = those whose "
          "EPS was proved\nfrom the document. Coverage is reported before any outcome is computed.")


if __name__ == "__main__":
    main()
