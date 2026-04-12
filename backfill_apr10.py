#!/usr/bin/env python3
# backfill_apr10.py
#
# One-off: fetch April 10 2026 OHLC for symbols that have stuck April 9 signals,
# so recover_stuck_orders.py can fill them at April 10's open price.
# Delete this script after running.

from datetime import date
from dotenv import load_dotenv
load_dotenv()

from app.data.providers.yfinance_provider import YFinanceProvider
from app.data.repository import MarketDataRepository

# Symbols with signal_date=2026-04-09 that need April 10 data to fill
SYMBOLS = ["BHEL", "HFCL", "KAJARIACER", "HINDALCO"]

def main():
    provider = YFinanceProvider()
    repo     = MarketDataRepository()

    start = date(2026, 4, 10)
    end   = date(2026, 4, 11)   # yfinance end is exclusive

    print(f"Fetching OHLC for {start} ...")
    all_records = []

    for symbol in SYMBOLS:
        records = provider.fetch_ohlc(symbol, start=start, end=end)
        if records:
            print(f"  {symbol}: {len(records)} record(s), open={records[0].open}")
            all_records.extend(records)
        else:
            print(f"  {symbol}: NO DATA returned by yfinance (market may have been closed)")

    if all_records:
        repo.bulk_upsert(all_records)
        print(f"\nInserted {len(all_records)} record(s) into market_ohlc.")
        print("Now run:  python recover_stuck_orders.py")
    else:
        print("\nNo data fetched. April 10 may have been a market holiday not in NSECalendar.")


if __name__ == "__main__":
    main()
