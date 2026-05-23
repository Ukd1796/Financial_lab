from dataclasses import dataclass, field
from typing import Dict


@dataclass
class Position:
    symbol: str
    quantity: float
    average_price: float
    atr_at_entry: float = 0.0
    high_watermark: float = 0.0  # highest price seen since entry; trailing stop trails this
    entry_date: object = None    # datetime of first fill; used by the ETF min-hold gate (None ⇒ ungated)


@dataclass
class Portfolio:
    cash: float
    positions: Dict[str, Position] = field(default_factory=dict)
    realized_pnl: float = 0.0

    def total_equity(self, current_prices: Dict[str, float]) -> float:
        equity = self.cash
        for symbol, position in self.positions.items():
            equity += position.quantity * current_prices.get(symbol, 0)
        return equity

    def unrealized_pnl(self, current_prices: Dict[str, float]) -> float:
        pnl = 0.0
        for symbol, position in self.positions.items():
            current_price = current_prices.get(symbol, 0)
            pnl += (current_price - position.average_price) * position.quantity
        return pnl

