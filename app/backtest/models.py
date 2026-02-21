from dataclasses import dataclass
from datetime import datetime


@dataclass
class BacktestResult:
    date: datetime
    equity: float
    cash: float
    realized_pnl: float
