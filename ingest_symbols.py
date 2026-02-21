from datetime import date
from app.data.providers.yfinance_provider import YFinanceProvider
from app.data.repository import MarketDataRepository



SYMBOLS = [
    "RELIANCE",
    "TCS",
    "INFY",
    "HDFCBANK",
    "ICICIBANK",
    "ITC",
    "SBIN",
    "BHARTIARTL",
    "ASIANPAINT",
    "AXISBANK",
    "MARUTI",
    "HCLTECH",
    "WIPRO",
    "BAJFINANCE",
    "KOTAKBANK",
    "ULTRACEMCO",
    "TITAN",
    "SUNPHARMA",
    "NESTLEIND"
]

START_DATE = date(2015, 1, 1)
END_DATE = date(2024, 6, 1)


def main():

    provider = YFinanceProvider()
    repository = MarketDataRepository()

    for symbol in SYMBOLS:

        print(f"\nFetching data for {symbol}...")

        records = provider.fetch_ohlc(
            symbol=symbol,
            start=START_DATE,
            end=END_DATE
        )

        if not records:
            print(f"No data found for {symbol}")
            continue

        repository.bulk_upsert(records)

        print(f"Stored {len(records)} records for {symbol}")


if __name__ == "__main__":
    main()
