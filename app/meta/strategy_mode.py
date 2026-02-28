from enum import Enum
from dataclasses import dataclass



class StrategyMode(Enum):
    AGGRESSIVE = "AGGRESSIVE"
    BALANCED = "BALANCED"
    DEFENSIVE = "DEFENSIVE"

@dataclass
class ModePolicy:
    max_position_pct: float
    atr_multiplier: float
    allowed_regimes: list