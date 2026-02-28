from dataclasses import dataclass
from typing import Dict, Optional


@dataclass
class MetaDecision:
    action: str  # "INCREASE", "REDUCE", "MAINTAIN"
    allocation_multiplier: float
    reasoning: str
    diagnostics: Optional[Dict] = None