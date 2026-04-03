# api/routers/market.py
#
# Market data endpoints:
#   GET  /api/market/regime                — current broad regime + breadth stats
#   GET  /api/market/universe-stats        — active stock counts per universe tier
#   GET  /api/market/strategy-weights      — LLM-driven weights for all 5 strategies
#   POST /api/market/strategy-weights      — LLM-driven weights filtered to enabled strategies
#   GET  /api/market/llm-decision-history  — recent live-market LLM weight decisions

from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from pydantic import BaseModel

import api.services.regime_service as regime_svc
import api.services.adaptive_weights_service as adaptive_svc
import api.db.store as store

router = APIRouter()

# ---------------------------------------------------------------------------
# Hardcoded fallback weights — used ONLY when the LLM / regime service fails.
# Not the primary source of truth: AdaptiveStrategySelector drives live weights.
# ---------------------------------------------------------------------------
_FALLBACK_WEIGHTS: dict[str, dict] = {
    "BULL_CONFIRMED":  {"trend-follow": 0.35, "breakout": 0.30, "quiet-breakout": 0.20, "trend-pullback": 0.15, "mean-reversion": 0.00},
    "BULL_EARLY":      {"trend-follow": 0.20, "breakout": 0.30, "quiet-breakout": 0.20, "trend-pullback": 0.20, "mean-reversion": 0.10},
    "BULL_WATCH":      {"trend-follow": 0.15, "breakout": 0.25, "quiet-breakout": 0.20, "trend-pullback": 0.20, "mean-reversion": 0.20},
    "SIDEWAYS_CHOPPY": {"trend-follow": 0.10, "breakout": 0.20, "quiet-breakout": 0.10, "trend-pullback": 0.25, "mean-reversion": 0.35},
    "TRANSITION_UP":   {"trend-follow": 0.20, "breakout": 0.30, "quiet-breakout": 0.15, "trend-pullback": 0.15, "mean-reversion": 0.20},
    "BEAR_WATCH":      {"trend-follow": 0.15, "breakout": 0.20, "quiet-breakout": 0.10, "trend-pullback": 0.15, "mean-reversion": 0.40},
    "BEAR_TRANSITION": {"trend-follow": 0.15, "breakout": 0.25, "quiet-breakout": 0.10, "trend-pullback": 0.10, "mean-reversion": 0.40},
    "BEAR_CONFIRMED":  {"trend-follow": 0.10, "breakout": 0.10, "quiet-breakout": 0.00, "trend-pullback": 0.10, "mean-reversion": 0.70},
}

_FALLBACK_RATIONALE: dict[str, str] = {
    "BULL_CONFIRMED":  "Broad uptrend confirmed. Trend-follow and Breakout dominate.",
    "BULL_EARLY":      "Early bull phase. Breakout and Quiet-Breakout lead.",
    "BULL_WATCH":      "Uptrend present but not accelerating. Balanced allocation.",
    "SIDEWAYS_CHOPPY": "No dominant trend. Mean-Reversion and Trend-Pullback thrive.",
    "TRANSITION_UP":   "Early recovery from bear — breadth improving.",
    "BEAR_WATCH":      "Downtrend expanding. Mean-Reversion dominates.",
    "BEAR_TRANSITION": "Bear confirmed but breadth improving.",
    "BEAR_CONFIRMED":  "Deep bear. Only Mean-Reversion active for oversold bounces.",
}


# ---------------------------------------------------------------------------
# Request / response models
# ---------------------------------------------------------------------------

class StrategyConfig(BaseModel):
    id: str
    floor_weight: float = 0.0


class StrategyWeightsRequest(BaseModel):
    regime: Optional[str] = None          # ignored — kept for API compatibility
    enabled_strategies: Optional[list[StrategyConfig]] = None


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@router.get("/regime")
def get_regime():
    """
    Current market regime from RegimeContextAgent.
    Cached for up to 1 hour.
    """
    try:
        return regime_svc.get_regime()
    except Exception as exc:
        raise HTTPException(status_code=503, detail=str(exc))


@router.get("/universe-stats")
def get_universe_stats():
    """
    Active stock count per universe tier (nifty50 / nifty100 / broad150).
    Shares the same cache as /regime.
    """
    try:
        return regime_svc.get_universe_stats()
    except Exception as exc:
        raise HTTPException(status_code=503, detail=str(exc))


@router.get("/strategy-weights")
def get_strategy_weights():
    """
    LLM-driven capital weights for all 5 strategies based on the current regime.

    Uses AdaptiveStrategySelector (OpenAI gpt-4o-mini). The selector rebalances
    at most once per 5 trading days; subsequent calls return the cached result.
    Falls back to a rule-based table if the LLM or regime service is unavailable.
    """
    try:
        weights = adaptive_svc.get_adaptive_weights()
        regime  = regime_svc.get_regime()["regime"]
        return {
            "regime":    regime,
            "weights":   weights,
            "rationale": "Weights computed by AdaptiveStrategySelector (LLM-driven, regime-aware).",
            "source":    "llm",
        }
    except Exception:
        # Fallback: rule-based lookup
        try:
            regime = regime_svc.get_regime()["regime"]
        except Exception as exc:
            raise HTTPException(status_code=503, detail=str(exc))

        weights   = dict(_FALLBACK_WEIGHTS.get(regime, _FALLBACK_WEIGHTS["SIDEWAYS_CHOPPY"]))
        rationale = _FALLBACK_RATIONALE.get(regime, "No specific guidance for this regime.")
        return {
            "regime":    regime,
            "weights":   weights,
            "rationale": rationale,
            "source":    "fallback",
        }


@router.post("/strategy-weights")
def post_strategy_weights(body: StrategyWeightsRequest):
    """
    LLM-driven weights filtered to the caller's enabled strategies,
    with floor-weight constraints enforced.

    Body:
      enabled_strategies — list of {id, floor_weight}
                           Omit to get weights for all 5 strategies.

    Response adds a `source` field: "llm" or "fallback".
    """
    enabled_ids: list[str] | None = None
    floor_map:   dict[str, float] | None = None

    if body.enabled_strategies:
        enabled_ids = [s.id for s in body.enabled_strategies]
        floor_map   = {s.id: s.floor_weight for s in body.enabled_strategies if s.floor_weight > 0}

    try:
        weights = adaptive_svc.get_adaptive_weights(
            enabled_ui_ids=enabled_ids,
            floor_map_ui=floor_map or None,
        )
        regime = regime_svc.get_regime()["regime"]
        return {
            "regime":    regime,
            "weights":   weights,
            "rationale": "Weights computed by AdaptiveStrategySelector (LLM-driven, regime-aware).",
            "source":    "llm",
        }
    except Exception:
        # Fallback: rule-based lookup filtered to enabled strategies
        try:
            regime = regime_svc.get_regime()["regime"]
        except Exception as exc:
            raise HTTPException(status_code=503, detail=str(exc))

        base = dict(_FALLBACK_WEIGHTS.get(regime, _FALLBACK_WEIGHTS["SIDEWAYS_CHOPPY"]))

        if enabled_ids:
            base = {k: v for k, v in base.items() if k in enabled_ids}
            if floor_map:
                base = {k: max(v, floor_map.get(k, 0.0)) for k, v in base.items()}
            total = sum(base.values())
            if total > 0:
                base = {k: round(v / total, 4) for k, v in base.items()}

        rationale = _FALLBACK_RATIONALE.get(regime, "No specific guidance for this regime.")
        return {
            "regime":    regime,
            "weights":   base,
            "rationale": rationale,
            "source":    "fallback",
        }


@router.get("/llm-decision-history")
def get_llm_decision_history(limit: int = Query(default=50, le=200)):
    """
    Recent LLM weight decisions made by the live market strategy-weights endpoint.
    Only populated when OPENAI_API_KEY is set and an actual LLM call was made.
    """
    decisions = store.get_llm_decisions(run_id=None, limit=limit)
    return {"decisions": decisions}
