# app/data/providers/yfinance_provider.py
import yfinance as yf
import pandas as pd
from datetime import date
from typing import List

from .base import MarketDataProvider, OHLCRecord


class YFinanceProvider(MarketDataProvider):

    def fetch_ohlc(
        self,
        symbol: str,
        start: date,
        end: date,
        interval: str = "1d"
    ) -> List[OHLCRecord]:

        # NSE symbols need .NS suffix
        ticker_symbol = f"{symbol}.NS"

        ticker = yf.Ticker(ticker_symbol)

        df = ticker.history(
            start=start,
            end=end,
            interval=interval,
            auto_adjust=False
        )

        if df.empty:
            return []

        records: List[OHLCRecord] = []

        for timestamp, row in df.iterrows():
            record = OHLCRecord(
                symbol=symbol,
                timestamp=timestamp.to_pydatetime(),
                open=float(row["Open"]),
                high=float(row["High"]),
                low=float(row["Low"]),
                close=float(row["Close"]),
                volume=float(row["Volume"]),
            )
            records.append(record)

        return records
