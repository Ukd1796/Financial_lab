"""Evaluate one fold against charter v3 §7's frozen decision table.

This is the only script that turns per-event features into a verdict, and the
only one subject to the one-pass limit.  Fold A may be re-run freely -- it is
the development fold, where charter v2 §2 says every design choice is fixed.
Folds B and C record a `fold_evaluation_runs` row on first use and refuse a
second run, so "fold B is run exactly once" is enforced by a uniqueness
constraint rather than by anyone's memory.

The verdict vocabulary is charter v3 §5: PASS, FAIL, or INCONCLUSIVE, where
INCONCLUSIVE means the sample was too thin to decide and is **not** a licence to
widen the search.

Usage:
  finance/bin/python3 -m scripts.event_research.run_fold --fold A
"""

from __future__ import annotations

import argparse
import sqlite3
import statistics
from collections import defaultdict
from datetime import date
from pathlib import Path

from dotenv import load_dotenv

from app.event_research import features as F

# The per-quarter standard error measured in charter v3 §6 for a 40-name book.
# Quoted, not recomputed, so the t-statistic is judged against the number that
# was frozen before any result existed.
SE_PER_QUARTER = 0.0142


def load_eligible(session, fold: str) -> list[dict]:
    from sqlalchemy import select

    from app.event_research.models import (
        EventFeatureSnapshot,
        EventResearchInstrument,
        FinancialResultEvent,
    )

    rows = session.execute(
        select(
            EventFeatureSnapshot.event_id,
            EventResearchInstrument.isin,
            EventResearchInstrument.nse_symbol,
            FinancialResultEvent.result_period_end,
            EventFeatureSnapshot.surprise_standardised,
            EventFeatureSnapshot.surprise_method,
            EventFeatureSnapshot.response_peer_adjusted,
            EventFeatureSnapshot.forward_return_peer_adjusted,
        )
        .join(
            FinancialResultEvent,
            FinancialResultEvent.id == EventFeatureSnapshot.event_id,
        )
        .join(
            EventResearchInstrument,
            EventResearchInstrument.id == FinancialResultEvent.instrument_id,
        )
        .where(
            EventFeatureSnapshot.feature_version == F.FEATURE_VERSION,
            EventFeatureSnapshot.fold_label == fold,
            EventFeatureSnapshot.eligibility_decision == "ELIGIBLE",
        )
    ).all()
    return [
        {
            "event_id": event_id,
            "isin": isin,
            "symbol": symbol,
            "period_end": period_end,
            "surprise": surprise,
            "method": method,
            "response": response,
            "forward": forward,
        }
        for event_id, isin, symbol, period_end, surprise, method, response, forward in rows
    ]


def load_collapsed_issuers(analysis_db: Path) -> set[str]:
    """Issuer prefixes whose equity was destroyed, for charter v3 §7 condition 5."""
    if not analysis_db.exists():
        return set()
    conn = sqlite3.connect(f"file:{analysis_db}?mode=ro", uri=True)
    try:
        return {
            row[0][:9]
            for row in conn.execute(
                "SELECT isin FROM delisting_outcomes WHERE status = 'EXIT_AFTER_COLLAPSE'"
            )
        }
    finally:
        conn.close()


def response_median_reference(
    events: list[dict], periods: list[date]
) -> dict[date, float | None]:
    """The positive-surprise response median, taken from the PRIOR quarter.

    Charter §3.4 compares an event to "the positive-surprise cohort median for
    that quarter", but at the moment any one event becomes actionable most of
    that quarter has not reported.  Reading the completed quarter would be
    look-ahead, which charter §6 calls a hard failure; restricting to the
    season-to-date would drop each quarter's earliest reporters, a
    size-correlated exclusion.  The prior completed quarter is point-in-time,
    stable, and applied identically to every event.
    """
    by_period: dict[date, list[float]] = defaultdict(list)
    for event in events:
        if event["surprise"] is not None and event["surprise"] > 0 and event["response"] is not None:
            by_period[event["period_end"]].append(event["response"])

    reference: dict[date, float | None] = {}
    for index, period in enumerate(periods):
        if index == 0:
            reference[period] = None
            continue
        prior = by_period.get(periods[index - 1], [])
        reference[period] = statistics.median(prior) if len(prior) >= 2 else None
    return reference


def build_book(events: list[dict], median_response: float | None) -> list[dict]:
    """Charter §3.4's primary bucket, truncated to charter v3 §4's fixed K."""
    if median_response is None:
        return []
    bucket = [
        event
        for event in events
        if event["surprise"] is not None
        and event["surprise"] > 0
        and event["response"] is not None
        and event["response"] < median_response
        and event["forward"] is not None
    ]
    bucket.sort(key=lambda event: event["surprise"], reverse=True)
    return bucket[: F.BOOK_SIZE]


def evaluate(events: list[dict], collapsed: set[str]) -> dict:
    periods = sorted({event["period_end"] for event in events})
    reference = response_median_reference(events, periods)

    quarters: list[dict] = []
    for period in periods:
        in_quarter = [event for event in events if event["period_end"] == period]
        book = build_book(in_quarter, reference[period])
        gross = statistics.mean(event["forward"] for event in book) if book else None
        excluded_book = [
            event for event in book if event["isin"][:9] not in collapsed
        ]
        quarters.append(
            {
                "period": period,
                "candidates": len(in_quarter),
                "book": len(book),
                "gross": gross,
                "net": gross - F.ROUND_TRIP_COST if gross is not None else None,
                "net_ex_collapsed": (
                    statistics.mean(e["forward"] for e in excluded_book) - F.ROUND_TRIP_COST
                    if excluded_book
                    else None
                ),
                "methods": {
                    method: sum(1 for e in book if e["method"] == method)
                    for method in {e["method"] for e in book}
                },
                "usable": len(book) >= F.MIN_EVENTS_PER_QUARTER,
            }
        )

    usable = [q for q in quarters if q["usable"] and q["net"] is not None]
    nets = [q["net"] for q in usable]
    aggregate = statistics.mean(nets) if nets else None
    standard_error = SE_PER_QUARTER / len(usable) ** 0.5 if usable else None

    concentration = None
    if aggregate is not None and nets and any(abs(n) > 0 for n in nets):
        total = sum(abs(n) for n in nets)
        concentration = max(abs(n) for n in nets) / total if total else None

    nets_ex = [q["net_ex_collapsed"] for q in usable if q["net_ex_collapsed"] is not None]
    return {
        "quarters": quarters,
        "usable_quarters": len(usable),
        "aggregate_net": aggregate,
        "aggregate_net_ex_collapsed": statistics.mean(nets_ex) if nets_ex else None,
        "standard_error": standard_error,
        "t_stat": aggregate / standard_error if aggregate is not None and standard_error else None,
        "max_quarter_share": concentration,
    }


def verdict(result: dict) -> tuple[str, list[str]]:
    """Charter v3 §7, applied literally.  Sufficiency is checked first."""
    notes: list[str] = []
    if result["usable_quarters"] < F.MIN_QUARTERS_PER_FOLD:
        return "INCONCLUSIVE", [
            f"only {result['usable_quarters']} usable quarters, floor is "
            f"{F.MIN_QUARTERS_PER_FOLD} (charter v3 §4)"
        ]

    failures: list[str] = []
    aggregate = result["aggregate_net"]
    if aggregate is None or aggregate < F.PASS_BAR:
        failures.append(
            f"cond.1 net return {aggregate:.4f} < bar {F.PASS_BAR:.4f}"
            if aggregate is not None else "cond.1 no measurable net return"
        )
    if aggregate is not None and aggregate <= 0:
        failures.append("cond.2 fold sign is not positive")
    share = result["max_quarter_share"]
    if share is not None and share > 0.40:
        failures.append(f"cond.3 one quarter carries {share:.0%} of the aggregate (>40%)")
    ex_collapsed = result["aggregate_net_ex_collapsed"]
    if (
        aggregate is not None
        and ex_collapsed is not None
        and (aggregate > 0) != (ex_collapsed > 0)
    ):
        failures.append("cond.5 sign flips when the collapsed population is excluded")

    if failures:
        return "FAIL", failures
    notes.append("cond.2 requires fold B independently; cond.4 requires fold C")
    return "PASS", notes


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--fold", required=True, choices=["A", "B", "C"])
    parser.add_argument("--analysis-db", type=Path, default=Path("data/analysis/analysis.sqlite"))
    parser.add_argument(
        "--i-am-overriding-a-pre-registered-limit", dest="override", default=None,
        help="Reason for re-running a spent fold; recorded in the run log",
    )
    args = parser.parse_args()

    load_dotenv()
    from sqlalchemy import select

    from app.event_research.database import new_session
    from app.event_research.models import FoldEvaluationRun

    session = new_session()
    try:
        # Charter v3 §7: fold B is run exactly once.  Fold A is the development
        # fold and is deliberately exempt.
        if args.fold in ("B", "C"):
            spent = session.execute(
                select(FoldEvaluationRun).where(
                    FoldEvaluationRun.fold_label == args.fold,
                    FoldEvaluationRun.feature_version == F.FEATURE_VERSION,
                )
            ).scalar_one_or_none()
            if spent and not args.override:
                raise SystemExit(
                    f"Fold {args.fold} was already evaluated at {spent.ran_at} under "
                    f"feature version {F.FEATURE_VERSION}.\n"
                    f"  Result then: {spent.result_summary}\n"
                    "Charter v3 §7 allows one pass. Re-running requires "
                    "--i-am-overriding-a-pre-registered-limit '<reason>', and the "
                    "override must be recorded in docs/research_log.md."
                )

        events = load_eligible(session, args.fold)
        if not events:
            raise SystemExit(f"No eligible events for fold {args.fold}")
        collapsed = load_collapsed_issuers(args.analysis_db)
        result = evaluate(events, collapsed)

        print(f"Fold {args.fold} — feature {F.FEATURE_VERSION}, charter {F.CHARTER_VERSION}")
        print(f"{len(events)} eligible events, {len(result['quarters'])} quarters\n")
        print(f"{'quarter':<12}{'cand':>6}{'book':>6}{'gross':>9}{'net':>9}  methods")
        for quarter in result["quarters"]:
            gross = f"{quarter['gross']:+.2%}" if quarter["gross"] is not None else "  --  "
            net = f"{quarter['net']:+.2%}" if quarter["net"] is not None else "  --  "
            flag = "" if quarter["usable"] else f"  (dropped, <{F.MIN_EVENTS_PER_QUARTER})"
            methods = " ".join(f"{k}={v}" for k, v in sorted(quarter["methods"].items()))
            print(
                f"{quarter['period'].isoformat():<12}{quarter['candidates']:>6}"
                f"{quarter['book']:>6}{gross:>9}{net:>9}  {methods}{flag}"
            )

        print(f"\nusable quarters      : {result['usable_quarters']}")
        if result["aggregate_net"] is not None:
            print(f"aggregate net/quarter: {result['aggregate_net']:+.2%}"
                  f"   (bar {F.PASS_BAR:+.2%})")
            print(f"standard error       : {result['standard_error']:.2%}"
                  f"   t = {result['t_stat']:+.2f}")
        if result["aggregate_net_ex_collapsed"] is not None:
            print(f"ex-collapsed         : {result['aggregate_net_ex_collapsed']:+.2%}")
        if result["max_quarter_share"] is not None:
            print(f"largest quarter share: {result['max_quarter_share']:.0%}   (limit 40%)")

        outcome, notes = verdict(result)
        print(f"\nVERDICT: {outcome}")
        for note in notes:
            print(f"  - {note}")

        summary = (
            f"{outcome}; net {result['aggregate_net']}, "
            f"{result['usable_quarters']} usable quarters"
        )
        if args.fold in ("B", "C"):
            session.add(
                FoldEvaluationRun(
                    fold_label=args.fold,
                    feature_version=F.FEATURE_VERSION,
                    charter_version=F.CHARTER_VERSION,
                    result_summary=summary,
                    override_reason=args.override,
                )
            )
            session.commit()
            print(f"\nRecorded fold {args.fold} as spent.")
    finally:
        session.close()


if __name__ == "__main__":
    main()
