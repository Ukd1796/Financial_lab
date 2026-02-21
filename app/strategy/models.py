from dataclasses import dataclass
from typing import Optional


@dataclass
class Decision:
    symbol: str
    action: str  # BUY / SELL / HOLD
    quantity: Optional[float] = None
    confidence: float = 1.0
    reasoning: str = ""
