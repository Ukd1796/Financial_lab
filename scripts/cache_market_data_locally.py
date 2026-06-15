"""
scripts/cache_market_data_locally.py
====================================

One-time sync: pull all OHLC data from Supabase B and persist locally as
SQLite so subsequent backtests don't repeatedly hit the quota.

Defaults cache the full 2014-01-01 → 2026-12-31 window for the 150 broad-
universe stocks (Nifty 50 + Next 50 + Midcap 50) PLUS the 17 ETFs used by
the ETF profile. Single bulk pull, batched to stay under Supabase's pooler
limits. Writes to data_cache/market_ohlc.sqlite.

USAGE
-----
First run (initial sync):
    PYTHONHASHSEED=0 finance/bin/python3 -m scripts.cache_market_data_locally

Refresh (replace existing data — use sparingly):
    PYTHONHASHSEED=0 finance/bin/python3 -m scripts.cache_market_data_locally --refresh

Show stats on existing cache without syncing:
    PYTHONHASHSEED=0 finance/bin/python3 -m scripts.cache_market_data_locally --stats

After running once, every subsequent backtest (run_experiments.py,
run_ujjwal_baseline.py, scripts/diagnose_choppy_regime.py) automatically
serves from the local file via the OHLCCache.warm_all() short-circuit.

REFRESHING
----------
The cache is intentionally static — backtests are reproducible because the
underlying data doesn't drift. When new market data is needed (e.g. after
running the daily ingest cron for a few weeks), re-run this script with
--refresh. Or delete data_cache/market_ohlc.sqlite to force a full pull.
"""

from __future__ import annotations

import argparse
import sys
import time
from datetime import datetime

# Load .env before importing app modules so DATABASE_URL is set at import time
from dotenv import load_dotenv
load_dotenv()

from app.data.local_cache import (
    DEFAULT_CACHE_PATH,
    cache_exists,
    save_records,
    stats,
)
from app.data.repository import MarketDataRepository


# ---------------------------------------------------------------------------
# Universe to cache — must cover everything any backtest might request.
# Stocks: NIFTY_50 + NIFTY_NEXT_50 + NIFTY_MIDCAP_50 (mirrors run_experiments.py)
# ---------------------------------------------------------------------------
NIFTY_50 = [
    "RELIANCE", "TCS", "HDFCBANK", "BHARTIARTL", "ICICIBANK",
    "INFY", "SBIN", "HINDUNILVR", "ITC", "LT",
    "BAJFINANCE", "HCLTECH", "KOTAKBANK", "AXISBANK", "ASIANPAINT",
    "MARUTI", "SUNPHARMA", "TITAN", "ULTRACEMCO", "WIPRO",
    "NTPC", "POWERGRID", "NESTLEIND", "M&M", "TECHM",
    "BAJAJFINSV", "ADANIENT", "ADANIPORTS", "COALINDIA", "ONGC",
    "GRASIM", "TMCV", "TATASTEEL", "JSWSTEEL", "HINDALCO",
    "BRITANNIA", "DRREDDY", "DIVISLAB", "BPCL", "HDFCLIFE",
    "SBILIFE", "CIPLA", "APOLLOHOSP", "EICHERMOT", "HEROMOTOCO",
    "INDUSINDBK", "BAJAJ-AUTO", "TATACONSUM", "SHRIRAMFIN", "BEL",
]
NIFTY_NEXT_50 = [
    "ADANIGREEN", "AMBUJACEM", "ATGL", "BAJAJHLDNG", "BANKBARODA",
    "BERGEPAINT", "BOSCHLTD", "CANBK", "CHOLAFIN", "COLPAL",
    "DABUR", "DLF", "GODREJCP", "GODREJPROP", "HAVELLS",
    "HDFCAMC", "ICICIGI", "ICICIPRULI", "INDUSTOWER", "INDIGO",
    "IRCTC", "JSWENERGY", "LTIM", "LUPIN", "MUTHOOTFIN",
    "NAUKRI", "OFSS", "PFC", "PIDILITIND", "PNB",
    "RECLTD", "SIEMENS", "TATACOMM", "TATAPOWER", "TORNTPHARM",
    "TORNTPOWER", "UNIONBANK", "VEDL", "ETERNAL", "ZYDUSLIFE",
    "MARICO", "MOTHERSON", "OBEROIRLTY", "PAGEIND", "PERSISTENT",
    "POLYCAB", "SBICARD", "TRENT", "UPL", "VOLTAS",
]
NIFTY_MIDCAP_50 = [
    "ABB", "ABCAPITAL", "ABFRL", "ALKEM", "ASHOKLEY",
    "ASTRAL", "AUROPHARMA", "BALKRISIND", "BANKINDIA", "BHEL",
    "CANFINHOME", "CROMPTON", "CUMMINSIND", "DEEPAKNTR", "DIXON",
    "FEDERALBNK", "GLENMARK", "GLAXO", "GMRAIRPORT", "GNFC",
    "HFCL", "HINDPETRO", "IDFCFIRSTB", "INDIANB", "INDHOTEL",
    "JUBLFOOD", "KAJARIACER", "KPITTECH", "LALPATHLAB", "LAURUSLABS",
    "LICHSGFIN", "LTF", "MAXHEALTH", "METROPOLIS", "MFSL",
    "MPHASIS", "MRF", "NAVINFLUOR", "NMDC", "PIIND",
    "RAYMOND", "SAIL", "SCHAEFFLER", "SUNTV", "SUPREMEIND",
    "THERMAX", "TIINDIA", "TVSMOTOR", "WHIRLPOOL", "ZEEL",
]
BROAD_UNIVERSE = NIFTY_50 + NIFTY_NEXT_50 + NIFTY_MIDCAP_50

ALL_SYMBOLS = list(set(BROAD_UNIVERSE))

# Window — wide enough for any backtest period including the 200-day warm-up
# buffers that strategies need before period start.
CACHE_START = datetime(2014, 1, 1)
CACHE_END   = datetime(2026, 12, 31)

# Batch size — same as OHLCCache.warm_all default. Bigger = fewer trips but
# closer to Supabase pooler row-limit; smaller = more trips but safer.
BATCH_SIZE = 25


def _print_stats() -> None:
    s = stats(DEFAULT_CACHE_PATH)
    if not s["exists"]:
        print(f"\n  Cache file does not exist at {DEFAULT_CACHE_PATH}")
        print("  Run without --stats to perform initial sync.\n")
        return
    print(f"\n  Local cache: {s['path']}")
    print(f"  Size:        {s['size_mb']} MB")
    print(f"  Rows:        {s['rows']:,}")
    print(f"  Symbols:     {s['symbols']}")
    print(f"  Date range:  {s['first_date']} → {s['last_date']}\n")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument(
        "--refresh", action="store_true",
        help="Replace existing rows for each symbol (use after long ingest gaps).",
    )
    parser.add_argument(
        "--stats", action="store_true",
        help="Print current cache stats and exit (no Supabase pull).",
    )
    args = parser.parse_args()

    if args.stats:
        _print_stats()
        return

    if cache_exists(DEFAULT_CACHE_PATH) and not args.refresh:
        print("\n  Local cache already exists. Current state:")
        _print_stats()
        print("  Use --refresh to re-sync (replaces existing rows).")
        print("  Use --stats to inspect without pulling.\n")
        return

    repo = MarketDataRepository()

    print(f"\n  Local cache target: {DEFAULT_CACHE_PATH}")
    print(f"  Window:             {CACHE_START.date()} → {CACHE_END.date()}")
    print(f"  Symbols:            {len(ALL_SYMBOLS)}")
    print(f"  Mode:               {'REFRESH (replace existing)' if args.refresh else 'INITIAL SYNC'}")
    print(f"  Batch size:         {BATCH_SIZE}")
    print()

    batches = [
        ALL_SYMBOLS[i:i + BATCH_SIZE]
        for i in range(0, len(ALL_SYMBOLS), BATCH_SIZE)
    ]
    total_inserted = 0
    total_rows_seen = 0
    skipped_symbols: list[str] = []

    t_start = time.time()
    for idx, batch in enumerate(batches, 1):
        print(f"  Batch {idx}/{len(batches)} ({len(batch)} symbols)... ",
              end="", flush=True)
        records = repo.get_ohlc_bulk(batch, CACHE_START, CACHE_END)
        rows_this_batch = sum(len(v) for v in records.values())
        total_rows_seen += rows_this_batch

        # Track symbols with no data so the user knows
        for sym in batch:
            if sym not in records or not records[sym]:
                skipped_symbols.append(sym)

        inserted = save_records(
            records, DEFAULT_CACHE_PATH, replace_existing=args.refresh
        )
        total_inserted += inserted
        print(f"{rows_this_batch:>6,} rows fetched, {inserted:>6,} inserted")

    elapsed = time.time() - t_start
    print()
    print(f"  Done in {elapsed:.1f}s")
    print(f"  Total rows fetched:  {total_rows_seen:,}")
    print(f"  Total rows inserted: {total_inserted:,}")
    if skipped_symbols:
        print(f"  Symbols with NO data ({len(skipped_symbols)}): "
              f"{', '.join(skipped_symbols[:8])}"
              f"{'...' if len(skipped_symbols) > 8 else ''}")
    print()
    _print_stats()
    print("  ✓ Local cache ready. Subsequent backtests will serve from disk.")
    print("    (Delete data_cache/market_ohlc.sqlite or use --refresh to re-sync.)\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n  Interrupted. Partial cache may be present — re-run to resume.\n")
        sys.exit(130)
