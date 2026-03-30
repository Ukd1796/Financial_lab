# api/routers/backtest.py
#
# Backtest execution:
#   POST /api/backtest/run        — queue a backtest run, return run_id immediately
#   GET  /api/backtest/{run_id}   — poll for status / retrieve full results

import asyncio
import uuid
from datetime import datetime

from fastapi import APIRouter, HTTPException

import api.db.store as store
from api.models.request import BacktestRunRequest
from api.services.backtest_service import execute_backtest

router = APIRouter()


@router.post("/run", status_code=202)
async def run_backtest(body: BacktestRunRequest):
    """
    Start a backtest run in the background.
    Returns a `run_id` immediately — poll GET /api/backtest/{run_id} for results.

    Accepts either:
      { "strategy_id": "strat_abc123" }        — loads saved config from DB
      { "config": { ...inline config... } }    — uses config directly
    """
    # Resolve config
    config: dict | None = None

    if body.strategy_id:
        record = store.get_strategy(body.strategy_id)
        if record is None:
            raise HTTPException(
                status_code=404,
                detail=f"Strategy '{body.strategy_id}' not found.",
            )
        config = record["config"]
        config["strategy_id"] = body.strategy_id

    elif body.config:
        config = body.config.model_dump(mode="json")
    else:
        raise HTTPException(
            status_code=422,
            detail="Provide either 'strategy_id' or 'config' in the request body.",
        )

    run_id = f"bt_{uuid.uuid4().hex[:6]}"
    store.create_run(run_id, body.strategy_id, config)

    # Kick off the heavy computation in a thread so the event loop stays free.
    asyncio.get_running_loop().run_in_executor(
        None, execute_backtest, run_id, config
    )

    return {
        "run_id":            run_id,
        "status":            "queued",
        "estimated_seconds": 20,
    }


@router.get("/{run_id}")
def get_backtest(run_id: str):
    """
    Poll for backtest status.

    While running:
      { "run_id": "...", "status": "running", "progress_pct": 42 }

    On completion:
      { "run_id": "...", "status": "complete", "summary": {...}, "equity_curve": [...], ... }
    """
    record = store.get_run(run_id)
    if record is None:
        raise HTTPException(status_code=404, detail=f"Run '{run_id}' not found.")

    status = record["status"]

    if status in ("queued", "running"):
        return {
            "run_id":       run_id,
            "status":       status,
            "progress_pct": record.get("progress_pct", 0),
        }

    if status == "failed":
        return {
            "run_id":     run_id,
            "status":     "failed",
            "error_msg":  record.get("error_msg", "unknown error"),
        }

    # status == "complete"
    result = record.get("result", {})
    return {
        "run_id":          run_id,
        "status":          "complete",
        "strategy_id":     result.get("strategy_id"),
        "config_snapshot": result.get("config_snapshot", {}),
        "summary":         result.get("summary", {}),
        "equity_curve":    result.get("equity_curve", []),
        "period_breakdown": result.get("period_breakdown", []),
        "trade_log":        result.get("trade_log", []),
        "ai_narrative":     result.get("ai_narrative", {}),
    }
