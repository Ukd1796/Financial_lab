# app/data/providers/base.py

from abc import ABC, abstractmethod
from datetime import date
from typing import List
from dataclasses import dataclass
from datetime import datetime


@dataclass
class OHLCRecord:
    symbol: str
    timestamp: datetime
    open: float
    high: float
    low: float
    close: float
    volume: float


class MarketDataProvider(ABC):
    """
    Base interface for all market data providers.
    """

    @abstractmethod
    def fetch_ohlc(
        self,
        symbol: str,
        start: date,
        end: date,
        interval: str = "1d"
    ) -> List[OHLCRecord]:
        """
        Fetch OHLC data for a symbol between start and end dates.
        Must return normalized OHLCRecord list.
        """
        pass
