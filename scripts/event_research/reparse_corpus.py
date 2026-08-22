"""Re-derive facts from the archived documents under one parser rule.

The raw filing is immutable and archived under its content hash; the *facts*
are a derived view of it, which is why `parser_version` is stored per fact.
Re-parsing therefore corrects a derivation without touching a source document,
and it is the only way to guarantee the whole corpus was read under a single
rule -- a corpus half-parsed under two conventions is worse than one parsed
strictly, because the inconsistency is invisible downstream.

Run this AFTER all fetching, never during.

Usage:
  finance/bin/python3 -m scripts.event_research.reparse_corpus --resolve-conventions
  ... add --commit to persist.
"""

from __future__ import annotations

import argparse
from collections import Counter
from pathlib import Path

from dotenv import load_dotenv

from app.event_research.xbrl_parser import parse_result_xbrl


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument(
        "--resolve-conventions", action="store_true",
        help="Recover an undefined OneD/FourD pair from the document's own values",
    )
    parser.add_argument("--commit", action="store_true")
    args = parser.parse_args()

    load_dotenv()
    from sqlalchemy import select

    from app.event_research.database import new_session
    from app.event_research.models import FinancialResultEvent, FinancialResultFact

    session = new_session()
    try:
        rows = session.execute(
            select(FinancialResultEvent, FinancialResultFact)
            .join(FinancialResultFact, FinancialResultFact.event_id == FinancialResultEvent.id)
        ).all()
        print(f"{len(rows)} filings to re-parse "
              f"(resolve_conventions={args.resolve_conventions})")

        transitions: Counter[str] = Counter()
        eps_changed = missing = 0
        for event, fact in rows:
            path = Path(event.raw_storage_path)
            if not path.exists():
                missing += 1
                continue
            result = parse_result_xbrl(
                path,
                expected_period_end=event.result_period_end,
                resolve_conventions=args.resolve_conventions,
            )
            before, after = fact.validation_status, result.validation_status
            if before != after:
                transitions[f"{before} -> {after}"] += 1

            new_eps = result.facts.get("basic_eps")
            if (fact.basic_eps is None) != (new_eps is None) or (
                fact.basic_eps is not None and new_eps is not None
                and abs(fact.basic_eps - new_eps) > 1e-9
            ):
                eps_changed += 1

            if args.commit:
                fact.validation_status = after
                fact.validation_notes = "; ".join(result.notes) or None
                for name, value in result.facts.items():
                    setattr(fact, name, value)

        print(f"\nbasic_eps changed on {eps_changed} filings")
        if missing:
            print(f"{missing} archived documents were missing and were left untouched")
        print("\nstatus transitions:")
        if not transitions:
            print("  none")
        for label, count in transitions.most_common():
            print(f"  {count:5d}  {label}")

        if args.commit:
            session.commit()
            print("\nCommitted.")
        else:
            session.rollback()
            print("\nDry run only. Re-run with --commit to persist.")
    finally:
        session.close()


if __name__ == "__main__":
    main()
