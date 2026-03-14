# app/data/providers/yfinance_provider.py

import yfinance as yf
from datetime import date
from typing import List

from app.data.models import MarketDataProvider, OHLCRecord


class YFinanceProvider(MarketDataProvider):
    """
    Fetches OHLC data from Yahoo Finance for NSE-listed stocks.
    Appends .NS suffix automatically for Indian equities.
    """

    def fetch_ohlc(
        self,
        symbol: str,
        start: date,
        end: date,
        interval: str = "1d"
    ) -> List[OHLCRecord]:

        ticker_symbol = f"{symbol}.NS"

        ticker = yf.Ticker(ticker_symbol)
        df = ticker.history(
            start=start.isoformat(),
            end=end.isoformat(),
            interval=interval,
            auto_adjust=True,
        )

        if df.empty:
            return []

        records = []
        for timestamp, row in df.iterrows():
            records.append(OHLCRecord(
                symbol=symbol,
                timestamp=timestamp.to_pydatetime(),
                open=float(row["Open"]),
                high=float(row["High"]),
                low=float(row["Low"]),
                close=float(row["Close"]),
                volume=float(row["Volume"]),
            ))

        return records
    
