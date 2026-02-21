from dataclasses import dataclass
from typing import Dict, Optional
from datetime import datetime


@dataclass
class MarketState:
    symbol: str
    timestamp: datetime
    latest_price: float
    previous_price: Optional[float]
    indicators: Dict[str, float]
    previous_indicators: Dict[str, float]

