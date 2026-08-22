"""Day-0 probe: is the year-ago comparative recoverable from a single filing?

The charter's primary signal is a seasonal surprise -- EPS for a quarter against
the same quarter one year earlier.  Today `xbrl_parser` resolves exactly one
context (the reported period) and stores one `basic_eps`, so a surprise can only
be formed by *chaining* two separately-ingested filings four quarters apart.
Chaining is expensive: it needs both filings to be VALID, and fold A's opening
quarters would need year-ago filings from 2022, an era measured at 0% usable.

`docs/research_log.md` records that an NSE instance carries "both the reported
quarter and the year-ago quarter".  That has never been verified on the clean
era.  This probe answers three questions, using only files already on disk:

  1. Does a *defined, non-dimensional* duration context exist for the year-ago
     quarter in filings we already scored VALID?
  2. Is `basic_eps` actually tagged against that context?
  3. Where a chained prior filing also exists, do the two agree?

(3) is the one that matters.  A number that merely parses is not evidence; a
number that reproduces an independently-ingested filing to the paisa is.

Reads only.  No network, no API spend, no writes to the research database.
"""

from __future__ import annotations

import argparse
import json
import sqlite3
import xml.etree.ElementTree as ET
from collections import Counter, defaultdict
from datetime import date, timedelta
from pathlib import Path
from typing import Any

from app.event_research.xbrl_parser import (
    XBRLContext,
    _collect_candidates,
    read_contexts,
)


DEFAULT_DB = Path("data/event_research/event_research.sqlite")

# A "year-ago" context ends 360-370 days before the reported period and covers a
# span within 8 days of the reported one.  Both bands are deliberately loose:
# quarter-ends drift with the calendar, and a filer may define 2023-04-01..
# 2023-06-30 where its predecessor defined 2022-04-01..2022-06-30.  Tight
# matching would report a false negative for the probe's actual question.
_END_LAG_MIN = timedelta(days=360)
_END_LAG_MAX = timedelta(days=370)
_SPAN_TOLERANCE = timedelta(days=8)

# Agreement band for (3).  EPS is reported to two decimals; anything inside a
# paisa is the same number.
_EPS_AGREE_ABS = 0.011


def _load_valid_events(db_path: Path) -> list[dict[str, Any]]:
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    try:
        rows = conn.execute(
            """
            SELECT e.id            AS event_id,
                   e.instrument_id AS instrument_id,
                   e.result_period_end,
                   e.raw_storage_path,
                   e.disseminated_at,
                   f.basic_eps,
                   f.is_cumulative,
                   f.reporting_scope
            FROM financial_result_events e
            JOIN financial_result_facts f ON f.event_id = e.id
            WHERE f.validation_status = 'VALID'
              AND f.basic_eps IS NOT NULL
            ORDER BY e.instrument_id, e.result_period_end
            """
        ).fetchall()
    finally:
        conn.close()
    return [dict(row) for row in rows]


def _reported_context(
    contexts: dict[str, XBRLContext], period_end: date
) -> XBRLContext | None:
    """The non-dimensional duration whose end matches the filing's stated period.

    Mirrors how `parse_result_xbrl` chose the context that produced the stored
    `basic_eps`, so the comparative is anchored to the same period the VALID
    record describes -- not to whatever the document happens to end on.
    """
    durations = [
        c for c in contexts.values()
        if not c.is_dimensional and c.start_date and c.end_date
    ]
    exact = [c for c in durations if c.end_date == period_end]
    if exact:
        # Shortest span wins: a filing carries both the quarter and the YTD
        # period ending on the same date.
        return min(exact, key=lambda c: c.end_date - c.start_date)
    return None


def _comparative_context(
    contexts: dict[str, XBRLContext], reported: XBRLContext
) -> XBRLContext | None:
    """The defined duration one year behind `reported`, same span."""
    assert reported.start_date and reported.end_date
    reported_span = reported.end_date - reported.start_date
    matches = [
        c for c in contexts.values()
        if not c.is_dimensional
        and c.start_date
        and c.end_date
        and _END_LAG_MIN <= (reported.end_date - c.end_date) <= _END_LAG_MAX
        and abs((c.end_date - c.start_date) - reported_span) <= _SPAN_TOLERANCE
    ]
    if not matches:
        return None
    # Closest span to the reported one, then closest to exactly 365 days back.
    return min(
        matches,
        key=lambda c: (
            abs((c.end_date - c.start_date) - reported_span),
            abs((reported.end_date - c.end_date) - timedelta(days=365)),
        ),
    )


def _eps_for_context(
    candidates: dict[str, list[tuple[str, str, str]]], context_id: str
) -> float | None:
    """`basic_eps` tagged against one context, using the parser's tag preference."""
    from app.event_research.xbrl_parser import _FIELD_TAGS, _to_float

    for tag in _FIELD_TAGS["basic_eps"]:
        for candidate_tag, context_ref, raw in candidates["basic_eps"]:
            if candidate_tag == tag and context_ref == context_id:
                value = _to_float(raw)
                if value is not None:
                    return value
    return None


def probe(db_path: Path) -> dict[str, Any]:
    events = _load_valid_events(db_path)
    outcomes: Counter[str] = Counter()
    by_year: dict[str, Counter[str]] = defaultdict(Counter)
    extracted: dict[tuple[str, str], float] = {}
    per_event: list[dict[str, Any]] = []

    for event in events:
        period_end = date.fromisoformat(event["result_period_end"])
        year = (event["disseminated_at"] or "")[:4]
        raw_path = Path(event["raw_storage_path"])

        record: dict[str, Any] = {
            "instrument_id": event["instrument_id"],
            "result_period_end": event["result_period_end"],
            "dissemination_year": year,
            "is_cumulative": bool(event["is_cumulative"]),
            "reported_eps": event["basic_eps"],
        }

        if not raw_path.exists():
            outcomes["RAW_MISSING"] += 1
            by_year[year]["RAW_MISSING"] += 1
            record["outcome"] = "RAW_MISSING"
            per_event.append(record)
            continue

        try:
            root = ET.parse(str(raw_path)).getroot()
        except ET.ParseError:
            outcomes["UNPARSEABLE"] += 1
            by_year[year]["UNPARSEABLE"] += 1
            record["outcome"] = "UNPARSEABLE"
            per_event.append(record)
            continue

        contexts = read_contexts(root)
        candidates, _ = _collect_candidates(root, contexts)

        reported = _reported_context(contexts, period_end)
        if reported is None:
            outcomes["NO_REPORTED_CONTEXT"] += 1
            by_year[year]["NO_REPORTED_CONTEXT"] += 1
            record["outcome"] = "NO_REPORTED_CONTEXT"
            per_event.append(record)
            continue
        record["reported_period"] = f"{reported.start_date}..{reported.end_date}"

        comparative = _comparative_context(contexts, reported)
        if comparative is None:
            outcomes["NO_COMPARATIVE_CONTEXT"] += 1
            by_year[year]["NO_COMPARATIVE_CONTEXT"] += 1
            record["outcome"] = "NO_COMPARATIVE_CONTEXT"
            per_event.append(record)
            continue
        record["comparative_period"] = f"{comparative.start_date}..{comparative.end_date}"

        eps = _eps_for_context(candidates, comparative.context_id)
        if eps is None:
            outcomes["CONTEXT_BUT_NO_EPS"] += 1
            by_year[year]["CONTEXT_BUT_NO_EPS"] += 1
            record["outcome"] = "CONTEXT_BUT_NO_EPS"
            per_event.append(record)
            continue

        outcomes["COMPARATIVE_EPS_FOUND"] += 1
        by_year[year]["COMPARATIVE_EPS_FOUND"] += 1
        record["outcome"] = "COMPARATIVE_EPS_FOUND"
        record["comparative_eps"] = eps
        assert comparative.end_date is not None
        extracted[(event["instrument_id"], comparative.end_date.isoformat())] = eps
        per_event.append(record)

    cross_check = _cross_check(events, extracted)

    return {
        "valid_events_examined": len(events),
        "outcomes": dict(outcomes),
        "outcomes_by_dissemination_year": {y: dict(c) for y, c in sorted(by_year.items())},
        "cross_check": cross_check,
        "per_event": per_event,
    }


def _cross_check(
    events: list[dict[str, Any]], extracted: dict[tuple[str, str], float]
) -> dict[str, Any]:
    """Compare in-filing comparatives against independently-ingested filings.

    The year-ago EPS pulled out of a 2024 filing should equal the EPS parsed
    from that issuer's own 2023 filing, which was ingested separately from a
    different document.  Two independent documents agreeing is the only
    evidence here that the extraction is reading the right context.
    """
    # A period can be filed more than once (standalone/consolidated, revisions),
    # so collect every stored value per (instrument, period) rather than one.
    stored: dict[tuple[str, str], set[float]] = defaultdict(set)
    for event in events:
        stored[(event["instrument_id"], event["result_period_end"])].add(event["basic_eps"])

    agree = disagree = 0
    mismatches: list[dict[str, Any]] = []
    for key, comparative_eps in extracted.items():
        known = stored.get(key)
        if not known:
            continue
        if any(abs(comparative_eps - value) <= _EPS_AGREE_ABS for value in known):
            agree += 1
        else:
            disagree += 1
            mismatches.append(
                {
                    "instrument_id": key[0],
                    "period_end": key[1],
                    "from_comparative": comparative_eps,
                    "from_own_filing": sorted(known),
                }
            )

    comparable = agree + disagree
    return {
        "comparable_pairs": comparable,
        "agree": agree,
        "disagree": disagree,
        "agreement_rate": round(agree / comparable, 4) if comparable else None,
        "mismatches": mismatches[:20],
    }


def _print_report(report: dict[str, Any]) -> None:
    total = report["valid_events_examined"]
    print(f"VALID events examined: {total}")
    print("\nOutcome:")
    for name, count in sorted(report["outcomes"].items(), key=lambda kv: -kv[1]):
        print(f"  {name:<24} {count:>5}  ({count / total:.0%})" if total else f"  {name}")

    print("\nBy dissemination year:")
    for year, counts in report["outcomes_by_dissemination_year"].items():
        found = counts.get("COMPARATIVE_EPS_FOUND", 0)
        year_total = sum(counts.values())
        rate = f"{found / year_total:.0%}" if year_total else "-"
        print(f"  {year}  {found:>4}/{year_total:<4} usable ({rate})")

    check = report["cross_check"]
    print("\nCross-check against independently-ingested filings:")
    print(f"  comparable pairs  {check['comparable_pairs']}")
    print(f"  agree             {check['agree']}")
    print(f"  disagree          {check['disagree']}")
    if check["agreement_rate"] is not None:
        print(f"  agreement rate    {check['agreement_rate']:.1%}")
    for mismatch in check["mismatches"]:
        print(
            f"    MISMATCH {mismatch['period_end']} "
            f"comparative={mismatch['from_comparative']} own={mismatch['from_own_filing']}"
        )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--db", type=Path, default=DEFAULT_DB)
    parser.add_argument("--output", type=Path, help="write the full report as JSON")
    args = parser.parse_args()

    report = probe(args.db)
    _print_report(report)

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(report, indent=2, default=str))
        print(f"\nWrote {args.output}")


if __name__ == "__main__":
    main()
