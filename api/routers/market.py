# api/routers/market.py
#
# Market data endpoints:
#   GET /api/market/regime           — current broad regime + breadth stats
#   GET /api/market/universe-stats   — active stock counts per universe tier
#   GET /api/market/strategy-weights — rule-based capital weights for current regime

from fastapi import APIRouter, HTTPException, Query
from typing import Optional

import api.services.regime_service as regime_svc

router = APIRouter()

# ---------------------------------------------------------------------------
# Rule-based strategy weights per regime
# (deterministic fallback; does not require OpenAI/LLM)
# ---------------------------------------------------------------------------
_REGIME_WEIGHTS: dict[str, dict] = {
    "BULL_CONFIRMED": {
        "trend-follow": 0.35, "breakout": 0.30,
        "quiet-breakout": 0.20, "trend-pullback": 0.15, "mean-reversion": 0.00,
    },
    "BULL_EARLY": {
        "trend-follow": 0.20, "breakout": 0.30,
        "quiet-breakout": 0.20, "trend-pullback": 0.20, "mean-reversion": 0.10,
    },
    "BULL_WATCH": {
        "trend-follow": 0.15, "breakout": 0.25,
        "quiet-breakout": 0.20, "trend-pullback": 0.20, "mean-reversion": 0.20,
    },
    "SIDEWAYS_CHOPPY": {
        "trend-follow": 0.10, "breakout": 0.20,
        "quiet-breakout": 0.10, "trend-pullback": 0.25, "mean-reversion": 0.35,
    },
    "TRANSITION_UP": {
        "trend-follow": 0.20, "breakout": 0.30,
        "quiet-breakout": 0.15, "trend-pullback": 0.15, "mean-reversion": 0.20,
    },
    "BEAR_WATCH": {
        "trend-follow": 0.15, "breakout": 0.20,
        "quiet-breakout": 0.10, "trend-pullback": 0.15, "mean-reversion": 0.40,
    },
    "BEAR_TRANSITION": {
        "trend-follow": 0.15, "breakout": 0.25,
        "quiet-breakout": 0.10, "trend-pullback": 0.10, "mean-reversion": 0.40,
    },
    "BEAR_CONFIRMED": {
        "trend-follow": 0.10, "breakout": 0.10,
        "quiet-breakout": 0.00, "trend-pullback": 0.10, "mean-reversion": 0.70,
    },
}

_REGIME_RATIONALE: dict[str, str] = {
    "BULL_CONFIRMED":  "Broad uptrend confirmed. Trend-follow and Breakout dominate. Mean-Reversion weight set to 0 — performs poorly in strong bull phases.",
    "BULL_EARLY":      "Early bull phase. Breakout and Quiet-Breakout lead. Mean-Reversion gets a small allocation as oversold bounces still occur.",
    "BULL_WATCH":      "Uptrend present but not accelerating. Balanced across momentum and mean-reversion strategies.",
    "SIDEWAYS_CHOPPY": "No dominant trend. Mean-Reversion and Trend-Pullback thrive in range-bound markets. Trend-Follow weight minimal.",
    "TRANSITION_UP":   "Early recovery from bear — breadth improving. Breakout and Mean-Reversion capture first moves. Trend-Follow begins rebuilding.",
    "BEAR_WATCH":      "Downtrend expanding. Mean-Reversion dominates with tight stops. Trend strategies reduce exposure.",
    "BEAR_TRANSITION": "Bear confirmed but breadth improving. Breakout allocated for first recovery longs. High Mean-Reversion weight for oversold bounces.",
    "BEAR_CONFIRMED":  "Deep bear. Only Mean-Reversion active (oversold bounces). All trend-following weight near zero to prevent catching falling knives.",
}


@router.get("/regime")
def get_regime():
    """
    Current market regime from RegimeContextAgent.
    Cached for up to 1 hour — the heaviest computation in the API.
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
def get_strategy_weights(
    regime: Optional[str] = Query(
        default=None,
        description="Override regime label. Uses live regime if omitted.",
    )
):
    """
    Rule-based capital weights per strategy for the given (or live) regime.
    """
    if regime is None:
        try:
            regime = regime_svc.get_regime()["regime"]
        except Exception as exc:
            raise HTTPException(status_code=503, detail=str(exc))

    weights   = _REGIME_WEIGHTS.get(regime, _REGIME_WEIGHTS["SIDEWAYS_CHOPPY"])
    rationale = _REGIME_RATIONALE.get(regime, "No specific guidance for this regime.")

    return {
        "regime":    regime,
        "weights":   weights,
        "rationale": rationale,
    }
