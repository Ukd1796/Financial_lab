from datetime import date
from app.data.providers.yfinance_provider import YFinanceProvider
from app.data.repository import MarketDataRepository

provider = YFinanceProvider()
repository = MarketDataRepository()

records = provider.fetch_ohlc(
    symbol="RELIANCE",
    start=date(2024, 1, 1),
    end=date(2024, 6, 1)
)

repository.bulk_upsert(records)
