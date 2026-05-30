from dataclasses import dataclass
from datetime import datetime


@dataclass
class BacktestResult:
    date: datetime
    equity: float
    cash: float
    realized_pnl: float
    

@dataclass
class Trade:
    symbol: str
    entry_price: float
    exit_price: float
    quantity: float
    pnl: float
    entry_date: datetime
    exit_date: datetime
    exit_reason: str = ""   # "atr_stop" | "strategy" — set by BacktestEngine
    strategy: str = ""      # owning strategy at BUY time — set by BacktestEngine

