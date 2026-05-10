from dataclasses import dataclass
from typing import Optional


@dataclass
class Decision:
    symbol: str
    action: str  # BUY / SELL / HOLD
    quantity: Optional[float] = None
    confidence: float = 1.0
    reasoning: str = ""
    weight: float = 1.0        # strategy capital weight (set by MultiStrategyRouter / AdaptiveSelector)
    source: str = ""           # strategy name that generated this decision (set by MultiStrategyRouter)
    atr_at_entry: float = 0.0  # ATR recorded when the BUY was approved (set by RiskAgent)
