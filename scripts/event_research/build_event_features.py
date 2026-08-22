"""Assemble event features under charter v3's frozen rules.

Chains each filing to its year-ago counterpart, walks the causal clock, measures
the initial response and the 20-session outcome against a point-in-time peer
basket, and writes one `event_feature_snapshot` per event.

This script computes features for **every** fold.  Feature computation is
signal-blind -- it produces per-event numbers, not a fold verdict -- so running
it now costs none of charter v3 §7's one-pass limit on fold B.  Evaluation is
`run_fold.py`, which is where the gate lives.

**A look-ahead decision, recorded here because charter §6 forces it.**
Charter §3.4 ranks an event against "the positive-surprise cohort median for
that quarter", and v3 §1's fallback standardisation is cross-sectional.  Both
read a distribution over issuers who mostly have not reported yet at the moment
any single event becomes actionable.  Using the completed quarter would be
look-ahead, which §6 classes as a hard failure, and restricting to the
season-to-date would systematically drop each quarter's earliest reporters --
a size-correlated exclusion, the exact defect shape this project keeps hitting.
So both statistics are taken from the **immediately preceding completed
reporting quarter**: fully point-in-time, stable at ~200 names, and applied
uniformly to every event.  The cost is that the first chainable quarter has no
predecessor and is recorded as ineligible.

Usage:
  finance/bin/python3 -m scripts.event_research.build_event_features
  ... add --commit to persist.
"""

from __future__ import annotations

import argparse
import sqlite3
import statistics
from collections import defaultdict
from datetime import date, timedelta
from pathlib import Path

from dotenv import load_dotenv

from app.analysis.corporate_actions import adjusted_close_series_by_issuer
from app.event_research import features as F

# A year-ago quarter is four quarters back.  Reported period ends drift by a few
# days (a 52/53-week retailer, a leap year), so the match is a window rather
# than an exact date.
YEAR_AGO_MIN_DAYS = 350
YEAR_AGO_MAX_DAYS = 380


def _as_ist(value):
    """Re-attach the offset SQLite drops.

    SQLAlchemy's SQLite DATETIME stores a naive wall-clock even when the column
    is declared timezone-aware, so timestamps come back without an offset.  The
    write path (`validation._parse_timestamp`) rejects any input lacking an
    offset and stores `.astimezone(IST)`, so the stored wall-clock is IST by
    construction -- this restores what was written rather than inferring a zone,
    which charter §6 forbids.
    """
    if value is None or value.tzinfo is not None:
        return value
    return value.replace(tzinfo=F.IST)


def load_calendar(panel: sqlite3.Connection, exchange: str = "NSE") -> list[date]:
    """The exchange's own recorded trading days, weekend sessions included."""
    return [
        date.fromisoformat(row[0])
        for row in panel.execute(
            "SELECT session FROM price_sessions "
            "WHERE exchange = ? AND status = 'LOADED' ORDER BY session",
            (exchange,),
        )
    ]


def load_cohorts(session) -> dict[date, dict[str, float]]:
    """Traded value by issuer prefix, per dated cohort snapshot."""
    from sqlalchemy import select

    from app.event_research.models import EligibleUniverseSnapshot

    rows = session.execute(
        select(
            EligibleUniverseSnapshot.as_of_date,
            EligibleUniverseSnapshot.isin,
            EligibleUniverseSnapshot.avg_daily_value_20d,
        ).where(EligibleUniverseSnapshot.cohort_id.like("liquid-%"))
    ).all()
    cohorts: dict[date, dict[str, float]] = defaultdict(dict)
    for as_of, isin, value in rows:
        if value:
            cohorts[as_of][isin[:9]] = value
    return dict(cohorts)


def cohort_as_of(cohorts: dict[date, dict[str, float]], when: date) -> date | None:
    """The most recent snapshot effective at `when`.

    Never a later one: a cohort formed after the event would encode who was
    still liquid afterwards.
    """
    eligible = [as_of for as_of in cohorts if as_of <= when]
    return max(eligible) if eligible else None


def load_events(session) -> list[dict]:
    """Original, consolidated-preferred, discrete quarterly filings with an EPS.

    Revisions are excluded from the signal per charter §6: the original is what
    the market actually traded on.  Where an issuer filed both consolidated and
    standalone for a period, consolidated wins -- charter §3.1 -- and standalone
    is the fallback rather than a second event.
    """
    from sqlalchemy import select

    from app.event_research.models import (
        EventResearchInstrument,
        FinancialResultEvent,
        FinancialResultFact,
    )

    rows = session.execute(
        select(
            FinancialResultEvent.id,
            EventResearchInstrument.isin,
            EventResearchInstrument.nse_symbol,
            FinancialResultEvent.result_period_end,
            FinancialResultEvent.available_at,
            FinancialResultFact.basic_eps,
            FinancialResultFact.reporting_scope,
        )
        .join(
            EventResearchInstrument,
            EventResearchInstrument.id == FinancialResultEvent.instrument_id,
        )
        .join(
            FinancialResultFact,
            FinancialResultFact.event_id == FinancialResultEvent.id,
        )
        .where(
            FinancialResultEvent.is_revision.is_(False),
            FinancialResultFact.validation_status == "VALID",
            FinancialResultFact.is_cumulative.is_(False),
            FinancialResultFact.basic_eps.isnot(None),
        )
    ).all()

    # One event per (issuer, period): consolidated preferred, then the earliest
    # dissemination, so the choice is deterministic and not document order.
    best: dict[tuple[str, date], dict] = {}
    for event_id, isin, symbol, period_end, available_at, eps, scope in rows:
        key = (isin[:9], period_end)
        candidate = {
            "event_id": event_id,
            "isin": isin,
            "prefix": isin[:9],
            "symbol": symbol,
            "period_end": period_end,
            "available_at": _as_ist(available_at),
            "eps": eps,
            "scope": scope,
        }
        incumbent = best.get(key)
        if incumbent is None:
            best[key] = candidate
            continue
        better_scope = (
            candidate["scope"] == "consolidated" and incumbent["scope"] != "consolidated"
        )
        same_scope_earlier = (
            candidate["scope"] == incumbent["scope"]
            and candidate["available_at"] < incumbent["available_at"]
        )
        if better_scope or same_scope_earlier:
            best[key] = candidate
    return list(best.values())


def find_year_ago(periods: dict[date, dict], period_end: date) -> dict | None:
    """The same fiscal quarter one year earlier, matched on a tolerance window."""
    for candidate_end, event in periods.items():
        gap = (period_end - candidate_end).days
        if YEAR_AGO_MIN_DAYS <= gap <= YEAR_AGO_MAX_DAYS:
            return event
    return None


def build(panel: sqlite3.Connection, session, calendar: list[date]) -> list[dict]:
    cohorts = load_cohorts(session)
    events = load_events(session)
    print(f"{len(events)} original discrete VALID filings with an EPS")

    by_issuer: dict[str, dict[date, dict]] = defaultdict(dict)
    for event in events:
        by_issuer[event["prefix"]][event["period_end"]] = event

    # ---- seasonal differences, and the price they are scaled by -------------
    price_cache: dict[tuple[str, str, str], dict[str, float]] = {}

    def prices(prefix_isin: str, start: date, end: date, column: str) -> dict[str, float]:
        key = (prefix_isin[:9], column, f"{start}:{end}")
        if key not in price_cache:
            price_cache[key] = dict(
                adjusted_close_series_by_issuer(
                    panel, prefix_isin, start, end, column=column
                )
            )
        return price_cache[key]

    computed: list[dict] = []
    for event in events:
        record = {
            **event,
            "prior_event_id": None,
            "eps_year_ago": None,
            "surprise_raw": None,
            "surprise_scaled": None,
            "decision": "EXCLUDED",
            "reason": "",
        }
        prior = find_year_ago(by_issuer[event["prefix"]], event["period_end"])
        if prior is None:
            record["reason"] = "NO_YEAR_AGO_FILING"
            computed.append(record)
            continue
        if prior["available_at"] >= event["available_at"]:
            # The comparative must have been public first, or the surprise
            # could not have been computed at the time.
            record["reason"] = "YEAR_AGO_NOT_YET_PUBLIC"
            computed.append(record)
            continue

        record["prior_event_id"] = prior["event_id"]
        record["eps_year_ago"] = prior["eps"]
        record["surprise_raw"] = F.seasonal_difference(event["eps"], prior["eps"])

        clock = F.resolve_clock(event["available_at"], calendar)
        if clock is None:
            record["reason"] = "NO_COMPLETE_FORWARD_WINDOW"
            computed.append(record)
            continue
        record["clock"] = clock

        closes = prices(event["isin"], clock.prior_session, clock.exit_session, "close")
        reference_price = closes.get(clock.prior_session.isoformat())
        if not reference_price:
            record["reason"] = "NO_PRICE_AT_AVAILABLE_AT"
            computed.append(record)
            continue
        record["surprise_scaled"] = record["surprise_raw"] / reference_price
        record["decision"] = "PENDING"
        computed.append(record)

    # ---- standardisation ----------------------------------------------------
    # Cross-sectional statistics come from the PRIOR completed reporting
    # quarter, so nothing reads a distribution that did not exist yet.
    scaled_by_period: dict[date, list[float]] = defaultdict(list)
    for record in computed:
        if record["surprise_scaled"] is not None:
            scaled_by_period[record["period_end"]].append(record["surprise_scaled"])

    ordered_periods = sorted(scaled_by_period)
    previous_period = {
        period: ordered_periods[index - 1] if index else None
        for index, period in enumerate(ordered_periods)
    }

    for record in computed:
        if record["decision"] != "PENDING":
            continue
        prefix, period_end = record["prefix"], record["period_end"]

        # Prior seasonal differences for this issuer, restricted to pairs that
        # were both public before this event became actionable.
        history: list[float] = []
        for other_end, other in sorted(by_issuer[prefix].items()):
            if other_end >= period_end:
                continue
            other_prior = find_year_ago(by_issuer[prefix], other_end)
            if other_prior is None:
                continue
            if max(other["available_at"], other_prior["available_at"]) >= record["available_at"]:
                continue
            history.append(F.seasonal_difference(other["eps"], other_prior["eps"]))
        record["history_n"] = len(history)

        time_series = F.standardise_time_series(record["surprise_raw"], history)
        reference_period = previous_period.get(period_end)
        cross_sectional = (
            F.standardise_cross_sectional(
                record["surprise_scaled"], scaled_by_period[reference_period]
            )
            if reference_period
            else None
        )
        record["std_time_series"] = time_series
        record["std_cross_sectional"] = cross_sectional
        value, method = F.select_standardisation(time_series, cross_sectional)
        record["surprise_standardised"] = value
        record["surprise_method"] = method
        if value is None:
            record["decision"] = "EXCLUDED"
            record["reason"] = "NO_STANDARDISATION_AVAILABLE"

    # ---- returns against the peer basket ------------------------------------
    for record in computed:
        if record["decision"] != "PENDING":
            continue
        clock = record["clock"]
        as_of = cohort_as_of(cohorts, clock.reaction_session)
        if as_of is None or record["prefix"] not in cohorts[as_of]:
            record["decision"] = "EXCLUDED"
            record["reason"] = "NOT_IN_COHORT_AT_EVENT_TIME"
            continue
        record["cohort_as_of"] = as_of
        record["cohort_id"] = f"liquid-{as_of.isoformat()}"

        peers = F.peer_basket(record["isin"], cohorts[as_of])
        if len(peers) < F.PEER_BASKET_SIZE:
            record["decision"] = "EXCLUDED"
            record["reason"] = f"PEER_BASKET_TOO_SMALL_{len(peers)}"
            continue
        record["peers"] = peers

        own_closes = prices(record["isin"], clock.prior_session, clock.exit_session, "close")
        own_opens = prices(record["isin"], clock.prior_session, clock.exit_session, "open")
        response = F.simple_return(
            own_closes.get(clock.prior_session.isoformat()),
            own_closes.get(clock.reaction_session.isoformat()),
        )
        forward = F.simple_return(
            own_opens.get(clock.entry_session.isoformat()),
            own_opens.get(clock.exit_session.isoformat()),
        )
        if response is None or forward is None:
            record["decision"] = "EXCLUDED"
            record["reason"] = "INCOMPLETE_OWN_PRICE_SERIES"
            continue

        peer_responses, peer_forwards = [], []
        for peer in peers:
            peer_closes = prices(peer, clock.prior_session, clock.exit_session, "close")
            peer_opens = prices(peer, clock.prior_session, clock.exit_session, "open")
            peer_responses.append(
                F.simple_return(
                    peer_closes.get(clock.prior_session.isoformat()),
                    peer_closes.get(clock.reaction_session.isoformat()),
                )
            )
            peer_forwards.append(
                F.simple_return(
                    peer_opens.get(clock.entry_session.isoformat()),
                    peer_opens.get(clock.exit_session.isoformat()),
                )
            )
        benchmark_response = F.equal_weight_mean(peer_responses)
        benchmark_forward = F.equal_weight_mean(peer_forwards)
        if benchmark_response is None or benchmark_forward is None:
            record["decision"] = "EXCLUDED"
            record["reason"] = "NO_USABLE_PEER_RETURNS"
            continue

        record["response_raw"] = response
        record["response_peer_adjusted"] = response - benchmark_response
        record["forward_raw"] = forward
        record["forward_peer_adjusted"] = forward - benchmark_forward
        record["benchmark_response"] = benchmark_response
        record["benchmark_forward"] = benchmark_forward

        adv = cohorts[as_of].get(record["prefix"])
        record["adv_60d"] = adv
        record["participation_ok"] = F.participation_ok(adv)
        if record["participation_ok"] is False:
            record["decision"] = "EXCLUDED"
            record["reason"] = "EXCEEDS_ADV_PARTICIPATION_CAP"
            continue

        record["fold"] = fold_label = F.fold_for(clock.reaction_session)
        if fold_label is None:
            record["decision"] = "EXCLUDED"
            record["reason"] = "OUTSIDE_EVERY_FOLD"
            continue

        record["decision"] = "ELIGIBLE"
        record["reason"] = "OK"

    return computed


def persist(session, records: list[dict]) -> int:
    from app.event_research.models import EventFeatureSnapshot

    written = 0
    for record in records:
        clock = record.get("clock")
        session.add(
            EventFeatureSnapshot(
                event_id=record["event_id"],
                feature_version=F.FEATURE_VERSION,
                prior_event_id=record.get("prior_event_id"),
                eps_current=record.get("eps"),
                eps_year_ago=record.get("eps_year_ago"),
                surprise_raw=record.get("surprise_raw"),
                surprise_scaled=record.get("surprise_scaled"),
                surprise_standardised=record.get("surprise_standardised"),
                surprise_std_time_series=record.get("std_time_series"),
                surprise_std_cross_sectional=record.get("std_cross_sectional"),
                surprise_method=record.get("surprise_method"),
                surprise_history_n=record.get("history_n"),
                available_at=record.get("available_at"),
                reaction_session=clock.reaction_session if clock else None,
                entry_session=clock.entry_session if clock else None,
                exit_session=clock.exit_session if clock else None,
                response_raw=record.get("response_raw"),
                response_peer_adjusted=record.get("response_peer_adjusted"),
                forward_return_raw=record.get("forward_raw"),
                forward_return_peer_adjusted=record.get("forward_peer_adjusted"),
                benchmark_rule=f"equal-weight {F.PEER_BASKET_SIZE} nearest by log 20d traded value",
                benchmark_peer_isins=",".join(record.get("peers", [])) or None,
                benchmark_response_return=record.get("benchmark_response"),
                benchmark_forward_return=record.get("benchmark_forward"),
                adv_60d=record.get("adv_60d"),
                participation_ok=record.get("participation_ok"),
                cohort_id=record.get("cohort_id"),
                cohort_as_of=record.get("cohort_as_of"),
                fold_label=record.get("fold"),
                eligibility_decision=record["decision"],
                eligibility_reason=record["reason"],
            )
        )
        written += 1
    session.commit()
    return written


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--panel-db", type=Path, default=Path("data/analysis/prices.sqlite"))
    parser.add_argument("--commit", action="store_true")
    args = parser.parse_args()

    load_dotenv()
    from app.event_research.database import new_session

    panel = sqlite3.connect(f"file:{args.panel_db}?mode=ro", uri=True)
    session = new_session()
    try:
        calendar = load_calendar(panel)
        print(f"Calendar: {len(calendar)} NSE sessions {calendar[0]} .. {calendar[-1]}")
        records = build(panel, session, calendar)

        print(f"\nFeature version {F.FEATURE_VERSION} (charter {CHARTER_VERSION_LABEL})")
        reasons: dict[str, int] = defaultdict(int)
        for record in records:
            reasons[f"{record['decision']}:{record['reason']}"] += 1
        for label, count in sorted(reasons.items(), key=lambda kv: -kv[1]):
            print(f"  {count:5d}  {label}")

        eligible = [r for r in records if r["decision"] == "ELIGIBLE"]
        print(f"\n{len(eligible)} eligible events")
        by_fold: dict[str, set] = defaultdict(set)
        for record in eligible:
            by_fold[record["fold"]].add(record["period_end"])
        for fold in sorted(by_fold):
            quarters = sorted(by_fold[fold])
            count = sum(1 for r in eligible if r["fold"] == fold)
            print(f"  fold {fold}: {count:4d} events across {len(quarters)} quarters")

        methods: dict[str, int] = defaultdict(int)
        for record in eligible:
            methods[f"{record['fold']}/{record['surprise_method']}"] += 1
        print("\nStandardisation method by fold (the hybrid rule's confound, made visible):")
        for label, count in sorted(methods.items()):
            print(f"  {label}: {count}")

        if args.commit:
            written = persist(session, records)
            print(f"\nWrote {written} feature snapshots")
        else:
            print("\nDry run only. Re-run with --commit to persist.")
    finally:
        session.close()
        panel.close()


CHARTER_VERSION_LABEL = F.CHARTER_VERSION


if __name__ == "__main__":
    main()
