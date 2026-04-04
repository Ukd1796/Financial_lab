# api/routers/paper_trade.py
#
# Phase 2 — Paper trading session management.
# The actual signal generation still runs via run_signals.py (cron job at 3:35 PM IST).
# These endpoints expose the session state and live positions from the existing DB tables.
#
#   POST /api/paper-trade/start
#   GET  /api/paper-trade/{session_id}/dashboard
#   GET  /api/paper-trade/{session_id}/positions
#   GET  /api/paper-trade/{session_id}/signals
#   GET  /api/paper-trade/{session_id}/report/weekly

import uuid
from datetime import date, datetime, timedelta

from fastapi import APIRouter, Header, HTTPException
from sqlalchemy import select, and_

import api.db.store as store
from api.models.request import PaperTradeStartRequest
import api.services.regime_service as regime_svc
from app.core.database import SessionLocal
from app.data.models import LivePosition, SignalQueue

router = APIRouter()


# ---------------------------------------------------------------------------
# Helpers — read from Supabase (existing tables)
# ---------------------------------------------------------------------------

def _get_live_positions() -> list[dict]:
    """Read all rows from live_positions table."""
    session = SessionLocal()
    try:
        rows = session.execute(select(LivePosition)).scalars().all()
        return [
            {
                "symbol":        r.symbol,
                "quantity":      r.quantity,
                "average_price": r.average_price,
                "entry_date":    str(r.entry_date),
                "strategy":      r.strategy,
            }
            for r in rows
        ]
    finally:
        session.close()


def _get_signals_for_date(signal_date: date, session_id: str) -> list[dict]:
    """Read signal_queue rows for a specific date and paper session."""
    session = SessionLocal()
    try:
        rows = session.execute(
            select(SignalQueue).where(
                and_(
                    SignalQueue.signal_date == signal_date,
                    SignalQueue.session_id  == session_id,
                )
            )
        ).scalars().all()
        return [
            {
                "symbol":       r.symbol,
                "action":       r.action,
                "strategy":     r.strategy,
                "raw_price":    r.raw_price,
                "target_qty":   r.target_qty,
                "status":       r.status,
                "regime_label": r.regime_label,
                "notes":        r.notes,
                "created_at":   str(r.created_at),
            }
            for r in rows
        ]
    finally:
        session.close()


def _get_signals_range(start_date: date, end_date: date, session_id: str) -> list[dict]:
    """Read signal_queue rows between two dates (inclusive) for a paper session."""
    session = SessionLocal()
    try:
        rows = session.execute(
            select(SignalQueue).where(
                and_(
                    SignalQueue.signal_date >= start_date,
                    SignalQueue.signal_date <= end_date,
                    SignalQueue.session_id  == session_id,
                )
            )
        ).scalars().all()
        return [
            {
                "symbol":       r.symbol,
                "action":       r.action,
                "strategy":     r.strategy,
                "raw_price":    r.raw_price,
                "fill_price":   r.fill_price,
                "target_qty":   r.target_qty,
                "status":       r.status,
                "signal_date":  str(r.signal_date),
                "regime_label": r.regime_label,
                "weight":       r.weight,
            }
            for r in rows
        ]
    finally:
        session.close()


def _unrealised_pnl(positions: list[dict]) -> float:
    """
    Estimate unrealised PnL using last raw_price from signal_queue as a proxy.
    In production this should use a live price feed.
    """
    total = 0.0
    for p in positions:
        # Approximation: we don't have live prices here, skip per-position calc
        total += 0.0
    return total


def _resolve_session(session_id: str) -> dict:
    session = store.get_paper_session(session_id)
    if session is None:
        raise HTTPException(
            status_code=404, detail=f"Paper trade session '{session_id}' not found."
        )
    return session


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@router.post("/start", status_code=201)
def start_paper_trade(
    body: PaperTradeStartRequest,
    x_session_token: str = Header(default=""),
):
    """
    Activate paper trading for a saved strategy.
    Requires the strategy to exist (must have run at least one backtest first
    — enforced at the UI level; not enforced here to keep the API stateless).
    """
    # Strategy validation: try SQLite (API-created IDs like strat_xxxx).
    # Frontend-saved strategies live in a separate Supabase project and cannot be
    # validated here — the frontend passes strategy_name explicitly in that case.
    saved_strategy = store.get_strategy(body.strategy_id)

    session_id = f"pt_{uuid.uuid4().hex[:6]}"
    start_date = date.today().isoformat()

    unlock_date = (date.today() + timedelta(days=44)).isoformat()

    # Resolve strategy display name: body override → SQLite name → strategy_id fallback.
    strategy_name = (
        body.strategy_name
        or (saved_strategy.get("name") if saved_strategy else None)
        or body.strategy_id
    )

    # SQLite: persist session so /dashboard, /positions, /signals can resolve it.
    store.create_paper_session(
        session_id=session_id,
        strategy_id=body.strategy_id,
        starting_capital=body.starting_capital,
        start_date=start_date,
    )

    # paper_trade_sessions in Supabase is written by the frontend directly via
    # the Supabase JS client (useCreatePaperSession) — no mirror write needed here.

    return {
        "session_id":       session_id,
        "start_date":       start_date,
        "unlock_live_date": unlock_date,
    }


@router.get("/{session_id}/dashboard")
def get_dashboard(session_id: str):
    """
    Everything the paper trade dashboard needs in one call:
    portfolio value, open positions, today's signals, regime, day count.
    """
    paper_session = _resolve_session(session_id)
    start_dt = datetime.fromisoformat(paper_session["start_date"])
    day_count = (date.today() - start_dt.date()).days + 1

    positions = _get_live_positions()
    today_signals = _get_signals_for_date(date.today(), session_id)

    # Best-effort portfolio value: starting capital + unrealised PnL from positions
    portfolio_value = paper_session["starting_capital"]

    # Regime (cached — fast)
    try:
        regime_data = regime_svc.get_regime()
        regime = regime_data["regime"]
    except Exception:
        regime = "UNKNOWN"

    return {
        "session_id":        session_id,
        "strategy_id":       paper_session["strategy_id"],
        "start_date":        paper_session["start_date"],
        "day_count":         day_count,
        "days_until_live":   max(0, 30 - day_count),
        "portfolio_value":   portfolio_value,
        "open_positions":    len(positions),
        "todays_signals":    len(today_signals),
        "regime":            regime,
        "positions":         positions,
        "signals":           today_signals,
    }


@router.get("/{session_id}/positions")
def get_positions(session_id: str):
    """
    Open positions with unrealised P&L, strategy source, and days held.
    """
    _resolve_session(session_id)
    positions = _get_live_positions()
    today = date.today()

    result = []
    for p in positions:
        entry = date.fromisoformat(p["entry_date"]) if p["entry_date"] else today
        days_held = (today - entry).days
        result.append({
            **p,
            "days_held":       days_held,
            "unrealised_pnl":  None,   # requires live price — supply at UI layer
        })

    return {"session_id": session_id, "positions": result}


@router.get("/{session_id}/signals")
def get_signals(session_id: str):
    """
    Today's generated signals (BUY / SELL / PENDING / FILLED / CANCELLED) with reason.
    """
    _resolve_session(session_id)
    signals = _get_signals_for_date(date.today(), session_id)
    return {"session_id": session_id, "date": str(date.today()), "signals": signals}


@router.get("/{session_id}/report/weekly")
def get_weekly_report(session_id: str):
    """
    Weekly health report: period signals, filled trades, regime summary.
    """
    paper_session = _resolve_session(session_id)
    end_date   = date.today()
    start_date = end_date - timedelta(days=7)

    signals = _get_signals_range(start_date, end_date, session_id)

    buys_filled  = [s for s in signals if s["action"] == "BUY"  and s["status"] == "FILLED"]
    sells_filled = [s for s in signals if s["action"] == "SELL" and s["status"] == "FILLED"]
    pending      = [s for s in signals if s["status"] == "PENDING"]

    try:
        regime_data = regime_svc.get_regime()
        regime = regime_data["regime"]
    except Exception:
        regime = "UNKNOWN"

    start_dt = datetime.fromisoformat(paper_session["start_date"])
    day_count = (end_date - start_dt.date()).days + 1

    return {
        "session_id":      session_id,
        "week_start":      str(start_date),
        "week_end":        str(end_date),
        "day_count":       day_count,
        "regime":          regime,
        "total_signals":   len(signals),
        "buys_filled":     len(buys_filled),
        "sells_filled":    len(sells_filled),
        "pending":         len(pending),
        "notable_trades":  sells_filled[:10],   # last 10 completed exits
    }
