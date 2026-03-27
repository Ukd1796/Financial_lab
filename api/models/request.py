# api/models/request.py
#
# Pydantic request schemas for all API endpoints.

from typing import List, Optional
from pydantic import BaseModel, Field


class StrategyEntry(BaseModel):
    id: str                               # UI strategy ID (e.g. "trend-follow")
    enabled: bool
    floor_weight: float = 0.0


class RiskConfig(BaseModel):
    risk_per_trade_pct: float = 0.5
    max_position_pct: float = 10.0
    pause_threshold_pct: float = 5.0
    capital_amount: float = 1_000_000


class StrategyConfigRequest(BaseModel):
    name: str
    universe: str = "nifty100"            # nifty50 | nifty100 | broad150
    strategies: List[StrategyEntry]
    risk: RiskConfig


class BacktestRunRequest(BaseModel):
    strategy_id: Optional[str] = None
    config: Optional[StrategyConfigRequest] = None


class PaperTradeStartRequest(BaseModel):
    strategy_id: str
    starting_capital: float = 1_000_000
