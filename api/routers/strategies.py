# api/routers/strategies.py
#
# Strategy config persistence:
#   POST /api/strategies         — save a strategy, get back a server-side ID
#   GET  /api/strategies/{id}    — rehydrate a saved strategy config

import uuid
from datetime import datetime

from fastapi import APIRouter, HTTPException

import api.db.store as store
from api.models.request import StrategyConfigRequest

router = APIRouter()


@router.post("", status_code=201)
def create_strategy(body: StrategyConfigRequest):
    """
    Persist a strategy configuration and return a server-side ID.
    The returned `id` is used as the URL param for backtest runs and paper trade sessions.
    """
    strategy_id = f"strat_{uuid.uuid4().hex[:6]}"
    config_dict = body.model_dump(mode="json")

    store.save_strategy(strategy_id, body.name, config_dict)

    return {
        "id":         strategy_id,
        "created_at": datetime.utcnow().isoformat() + "Z",
    }


@router.get("/{strategy_id}")
def get_strategy(strategy_id: str):
    """
    Return the full strategy config for the given ID.
    Response shape matches the POST /api/strategies request body plus `id` and `created_at`.
    """
    record = store.get_strategy(strategy_id)
    if record is None:
        raise HTTPException(status_code=404, detail=f"Strategy '{strategy_id}' not found.")

    return {
        "id":         record["id"],
        "created_at": record["created_at"] + "Z",
        **record["config"],
    }
