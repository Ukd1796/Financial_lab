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

START_DATE = date(2015, 1, 1)
END_DATE = date(2026, 2, 28)


def main():

    provider = YFinanceProvider()
    repository = MarketDataRepository()

    already_ingested = repository.get_ingested_symbols()
    pending = [s for s in SYMBOLS if s not in already_ingested]
    skipped = len(SYMBOLS) - len(pending)

    print(f"Total symbols: {len(SYMBOLS)} | Already in DB: {skipped} | To fetch: {len(pending)}")

    if not pending:
        print("Nothing to ingest — all symbols already in database.")
        return

    failed = []

    for symbol in pending:

        print(f"\nFetching data for {symbol}...")

        records = provider.fetch_ohlc(
            symbol=symbol,
            start=START_DATE,
            end=END_DATE
        )

        if not records:
            print(f"No data found for {symbol}")
            failed.append(symbol)
            continue

        repository.bulk_upsert(records)

        print(f"Stored {len(records)} records for {symbol}")

    if failed:
        print(f"\nFailed symbols ({len(failed)}): {', '.join(failed)}")
    else:
        print("\nAll pending symbols ingested successfully.")


if __name__ == "__main__":
    main()
