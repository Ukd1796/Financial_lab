# api/models/request.py
#
# Pydantic request schemas for all API endpoints.

from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import date


class StrategyEntry(BaseModel):
    id: str                               # UI strategy ID (e.g. "trend-follow")
    enabled: bool
    floor_weight: float = 0.0


class RiskConfig(BaseModel):
    risk_per_trade_pct: float = 0.5    # % of portfolio at risk per trade (e.g. 0.5 = 0.5%)
    max_position_pct: float = 10.0     # max single position size as % of capital (e.g. 10 = 10%)
    pause_threshold_pct: float = 35.0  # breadth circuit-breaker: pause BUY when >N% of universe
                                       # is in DOWNTREND — maps to RiskAgent.max_downtrend_pct/100
                                       # production default is 35 (pause when >35% in downtrend)
    capital_amount: float = 1_000_000


class StrategyConfigRequest(BaseModel):
    name: str
    universe: str = "nifty100"            # nifty50 | nifty100 | broad150
    strategies: List[StrategyEntry]
    risk: RiskConfig
    backtest_start: Optional[date] = None
    backtest_end: Optional[date] = None


class BacktestRunRequest(BaseModel):
    strategy_id: Optional[str] = None
    config: Optional[StrategyConfigRequest] = None


class PaperTradeStartRequest(BaseModel):
    strategy_id: str
    starting_capital: float = 1_000_000
    user_id: Optional[str] = None        # Supabase auth UID; optional for backwards-compat
    strategy_name: Optional[str] = None  # Display name; inferred from saved strategy if omitted
