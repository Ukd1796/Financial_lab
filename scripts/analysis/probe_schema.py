"""Spend ~30 calls once to make every later parser change free.

This is the highest-leverage spend in the ingestion plan.  It captures one raw
payload of every vocabulary the backfill will use, writes them as test
fixtures, and reports their structure.  Afterwards every parser can be written
and regression-tested offline against real payloads at zero further cost.

It also answers four things the published documentation does not:

1. Where ``stock_id`` comes from.  ``/stock_target_price`` and
   ``/stock_forecasts`` take ``stock_id``, not ``stock_name``, so ``/stock``
   probably has to be fetched first — which decides the backfill's ordering.
2. The ``/stock_forecasts`` enum values.  A rejected request usually names the
   values it will accept, so a deliberate miss is cheaper than guessing later
   across 500 symbols.
3. Whether promoter **pledge** percentage is in the shareholding payload.
   Promoter holding is; pledge is a separate disclosure and may be absent.
4. Whether ``/statement`` duplicates ``/historical_stats``.  If it does, the
   backfill drops it and saves 500 calls.

Usage::

    PYTHONPATH=. finance/bin/python3 -m scripts.analysis.probe_schema --dry-run
    PYTHONPATH=. finance/bin/python3 -m scripts.analysis.probe_schema
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from dotenv import load_dotenv

from app.analysis.sources import HISTORICAL_STATS

# Two unrelated large caps: a payload shape that holds for both is unlikely to
# be a per-issuer quirk.
PROBE_SYMBOLS = ("RELIANCE", "TCS")

FIXTURE_DIR = Path("tests/fixtures/indianapi")

# Deliberately narrow.  The price-derived endpoints (/trending, /price_shockers,
# /NSE_most_active, /historical_data, /fetch_52_week_high_low_data) are omitted:
# OQ6 established that no price-derived feature carries forward signal here, so
# sampling them would spend calls on a lane already falsified.
NO_PARAM_PROBES = ("/ipo",)


def describe(payload: object, depth: int = 0) -> str:
    """One-line shape summary — enough to see the schema without dumping it."""
    if isinstance(payload, dict):
        keys = list(payload)
        head = ", ".join(map(str, keys[:6]))
        more = f" (+{len(keys) - 6} more)" if len(keys) > 6 else ""
        inner = ""
        if keys and depth < 1:
            first = payload[keys[0]]
            inner = f"\n{'  ' * (depth + 1)}[{keys[0]}] -> {describe(first, depth + 1)}"
        return f"dict({len(keys)}) {{{head}{more}}}{inner}"
    if isinstance(payload, list):
        if not payload:
            return "list(0)"
        return f"list({len(payload)}) of {describe(payload[0], depth + 1)}"
    text = str(payload)
    return f"{type(payload).__name__}({text[:40]})"


def find_key(payload: object, needle: str, path: str = "") -> list[str]:
    """Every path whose key contains ``needle`` — used to locate stock_id."""
    hits: list[str] = []
    if isinstance(payload, dict):
        for key, value in payload.items():
            here = f"{path}.{key}" if path else str(key)
            if needle.lower() in str(key).lower():
                hits.append(f"{here} = {str(value)[:60]}")
            hits.extend(find_key(value, needle, here))
    elif isinstance(payload, list) and payload:
        hits.extend(find_key(payload[0], needle, f"{path}[0]"))
    return hits


def build_probes(stock_ids: dict[str, str]) -> list[tuple[str, dict, str]]:
    """The probe list, in dependency order."""
    probes: list[tuple[str, dict, str]] = []

    # /stock first: it is the likely source of stock_id for the two endpoints
    # that need one, and it also carries the industry label the sector
    # adjustment needs.
    for symbol in PROBE_SYMBOLS:
        probes.append(("/stock", {"name": symbol}, f"profile+industry+stock_id: {symbol}"))

    for symbol in PROBE_SYMBOLS:
        for stats in HISTORICAL_STATS:
            probes.append(
                ("/historical_stats", {"stock_name": symbol, "stats": stats}, f"{stats}: {symbol}")
            )

    for symbol in PROBE_SYMBOLS:
        probes.append(("/corporate_actions", {"stock_name": symbol}, f"actions: {symbol}"))
    probes.append(
        ("/recent_announcements", {"stock_name": PROBE_SYMBOLS[0]}, "announcements (text lane)")
    )

    # Undocumented enum.  One accepted guess plus one deliberate miss: the
    # rejection usually enumerates the valid values, which is cheaper than
    # discovering them across 500 symbols.
    probes.append(
        ("/statement", {"stock_name": PROBE_SYMBOLS[0], "stats": "balancesheet"},
         "/statement overlap with historical_stats?")
    )
    probes.append(
        ("/statement", {"stock_name": PROBE_SYMBOLS[0], "stats": "__enumerate__"},
         "deliberate miss to enumerate `stats`")
    )

    probes.append(("/industry_search", {"query": "software"}, "sector map, many names per call"))

    for endpoint in NO_PARAM_PROBES:
        probes.append((endpoint, {}, "no-param sample"))

    return probes


def forecast_probes(stock_id: str) -> list[tuple[str, dict, str]]:
    """Only runnable once /stock has yielded a stock_id."""
    return [
        ("/stock_target_price", {"stock_id": stock_id}, "analyst targets"),
        (
            "/stock_forecasts",
            {
                "stock_id": stock_id,
                "measure_code": "EPS",
                "period_type": "Annual",
                "data_type": "Estimates",
                "age": "Current",
            },
            "consensus EPS estimates (the forward-looking axis)",
        ),
        (
            "/stock_forecasts",
            {
                "stock_id": stock_id,
                "measure_code": "__enumerate__",
                "period_type": "Annual",
                "data_type": "Estimates",
                "age": "Current",
            },
            "deliberate miss to enumerate measure_code",
        ),
    ]


def run_probe(client, endpoint, params, note, results, *, save_fixture=True):
    from app.analysis.indianapi_client import APIError, BudgetExhausted

    label = f"{endpoint} {json.dumps(params, sort_keys=True)}"
    try:
        payload, from_cache, digest = client.get(endpoint, params)
    except BudgetExhausted as exc:
        print(f"  STOP  {label}\n        {exc}")
        results.append({"endpoint": endpoint, "params": params, "status": "BUDGET"})
        return None
    except APIError as exc:
        # A rejection is a result, not a crash: 422 bodies usually name the
        # accepted enum values, which is exactly what two of these probes want.
        print(f"  FAIL  {label}\n        {exc.failure_type} {exc.http_status or ''} {exc}")
        results.append({
            "endpoint": endpoint, "params": params, "status": "ERROR",
            "failure_type": exc.failure_type, "http_status": exc.http_status,
            "detail": str(exc)[:400],
        })
        return None

    tag = "cache" if from_cache else "fetch"
    print(f"  OK    {label}  [{tag}]\n        {note}\n        {describe(payload)}")
    results.append({
        "endpoint": endpoint, "params": params, "status": "OK",
        "from_cache": from_cache, "sha256": digest, "shape": describe(payload),
    })

    if save_fixture:
        name = endpoint.strip("/") + "__" + "_".join(
            str(v) for k, v in sorted(params.items())
        )
        safe = "".join(c if c.isalnum() or c in "-_" else "_" for c in name)[:90]
        (FIXTURE_DIR / f"{safe}.json").write_text(json.dumps(payload, indent=1, sort_keys=True))
    return payload


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--dry-run", action="store_true",
                        help="List the probes and their cost; spend nothing")
    parser.add_argument("--json", type=Path, help="Write the structural report here")
    args = parser.parse_args()

    load_dotenv()

    from app.analysis.database import initialize_schema
    from app.analysis.indianapi_client import IndianAPIClient

    probes = build_probes({})
    total = len(probes) + len(forecast_probes("<id>"))

    if args.dry_run:
        print(f"Probe plan — {total} calls maximum (cache hits cost nothing)\n")
        for endpoint, params, note in probes + forecast_probes("<discovered>"):
            print(f"  {endpoint:24} {json.dumps(params, sort_keys=True)[:70]:72} {note}")
        print(f"\nTotal: {total} calls. Nothing was spent.")
        return

    url = initialize_schema()
    FIXTURE_DIR.mkdir(parents=True, exist_ok=True)
    client = IndianAPIClient()

    print(f"Store    : {url}")
    print(f"Fixtures : {FIXTURE_DIR}")
    print(f"Budget   : {client.spent()} spent, {client.remaining()} remaining "
          f"of {client.budget}")
    print(f"Plan     : up to {total} calls\n")

    results: list[dict] = []
    payloads: dict[str, object] = {}

    for endpoint, params, note in probes:
        payload = run_probe(client, endpoint, params, note, results)
        if payload is not None and endpoint == "/stock":
            payloads[params["name"]] = payload

    # stock_id has to be discovered before the two endpoints that require it.
    stock_id = None
    for symbol, payload in payloads.items():
        hits = find_key(payload, "id")
        if hits:
            print(f"\n  stock_id candidates in /stock[{symbol}]:")
            for hit in hits[:12]:
                print(f"    {hit}")
            for hit in hits:
                if hit.split(" = ")[0].lower().endswith(("companyid", "stock_id", "id")):
                    stock_id = hit.split(" = ", 1)[1].strip()
                    break
        if stock_id:
            break

    if stock_id:
        print(f"\n  using stock_id={stock_id!r}\n")
        for endpoint, params, note in forecast_probes(stock_id):
            run_probe(client, endpoint, params, note, results)
    else:
        print("\n  no stock_id found in /stock — forecasts/target_price probes skipped.")
        print("  Inspect the saved /stock fixture to locate the identifier.\n")
        results.append({"endpoint": "/stock_forecasts", "status": "SKIPPED_NO_STOCK_ID"})

    print("\n" + "=" * 72)
    ok = sum(1 for r in results if r["status"] == "OK")
    billed = sum(1 for r in results if r.get("status") == "OK" and not r.get("from_cache"))
    print(f"Probes OK        : {ok}/{len(results)}")
    print(f"Calls billed     : {billed}")
    print(f"Budget remaining : {client.remaining()} of {client.budget}")

    errors = [r for r in results if r["status"] == "ERROR"]
    if errors:
        print("\nRejections (read these — they usually name the valid enum values):")
        for r in errors:
            print(f"  {r['endpoint']} {r.get('http_status')} :: {r.get('detail', '')[:200]}")

    report = args.json or Path("data/analysis/probe_report.json")
    report.parent.mkdir(parents=True, exist_ok=True)
    report.write_text(json.dumps(results, indent=2, default=str))
    print(f"\nWrote {report}")
    print("Fixtures are now offline test inputs — re-parsing costs zero calls.")


if __name__ == "__main__":
    main()
