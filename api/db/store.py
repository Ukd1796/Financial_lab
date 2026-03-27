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
from datetime import datetime, timedelta
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
