# api/routers/strategies.py
#
# Strategy config persistence:
#   POST /api/strategies         — save a strategy, get back a server-side ID
#   GET  /api/strategies/{id}    — rehydrate a saved strategy config

import uuid
from datetime import datetime

from fastapi import APIRouter, HTTPException
from sqlalchemy import text

import api.db.store as store
from api.models.request import StrategyConfigRequest
from app.core.database import SessionLocal

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


@router.delete("/{strategy_id}", status_code=200)
def delete_strategy(strategy_id: str):
    """
    Cascade-delete a strategy and all related data:
      SQLite  — backtest_runs, llm_weight_decisions, backtest_ab_results, paper_sessions, strategies
      Supabase — signal_queue (via session_ids), paper_trade_sessions, backtest_results

    The caller (frontend) is responsible for deleting user_strategies from Supabase
    using the user's JWT (RLS-protected table).
    """
    # SQLite cascade
    store.delete_strategy_cascade(strategy_id)

    # Supabase cascade — signal_queue must be deleted BEFORE paper_trade_sessions
    # so we can still resolve the session_ids.
    try:
        db = SessionLocal()
        db.execute(
            text("""
                DELETE FROM signal_queue
                WHERE session_id IN (
                    SELECT session_id FROM paper_trade_sessions WHERE strategy_id = :sid
                )
            """),
            {"sid": strategy_id},
        )
        db.execute(
            text("DELETE FROM paper_trade_sessions WHERE strategy_id = :sid"),
            {"sid": strategy_id},
        )
        db.execute(
            text("DELETE FROM backtest_results WHERE strategy_id = :sid"),
            {"sid": strategy_id},
        )
        db.commit()
    except Exception as exc:
        print(f"[strategies] Supabase cascade delete failed: {exc}")
    finally:
        db.close()

    return {"deleted": strategy_id}
