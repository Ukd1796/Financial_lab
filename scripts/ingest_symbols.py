import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from datetime import date
from app.data.providers.yfinance_provider import YFinanceProvider
from app.data.repository import MarketDataRepository


# --- Nifty 50 ---
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

# --- Nifty Next 50 ---
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

# --- Nifty Midcap 50 ---
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

# Nifty 100 (Nifty 50 + Nifty Next 50) + Nifty Midcap 50 = 150 symbols
SYMBOLS = NIFTY_50 + NIFTY_NEXT_50 + NIFTY_MIDCAP_50

FULL_START_DATE = date(2015, 1, 1)   # used only for symbols with no data at all


def main():
    from datetime import timedelta

    provider   = YFinanceProvider()
    repository = MarketDataRepository()
    end_date   = date.today()

    # Per-symbol last date — fetch only the gap, not the full history again
    last_dates = repository.get_last_dates(SYMBOLS)

    print(f"Total symbols: {len(SYMBOLS)} | End date: {end_date}")
    print(f"  Already in DB: {len(last_dates)} symbols (will gap-fill)")
    print(f"  New symbols:   {len(SYMBOLS) - len(last_dates)} symbols (will fetch from {FULL_START_DATE})")

    failed = []

    for symbol in SYMBOLS:
        if symbol in last_dates:
            # DB stores timestamps as UTC; yfinance uses midnight IST (UTC+5:30).
            # e.g. 2026-02-27 00:00 IST → stored as 2026-02-26 18:30 UTC.
            # Convert back to IST to get the actual trading date, then add 1 day.
            last_ts = last_dates[symbol]
            ist_date = (last_ts + timedelta(hours=5, minutes=30)).date()
            start_date = ist_date + timedelta(days=1)
            if start_date >= end_date:
                print(f"  {symbol}: up to date ({last_dates[symbol].date()})")
                continue
        else:
            start_date = FULL_START_DATE

        print(f"  Fetching {symbol}: {start_date} → {end_date} ...", end=" ", flush=True)
        records = provider.fetch_ohlc(symbol=symbol, start=start_date, end=end_date)

        if not records:
            print("no data")
            failed.append(symbol)
            continue

        repository.bulk_upsert(records)
        print(f"{len(records)} records stored")

    if failed:
        print(f"\nFailed ({len(failed)}): {', '.join(failed)}")
    else:
        print("\nAll symbols up to date.")


if __name__ == "__main__":
    main()
