# api/db/store.py
#
# SQLite-backed store for API state that lives outside the main Supabase DB:
#   - saved strategy configs  (strategies table)
#   - backtest run records    (backtest_runs table)
#   - paper trade sessions    (paper_sessions table)
#
# Uses WAL mode for safe concurrent reads from polling endpoints.

import json
import os
import sqlite3
from datetime import datetime, timedelta, timezone
from typing import Any, Optional

_DB_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "api_state.db")
_DB_PATH = os.path.abspath(_DB_PATH)


def _connect() -> sqlite3.Connection:
    conn = sqlite3.connect(_DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn


def init_db() -> None:
    """Create tables if they do not yet exist. Called once at startup."""
    with _connect() as conn:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS strategies (
                id          TEXT PRIMARY KEY,
                name        TEXT NOT NULL,
                config_json TEXT NOT NULL,
                created_at  TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS backtest_runs (
                run_id          TEXT PRIMARY KEY,
                strategy_id     TEXT,
                config_json     TEXT NOT NULL,
                status          TEXT NOT NULL DEFAULT 'queued',
                progress_pct    INTEGER NOT NULL DEFAULT 0,
                result_json     TEXT,
                error_msg       TEXT,
                created_at      TEXT NOT NULL,
                updated_at      TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS paper_sessions (
                session_id       TEXT PRIMARY KEY,
                strategy_id      TEXT NOT NULL,
                starting_capital REAL NOT NULL,
                start_date       TEXT NOT NULL,
                unlock_live_date TEXT NOT NULL,
                created_at       TEXT NOT NULL
            );

            -- Every LLM rebalance decision: regime, chosen weights, raw response.
            -- run_id is NULL for live market-API calls (not tied to a backtest).
            CREATE TABLE IF NOT EXISTS llm_weight_decisions (
                id               INTEGER PRIMARY KEY AUTOINCREMENT,
                run_id           TEXT,
                source           TEXT NOT NULL DEFAULT 'backtest',
                decided_at       TEXT NOT NULL,
                regime           TEXT NOT NULL,
                confidence       TEXT,
                weights_json     TEXT NOT NULL,
                snapshot_json    TEXT,
                raw_llm_response TEXT,
                model            TEXT,
                call_seq         INTEGER NOT NULL DEFAULT 0
            );

            -- Persisted regime state for cron runs (RegimeContextAgent + AdaptiveStrategySelector).
            -- Key format: "rca_history" (global) or "selector_<session_id>" (per session).
            CREATE TABLE IF NOT EXISTS regime_state (
                key        TEXT PRIMARY KEY,
                state_json TEXT NOT NULL,
                updated_at TEXT NOT NULL
            );

            -- Side-by-side LLM-adaptive vs fixed-weight baseline for each backtest.
            CREATE TABLE IF NOT EXISTS backtest_ab_results (
                run_id                TEXT PRIMARY KEY,
                adaptive_return_pct   REAL,
                adaptive_sharpe       REAL,
                adaptive_max_dd_pct   REAL,
                adaptive_num_trades   INTEGER,
                baseline_return_pct   REAL,
                baseline_sharpe       REAL,
                baseline_max_dd_pct   REAL,
                baseline_num_trades   INTEGER,
                alpha_return_pct      REAL,
                alpha_sharpe          REAL,
                llm_call_count        INTEGER NOT NULL DEFAULT 0,
                created_at            TEXT NOT NULL
            );
        """)


# ---------------------------------------------------------------------------
# Strategies
# ---------------------------------------------------------------------------

def save_strategy(strategy_id: str, name: str, config: dict) -> None:
    with _connect() as conn:
        conn.execute(
            "INSERT OR REPLACE INTO strategies (id, name, config_json, created_at) "
            "VALUES (?, ?, ?, ?)",
            (strategy_id, name, json.dumps(config), datetime.utcnow().isoformat()),
        )


def get_strategy(strategy_id: str) -> Optional[dict]:
    with _connect() as conn:
        row = conn.execute(
            "SELECT * FROM strategies WHERE id = ?", (strategy_id,)
        ).fetchone()
    if row is None:
        return None
    result = dict(row)
    result["config"] = json.loads(result.pop("config_json"))
    return result


# ---------------------------------------------------------------------------
# Backtest runs
# ---------------------------------------------------------------------------

def create_run(run_id: str, strategy_id: Optional[str], config: dict) -> None:
    now = datetime.utcnow().isoformat()
    with _connect() as conn:
        conn.execute(
            "INSERT INTO backtest_runs "
            "(run_id, strategy_id, config_json, status, progress_pct, created_at, updated_at) "
            "VALUES (?, ?, ?, 'queued', 0, ?, ?)",
            (run_id, strategy_id, json.dumps(config), now, now),
        )


def update_run_progress(run_id: str, pct: int) -> None:
    with _connect() as conn:
        conn.execute(
            "UPDATE backtest_runs SET progress_pct = ?, updated_at = ? WHERE run_id = ?",
            (pct, datetime.utcnow().isoformat(), run_id),
        )


def update_run_status(run_id: str, status: str) -> None:
    with _connect() as conn:
        conn.execute(
            "UPDATE backtest_runs SET status = ?, updated_at = ? WHERE run_id = ?",
            (status, datetime.utcnow().isoformat(), run_id),
        )


def complete_run(run_id: str, result: dict) -> None:
    with _connect() as conn:
        conn.execute(
            "UPDATE backtest_runs SET status = 'complete', progress_pct = 100, "
            "result_json = ?, updated_at = ? WHERE run_id = ?",
            (json.dumps(result), datetime.utcnow().isoformat(), run_id),
        )


def fail_run(run_id: str, error: str) -> None:
    with _connect() as conn:
        conn.execute(
            "UPDATE backtest_runs SET status = 'failed', error_msg = ?, updated_at = ? "
            "WHERE run_id = ?",
            (error, datetime.utcnow().isoformat(), run_id),
        )


def get_run(run_id: str) -> Optional[dict]:
    with _connect() as conn:
        row = conn.execute(
            "SELECT * FROM backtest_runs WHERE run_id = ?", (run_id,)
        ).fetchone()
    if row is None:
        return None
    result = dict(row)
    if result.get("result_json"):
        result["result"] = json.loads(result.pop("result_json"))
    else:
        result.pop("result_json", None)
        result["result"] = None
    result["config"] = json.loads(result.pop("config_json"))
    return result


# ---------------------------------------------------------------------------
# Paper trade sessions
# ---------------------------------------------------------------------------

def create_paper_session(
    session_id: str,
    strategy_id: str,
    starting_capital: float,
    start_date: str,
) -> None:
    unlock = (
        datetime.fromisoformat(start_date) + timedelta(days=44)
    ).strftime("%Y-%m-%d")
    with _connect() as conn:
        conn.execute(
            "INSERT OR REPLACE INTO paper_sessions "
            "(session_id, strategy_id, starting_capital, start_date, unlock_live_date, created_at) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            (
                session_id,
                strategy_id,
                starting_capital,
                start_date,
                unlock,
                datetime.utcnow().isoformat(),
            ),
        )


def get_paper_session(session_id: str) -> Optional[dict]:
    with _connect() as conn:
        row = conn.execute(
            "SELECT * FROM paper_sessions WHERE session_id = ?", (session_id,)
        ).fetchone()
    return dict(row) if row else None


def delete_strategy_cascade(strategy_id: str) -> None:
    """
    Delete a strategy and all related SQLite rows in dependency order:
      backtest_runs → llm_weight_decisions, backtest_ab_results
      paper_sessions
      strategies
    """
    with _connect() as conn:
        # Collect run IDs so we can cascade into llm/ab tables.
        run_ids = [
            row[0] for row in conn.execute(
                "SELECT run_id FROM backtest_runs WHERE strategy_id = ?", (strategy_id,)
            ).fetchall()
        ]
        if run_ids:
            placeholders = ",".join("?" * len(run_ids))
            conn.execute(
                f"DELETE FROM llm_weight_decisions WHERE run_id IN ({placeholders})", run_ids
            )
            conn.execute(
                f"DELETE FROM backtest_ab_results WHERE run_id IN ({placeholders})", run_ids
            )
            conn.execute(
                f"DELETE FROM backtest_runs WHERE run_id IN ({placeholders})", run_ids
            )
        conn.execute("DELETE FROM paper_sessions WHERE strategy_id = ?", (strategy_id,))
        conn.execute("DELETE FROM strategies WHERE id = ?", (strategy_id,))


# ---------------------------------------------------------------------------
# LLM weight decisions
# ---------------------------------------------------------------------------

def log_llm_decision(
    decided_at: str,
    regime: str,
    confidence: str,
    weights: dict,
    snapshot: dict,
    raw_llm_response: str,
    model: str,
    call_seq: int,
    run_id: Optional[str] = None,
    source: str = "backtest",
) -> None:
    """Record one LLM rebalance event."""
    # Only store the market-relevant subset of the snapshot to keep rows small.
    snapshot_slim = {
        k: snapshot.get(k)
        for k in ("pct_uptrend", "pct_downtrend", "avg_atr_pct", "broad_regime", "trend")
        if snapshot.get(k) is not None
    }
    with _connect() as conn:
        conn.execute(
            "INSERT INTO llm_weight_decisions "
            "(run_id, source, decided_at, regime, confidence, weights_json, "
            " snapshot_json, raw_llm_response, model, call_seq) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (
                run_id, source, decided_at, regime, confidence,
                json.dumps(weights), json.dumps(snapshot_slim),
                raw_llm_response, model, call_seq,
            ),
        )


def get_llm_decisions(run_id: Optional[str] = None, limit: int = 100) -> list[dict]:
    """Fetch LLM decisions, optionally filtered by run_id."""
    with _connect() as conn:
        if run_id:
            rows = conn.execute(
                "SELECT * FROM llm_weight_decisions WHERE run_id = ? ORDER BY id DESC LIMIT ?",
                (run_id, limit),
            ).fetchall()
        else:
            rows = conn.execute(
                "SELECT * FROM llm_weight_decisions ORDER BY id DESC LIMIT ?",
                (limit,),
            ).fetchall()
    results = []
    for row in rows:
        r = dict(row)
        r["weights"]  = json.loads(r.pop("weights_json"))
        r["snapshot"] = json.loads(r.pop("snapshot_json") or "{}")
        results.append(r)
    return results


# ---------------------------------------------------------------------------
# Backtest A/B comparison (LLM-adaptive vs fixed-weight baseline)
# ---------------------------------------------------------------------------

def save_ab_result(
    run_id: str,
    adaptive: dict,
    baseline: dict,
    llm_call_count: int,
) -> None:
    """
    Store side-by-side metrics.

    adaptive / baseline dicts expected keys:
        return_pct, sharpe, max_dd_pct, num_trades
    """
    alpha_return = round(
        (adaptive.get("return_pct") or 0) - (baseline.get("return_pct") or 0), 4
    )
    alpha_sharpe = round(
        (adaptive.get("sharpe") or 0) - (baseline.get("sharpe") or 0), 4
    )
    with _connect() as conn:
        conn.execute(
            "INSERT OR REPLACE INTO backtest_ab_results "
            "(run_id, adaptive_return_pct, adaptive_sharpe, adaptive_max_dd_pct, "
            " adaptive_num_trades, baseline_return_pct, baseline_sharpe, "
            " baseline_max_dd_pct, baseline_num_trades, "
            " alpha_return_pct, alpha_sharpe, llm_call_count, created_at) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (
                run_id,
                adaptive.get("return_pct"), adaptive.get("sharpe"),
                adaptive.get("max_dd_pct"), adaptive.get("num_trades"),
                baseline.get("return_pct"), baseline.get("sharpe"),
                baseline.get("max_dd_pct"), baseline.get("num_trades"),
                alpha_return, alpha_sharpe,
                llm_call_count,
                datetime.now(timezone.utc).isoformat(),
            ),
        )


def get_ab_result(run_id: str) -> Optional[dict]:
    with _connect() as conn:
        row = conn.execute(
            "SELECT * FROM backtest_ab_results WHERE run_id = ?", (run_id,)
        ).fetchone()
    return dict(row) if row else None


# ---------------------------------------------------------------------------
# Regime state persistence
# ---------------------------------------------------------------------------

def load_regime_state(key: str) -> Optional[dict]:
    """Load persisted regime state by key. Returns None if not found."""
    with _connect() as conn:
        row = conn.execute(
            "SELECT state_json FROM regime_state WHERE key = ?", (key,)
        ).fetchone()
    if row is None:
        return None
    return json.loads(row["state_json"])


def save_regime_state(key: str, state: dict) -> None:
    """Upsert persisted regime state for the given key."""
    with _connect() as conn:
        conn.execute(
            "INSERT OR REPLACE INTO regime_state (key, state_json, updated_at) "
            "VALUES (?, ?, ?)",
            (key, json.dumps(state, default=str), datetime.utcnow().isoformat()),
        )
