"""Does the vendor still serve companies that died? Decides if the lane is viable.

The red-flag work needs features **and** labels for the same names.  Bhavcopy
gives labels for everyone, including the 1,002 ISINs that stopped trading.
indianapi is built from current listings, so it may serve nothing at all for
those — in which case a model would learn what *surviving* companies look like
while being scored against failures it has never seen.  That would not be a
tuning problem; it would invalidate the lane.

So this measures one number: **feature coverage on the failure population**.

Two controls make the number mean something:

* **Size-matched living companies.**  Dead names are small, and a vendor may
  simply cover small companies poorly.  Without a matched control, thin coverage
  of small caps would be misread as survivorship.  Controls are drawn from the
  same traded-value decile, measured at each name's last session, from the
  bhavcopy cache — free.
* **Stratified by exit year.**  Coverage may be fine for last year's exits and
  zero for 2019's.  A single pooled percentage would hide that, and it changes
  what the data can support.

Usage::

    PYTHONPATH=. finance/bin/python3 -m scripts.analysis.probe_survivorship --dry-run
    PYTHONPATH=. finance/bin/python3 -m scripts.analysis.probe_survivorship --dead 150 --controls 100
"""

from __future__ import annotations

import argparse
import json
import math
import random
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path

from dotenv import load_dotenv

from app.analysis.delisting import (
    STATUS_ACTIVE,
    CachedBhavcopyClient,
    collect_monthly_snapshots,
)

# Fixed so the sample is reproducible and cannot be re-drawn until it flatters.
SAMPLE_SEED = 20260812


def traded_value(row: dict) -> float | None:
    try:
        value = float(row.get("TOTTRDVAL") or 0.0)
    except (TypeError, ValueError):
        return None
    return value if value > 0 else None


def size_bucket(value: float | None) -> int | None:
    """Decile-ish bucket on a log scale; matching is within a bucket."""
    if not value or value <= 0:
        return None
    return int(math.log10(value))


def load_last_traded_values(snapshots) -> dict[str, tuple[float | None, date]]:
    """Each ISIN's traded value at its final observed session. Costs nothing."""
    ordered = sorted(snapshots, key=lambda s: s.session)
    out: dict[str, tuple[float | None, date]] = {}
    for snapshot in ordered:
        for isin, row in snapshot.rows.items():
            out[isin] = (traded_value(row), snapshot.session)
    return out


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--dead", type=int, default=150, help="Dead ISINs to sample")
    parser.add_argument("--controls", type=int, default=100, help="Living controls to sample")
    parser.add_argument("--window-start", type=date.fromisoformat, default=date(2018, 1, 1))
    parser.add_argument("--window-end", type=date.fromisoformat, default=date(2026, 8, 11))
    parser.add_argument("--cache-dir", default="data/analysis/bhavcopy")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--json", type=Path, default=Path("data/analysis/survivorship_probe.json"))
    args = parser.parse_args()

    load_dotenv()

    from app.analysis.database import initialize_schema
    from app.analysis.indianapi_client import APIError, BudgetExhausted, IndianAPIClient
    from app.analysis.models import DelistingOutcome
    from app.analysis.repository import AnalysisRepository
    from app.event_research.nse_client import NSEResearchClient
    from sqlalchemy import select

    from app.analysis.database import new_session

    initialize_schema()
    repo = AnalysisRepository()

    session = new_session()
    try:
        outcomes = list(
            session.execute(
                select(DelistingOutcome).where(
                    DelistingOutcome.window_start == args.window_start,
                    DelistingOutcome.window_end == args.window_end,
                )
            ).scalars()
        )
    finally:
        session.close()

    if not outcomes:
        raise SystemExit(
            "no outcome labels for this window — run "
            "scripts.analysis.build_delisting_labels first"
        )

    # Size proxy comes from the cached bhavcopies; no downloads, no API calls.
    bhav = CachedBhavcopyClient(NSEResearchClient(request_delay_seconds=0.1), args.cache_dir)
    snapshots = collect_monthly_snapshots(bhav, args.window_start, args.window_end)
    sizes = load_last_traded_values(snapshots)

    dead = [o for o in outcomes if o.status != STATUS_ACTIVE]
    living = [o for o in outcomes if o.status == STATUS_ACTIVE]

    rng = random.Random(SAMPLE_SEED)

    # Stratify the dead sample by exit year so a year-dependent cliff is visible.
    by_year: dict[int, list] = defaultdict(list)
    for o in dead:
        by_year[o.last_seen.year].append(o)
    years = sorted(by_year)
    per_year = max(1, args.dead // max(1, len(years)))

    dead_sample: list = []
    for year in years:
        pool = sorted(by_year[year], key=lambda o: o.isin)
        dead_sample.extend(rng.sample(pool, min(per_year, len(pool))))
    dead_sample = dead_sample[: args.dead]

    # Match controls to the dead sample's size distribution.
    wanted = Counter(size_bucket(sizes.get(o.isin, (None, None))[0]) for o in dead_sample)
    living_by_bucket: dict[int | None, list] = defaultdict(list)
    for o in living:
        living_by_bucket[size_bucket(sizes.get(o.isin, (None, None))[0])].append(o)

    control_sample: list = []
    scale = args.controls / max(1, len(dead_sample))
    for bucket, count in wanted.items():
        pool = sorted(living_by_bucket.get(bucket, []), key=lambda o: o.isin)
        take = min(len(pool), max(1, round(count * scale)))
        if pool:
            control_sample.extend(rng.sample(pool, take))
    control_sample = control_sample[: args.controls]

    planned = len(dead_sample) + len(control_sample)
    client = IndianAPIClient()

    print(f"Dead ISINs in window : {len(dead)}   living: {len(living)}")
    print(f"Dead sample          : {len(dead_sample)} (stratified over {len(years)} exit years)")
    print(f"Control sample       : {len(control_sample)} (size-matched, living)")
    print(f"Planned calls        : {planned}")
    print(f"Budget               : {client.spent()} spent, {client.remaining()} remaining")

    if args.dry_run:
        print("\nDead sample by exit year:")
        for year in years:
            n = sum(1 for o in dead_sample if o.last_seen.year == year)
            print(f"  {year}  {n:>4}")
        print("\nDry run — nothing spent.")
        return

    if planned > client.remaining():
        raise SystemExit(
            f"{planned} calls needed, {client.remaining()} remaining. "
            "Lower --dead/--controls rather than raising the cap."
        )

    def measure(group: str, sample: list) -> list[dict]:
        results = []
        for index, o in enumerate(sample, start=1):
            try:
                payload, cached, digest = client.get(
                    "/historical_stats", {"stock_name": o.symbol, "stats": "quarter_results"}
                )
            except BudgetExhausted as exc:
                print(f"  STOPPED: {exc}")
                break
            except APIError as exc:
                repo.record_exception(
                    symbol=o.symbol, endpoint="/historical_stats", stats="quarter_results",
                    failure_type=exc.failure_type, http_status=exc.http_status,
                    details=f"{group} survivorship probe: {exc}"[:1000],
                )
                results.append({"group": group, "symbol": o.symbol, "isin": o.isin,
                                "status": o.status, "exit_year": o.last_seen.year,
                                "served": False, "quarters": 0,
                                "failure": f"{exc.failure_type}:{exc.http_status}"})
                continue

            from app.analysis.sources import parse_transposed

            quarters = len(parse_transposed(payload))
            if quarters == 0:
                repo.record_exception(
                    symbol=o.symbol, endpoint="/historical_stats", stats="quarter_results",
                    failure_type="EMPTY_PAYLOAD",
                    details=f"{group} survivorship probe: 200 with no period rows",
                )
            results.append({"group": group, "symbol": o.symbol, "isin": o.isin,
                            "status": o.status, "exit_year": o.last_seen.year,
                            "served": quarters > 0, "quarters": quarters,
                            "cached": cached, "sha256": digest})
            if index % 25 == 0:
                served = sum(1 for r in results if r["served"])
                print(f"  [{index}/{len(sample)}] {group}: {served} served so far, "
                      f"{client.remaining()} calls left")
        return results

    print("\nProbing dead names ...")
    dead_results = measure("dead", dead_sample)
    print("\nProbing living controls ...")
    control_results = measure("control", control_sample)

    all_results = dead_results + control_results

    def rate(rows):
        return (sum(1 for r in rows if r["served"]) / len(rows)) if rows else 0.0

    print("\n" + "=" * 68)
    print(f"{'group':<12}{'n':>5}{'served':>9}{'coverage':>11}{'median qtrs':>13}")
    for group, rows in (("dead", dead_results), ("control", control_results)):
        if not rows:
            continue
        served = [r for r in rows if r["served"]]
        med = sorted(r["quarters"] for r in served)[len(served) // 2] if served else 0
        print(f"{group:<12}{len(rows):>5}{len(served):>9}{rate(rows):>10.0%}{med:>13}")

    print(f"\nCoverage on dead names, by exit year")
    print(f"  {'year':<8}{'n':>5}{'served':>9}{'coverage':>11}")
    for year in years:
        rows = [r for r in dead_results if r["exit_year"] == year]
        if rows:
            served = sum(1 for r in rows if r["served"])
            print(f"  {year:<8}{len(rows):>5}{served:>9}{served / len(rows):>10.0%}")

    gap = rate(control_results) - rate(dead_results)
    print(f"\nCoverage gap (control - dead): {gap:+.0%}")
    print(
        "  A gap near zero means the vendor keeps delisted companies and the "
        "disaster lane is viable.\n"
        "  A large gap means features exist only for survivors — the lane cannot "
        "be trained or validated\n  historically, and only the forward run can support it."
    )

    args.json.parent.mkdir(parents=True, exist_ok=True)
    args.json.write_text(json.dumps(all_results, indent=2, default=str))
    print(f"\nWrote {args.json}")
    print(f"Calls spent: {client.spent()} of {client.budget}   remaining {client.remaining()}")


if __name__ == "__main__":
    main()
