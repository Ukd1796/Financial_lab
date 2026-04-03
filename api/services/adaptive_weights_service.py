# api/services/adaptive_weights_service.py
#
# Singleton wrapper around AdaptiveStrategySelector for the market API.
#
# The selector is instantiated once per process with all 5 strategies.
# It calls the OpenAI LLM at most once per rebalance_frequency_days (default 5).
# Filtering and floor-weight enforcement happen post-LLM so the model always
# reasons over a full universe and relative weights stay coherent.
#
# Fallback chain:
#   LLM weights → (if LLM fails) equal distribution across enabled strategies

from __future__ import annotations

from datetime import datetime, timezone

from app.meta.adaptive_selector import AdaptiveStrategySelector
from api.services.regime_service import get_raw_snapshot
import api.db.store as store

# Canonical name mapping (mirrors backtest_service.py)
_UI_TO_INTERNAL: dict[str, str] = {
    "trend-follow":   "DualMA",
    "breakout":       "Breakout",
    "quiet-breakout": "QuietBrk",
    "trend-pullback": "TrendPB",
    "mean-reversion": "RSI-MR",
}
_INTERNAL_TO_UI: dict[str, str] = {v: k for k, v in _UI_TO_INTERNAL.items()}
_ALL_INTERNALS: list[str] = list(_UI_TO_INTERNAL.values())  # insertion order = UI order

_selector: AdaptiveStrategySelector | None = None


def _market_api_callback(decided_at, regime, confidence, weights,
                          snapshot, raw_response, model):
    """Log live market-API LLM decisions to the DB (run_id=NULL)."""
    try:
        store.log_llm_decision(
            decided_at=decided_at.isoformat(),
            regime=regime,
            confidence=confidence,
            weights=weights,
            snapshot=snapshot,
            raw_llm_response=raw_response,
            model=model,
            call_seq=_selector.call_count if _selector else 0,
            run_id=None,
            source="market_api",
        )
    except Exception:
        pass


def _ensure_selector() -> AdaptiveStrategySelector:
    global _selector
    if _selector is None:
        _selector = AdaptiveStrategySelector(
            strategy_names=_ALL_INTERNALS,
            rebalance_frequency_days=5,
            model="gpt-4o-mini",
            verbose=False,
            on_rebalance=_market_api_callback,
        )
    return _selector


def get_adaptive_weights(
    enabled_ui_ids: list[str] | None = None,
    floor_map_ui: dict[str, float] | None = None,
) -> dict[str, float]:
    """
    Return LLM-driven, regime-aware capital weights keyed by UI strategy id.

    Parameters
    ----------
    enabled_ui_ids : UI strategy ids to include. None = all 5.
    floor_map_ui   : {ui_id: min_weight} — any weight below its floor is lifted,
                     then weights are renormalised to sum to 1.0.

    Returns
    -------
    dict  e.g. {"trend-follow": 0.35, "breakout": 0.30, ...}
    """
    selector = _ensure_selector()
    snapshot = get_raw_snapshot()

    # AdaptiveStrategySelector caches internally; LLM is called at most once per
    # rebalance_frequency_days. Returns equal distribution if LLM is unavailable.
    raw_internal: dict[str, float] = selector.rebalance(datetime.now(timezone.utc), snapshot)

    # Filter to requested strategies
    if enabled_ui_ids is not None:
        keep = {_UI_TO_INTERNAL[uid] for uid in enabled_ui_ids if uid in _UI_TO_INTERNAL}
        raw_internal = {k: v for k, v in raw_internal.items() if k in keep}

    if not raw_internal:
        return {}

    # Apply floor weights (lift then renormalise)
    if floor_map_ui:
        floor_internal = {
            _UI_TO_INTERNAL[uid]: w
            for uid, w in floor_map_ui.items()
            if uid in _UI_TO_INTERNAL
        }
        raw_internal = {k: max(v, floor_internal.get(k, 0.0)) for k, v in raw_internal.items()}

    total = sum(raw_internal.values())
    if total > 0:
        raw_internal = {k: round(v / total, 4) for k, v in raw_internal.items()}

    return {_INTERNAL_TO_UI[k]: v for k, v in raw_internal.items() if k in _INTERNAL_TO_UI}
