from dataclasses import dataclass
from datetime import datetime


@dataclass
class Trade:
    symbol: str
    entry_price: float
    exit_price: float
    quantity: float
    pnl: float
    entry_date: datetime
    exit_date: datetime

