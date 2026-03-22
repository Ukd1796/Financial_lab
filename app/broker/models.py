# app/broker/models.py
#
# Broker-layer data classes — returned by BrokerAdapter methods.
# Independent of the strategy/portfolio layer.

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class Order:
    order_id:   str
    symbol:     str
    action:     str             # BUY / SELL
    quantity:   int
    order_type: str             # MARKET / LIMIT
    status:     str             # PENDING / PLACED / FILLED / REJECTED / CANCELLED
    placed_at:  Optional[datetime] = None
    fill_price: Optional[float]    = None
    fill_qty:   Optional[int]      = None
    notes:      str                = ""


@dataclass
class BrokerPosition:
    symbol:        str
    quantity:      int
    average_price: float
    strategy:      str = ""     # populated from live_positions on reconciliation
