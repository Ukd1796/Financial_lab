"""Fetch the cohort's full fact set, once, within a hard call budget.

Resumable by construction: the work list is derived by subtracting what is
already stored from what is planned, so an interrupted run restarted with the
same arguments re-spends nothing.  Every call is checkpointed immediately —
there is no batch that can be lost.

Ordering is deliberate: fundamentals first, speculative estimate calls last, so
that a budget cut-off truncates the least valuable work rather than the core.

The estimate endpoints need no lookup call.  The 2026-08-12 probe established
that ``/stock_target_price`` and ``/stock_forecasts`` accept an **ISIN** as
their ``stock_id`` (confirmed on two unrelated issuers), and bhavcopy already
carries the ISIN — so ``/stock`` is not a prerequisite for them.  It is fetched
for a different reason: it is the only endpoint that populates a sector label.

At one request per second, a 500-symbol full pull takes roughly two hours.  Run
it detached and check the spend report afterwards.

Usage::

    PYTHONPATH=. finance/bin/python3 -m scripts.analysis.backfill \\
        --cohort-id liquid-2026-08-08 --dry-run
    PYTHONPATH=. finance/bin/python3 -m scripts.analysis.backfill \\
        --cohort-id liquid-2026-08-08 --tier core
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from dotenv import load_dotenv

from app.analysis.fundamentals import quarter_bucket
from app.analysis.sources import HISTORICAL_STATS, parse_transposed

# Fundamentals plus the governance vocabulary — the red-flag lane's inputs.
CORE_STATS = ("quarter_results", "ratios", "cashflow", "shareholding_pattern_quarterly")

# Probe finding (2026-08-12): only these two vocabularies are quarterly.  The
# rest are ANNUAL (Mar YYYY, 12 years deep), so they need re-fetching once a
# year rather than once a quarter — which is most of the steady-state saving.
QUARTERLY_STATS = ("quarter_results", "shareholding_pattern_quarterly")

# `/statement` is deliberately absent.  The probe showed its enum is
# {cashflow, yoy_results, ttm_results, quarter_results, balancesheet} — four of
# five duplicate /historical_stats — and it returns a flat single-period
# snapshot rather than a series.  Including it would spend a call per symbol for
# strictly less data.
FORECAST_MEASURES = ("EPS", "SAL")

TIERS = {
    "core": {"stats": CORE_STATS, "endpoints": (), "forecasts": ()},
    # /stock earns its call as the ONLY source of the sector label that charter
    # §3 (sector-adjusted returns) and §8 (no >40% from one sector) require —
    # /industry_search returns mgSector/mgIndustry null.
    "full": {
        "stats": HISTORICAL_STATS,
        "endpoints": ("/stock", "/corporate_actions"),
        "forecasts": (),
    },
    "everything": {
        "stats": HISTORICAL_STATS,
        "endpoints": ("/stock", "/corporate_actions", "/recent_announcements"),
        # (measure, period_type). Interim = quarterly. One call carries both the
        # consensus estimate AND the reported actual with SurprisePercent and a
        # standardized unexpected earnings figure.
        "forecasts": tuple(
            (measure, period) for measure in FORECAST_MEASURES for period in ("Annual", "Interim")
        ),
    },
}


def plan_for(members, tier):
    """Work items per member, cheapest-and-most-valuable first.

    ``members`` are dicts with ``symbol`` and (for the estimate endpoints)
    ``isin``.  Ordering matters because a budget cut-off truncates the tail: the
    fundamentals run before the speculative estimate calls.
    """
    spec = TIERS[tier]
    items: list[tuple[str, str, str, dict]] = []
    for member in members:
        symbol = member["symbol"] if isinstance(member, dict) else member
        isin = member.get("isin") if isinstance(member, dict) else None

        if "/stock" in spec["endpoints"]:
            items.append((symbol, "/stock", "", {"name": symbol}))
        for stats in spec["stats"]:
            items.append(
                (symbol, "/historical_stats", stats, {"stock_name": symbol, "stats": stats})
            )
        for endpoint in spec["endpoints"]:
            if endpoint != "/stock":
                items.append((symbol, endpoint, "", {"stock_name": symbol}))

        # The probe confirmed an ISIN is accepted as stock_id on two unrelated
        # issuers, so bhavcopy already supplies the identifier — no lookup call.
        if isin:
            for measure, period in spec["forecasts"]:
                items.append((
                    symbol, "/stock_forecasts", f"{measure}-{period}",
                    {"stock_id": isin, "measure_code": measure, "period_type": period,
                     "data_type": "Estimates", "age": "Current"},
                ))
            if spec["forecasts"]:
                items.append((symbol, "/stock_target_price", "", {"stock_id": isin}))
    return items


def facts_from(payload) -> list[dict]:
    """Transposed payloads become (period, metric, value) triples.

    Values that are not numeric are kept as ``raw_value`` with ``value`` null:
    the cell was reported, and losing that distinction would make a reported
    non-number indistinguishable from an absent quarter.
    """
    facts = []
    for period_end, row in parse_transposed(payload).items():
        for metric, value in row.items():
            numeric = None
            if isinstance(value, (int, float)) and not isinstance(value, bool):
                numeric = float(value)
                if numeric != numeric:  # NaN
                    numeric = None
            else:
                try:
                    numeric = float(str(value).replace(",", "").replace("%", "").strip())
                except (TypeError, ValueError):
                    numeric = None
            facts.append({
                "period_end": period_end,
                "bucket": quarter_bucket(period_end),
                "metric": metric,
                "value": numeric,
                "raw_value": None if value is None else str(value)[:200],
            })
    return facts


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--cohort-id", help="Cohort to fetch; omit with --symbols")
    parser.add_argument("--symbols", nargs="*", help="Explicit symbols instead of a cohort")
    parser.add_argument("--tier", choices=sorted(TIERS), default="full")
    parser.add_argument("--limit", type=int, help="Only the first N symbols (for a pilot run)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Print the planned spend and stop. Spends nothing.")
    parser.add_argument("--budget", type=int,
                        help="Override the cap for this run; still enforced")
    args = parser.parse_args()

    load_dotenv()

    from app.analysis.database import initialize_schema
    from app.analysis.indianapi_client import (
        APIError,
        BudgetExhausted,
        IndianAPIClient,
    )
    from app.analysis.repository import AnalysisRepository

    initialize_schema()
    repo = AnalysisRepository()

    members: list[dict] = [{"symbol": s, "isin": None} for s in (args.symbols or [])]
    if args.cohort_id:
        members += repo.cohort_members(args.cohort_id)
    if not members:
        raise SystemExit(
            "no symbols: pass --symbols, or --cohort-id for a cohort built by "
            "scripts.analysis.build_cohort"
        )
    if args.limit:
        members = members[: args.limit]

    if args.tier == "everything" and not any(m.get("isin") for m in members):
        print(
            "  NOTE: no ISINs available, so the estimate endpoints are skipped.\n"
            "        They key on ISIN as stock_id — use --cohort-id, which carries it."
        )

    planned = plan_for(members, args.tier)
    done = repo.fetched_pairs()
    todo = [item for item in planned if (item[0], item[1], item[2]) not in done]

    client = IndianAPIClient(budget=args.budget) if args.budget else IndianAPIClient()

    print(f"Cohort       : {args.cohort_id or 'explicit'} — {len(members)} symbols")
    print(f"Tier         : {args.tier}")
    print(f"Planned      : {len(planned)} calls")
    print(f"Already held : {len(planned) - len(todo)} (resumed, costs nothing)")
    print(f"To fetch     : {len(todo)}")
    print(f"Budget       : {client.spent()} spent, {client.remaining()} remaining "
          f"of {client.budget}")
    print(f"Est. runtime : {len(todo) * 1.05 / 60:.0f} min at 1 req/sec")

    if len(todo) > client.remaining():
        print(
            f"\n  WARNING: {len(todo)} calls needed but only {client.remaining()} remain. "
            "The run will stop at the cap rather than truncate silently.\n"
            "  Raise INDIAN_API_CALL_BUDGET only if the plan genuinely allows it."
        )

    if args.dry_run:
        by_endpoint: dict[str, int] = {}
        for _symbol, endpoint, stats, _params in todo:
            by_endpoint[f"{endpoint} {stats}".strip()] = (
                by_endpoint.get(f"{endpoint} {stats}".strip(), 0) + 1
            )
        print("\nBreakdown:")
        for key in sorted(by_endpoint):
            print(f"  {key:52} {by_endpoint[key]:>6}")
        print("\nDry run — nothing was spent.")
        return

    fetched = stored_snapshots = failures = 0
    for index, (symbol, endpoint, stats, params) in enumerate(todo, start=1):
        try:
            payload, from_cache, digest = client.get(endpoint, params)
        except BudgetExhausted as exc:
            print(f"\nSTOPPED at {index - 1}/{len(todo)}: {exc}")
            break
        except APIError as exc:
            failures += 1
            repo.record_exception(
                symbol=symbol, endpoint=endpoint, stats=stats,
                failure_type=exc.failure_type, http_status=exc.http_status,
                details=str(exc)[:1000],
            )
            print(f"  [{index}/{len(todo)}] FAIL {symbol} {endpoint} {stats} — "
                  f"{exc.failure_type} {exc.http_status or ''}")
            continue

        fetched += 1
        facts = facts_from(payload) if endpoint == "/historical_stats" else []

        if endpoint == "/historical_stats" and not facts:
            # A 200 with nothing parseable is a data fact about this issuer, not
            # a non-event — and it correlates with the companies worth noticing.
            repo.record_exception(
                symbol=symbol, endpoint=endpoint, stats=stats,
                failure_type="EMPTY_PAYLOAD",
                details="200 response contained no period-addressable rows",
            )
            failures += 1

        _snapshot, created = repo.save_snapshot(
            symbol=symbol, endpoint=endpoint, stats=stats,
            raw_sha256=digest,
            raw_storage_path=str(Path(client.cache_dir) / f"{digest}.json"),
            http_status=200, facts=facts,
        )
        stored_snapshots += int(created)

        if index % 25 == 0 or index == len(todo):
            print(f"  [{index}/{len(todo)}] {symbol} {endpoint} {stats} — "
                  f"{len(facts)} facts, {client.remaining()} calls left")

    print("\n" + "=" * 64)
    print(f"Fetched          : {fetched}")
    print(f"New snapshots    : {stored_snapshots}")
    print(f"Exceptions       : {failures} (stored, not dropped)")
    print(f"Calls spent      : {client.spent()} of {client.budget}")
    print(f"Remaining        : {client.remaining()}")

    summary = repo.coverage_summary()
    print(f"\nStore: {summary['symbols']} symbols, {summary['snapshots']} snapshots, "
          f"{summary['facts']} facts")
    if summary["exceptions"]:
        print(f"Exceptions by type: {json.dumps(summary['exceptions'])}")
    print(
        "\nRe-running this command is free for everything already stored. "
        "Inspect with: python3 -m scripts.analysis.quality_report --from-store"
    )


if __name__ == "__main__":
    main()
