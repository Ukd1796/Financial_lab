# api/routers/paper_trade.py
#
# Phase 2 — Paper trading session management.
# Signal generation runs via api/run_paper_signals.py (cron at 3:45 PM IST).
# Positions are derived from FILLED signal_queue rows (session-scoped).
# live_positions table is no longer used.
#
#   POST /api/paper-trade/start
#   GET  /api/paper-trade/{session_id}/dashboard
#   GET  /api/paper-trade/{session_id}/positions
#   GET  /api/paper-trade/{session_id}/signals
#   GET  /api/paper-trade/{session_id}/report/weekly

import uuid
from datetime import date, datetime, timedelta

from fastapi import APIRouter, Header, HTTPException
from sqlalchemy import select, and_, text

import api.db.store as store
from api.models.request import PaperTradeStartRequest
import api.services.regime_service as regime_svc
from app.core.database import SessionLocal
from app.data.models import SignalQueue

router = APIRouter()


# ---------------------------------------------------------------------------
# Helpers — read from Supabase (existing tables)
# ---------------------------------------------------------------------------

def _get_positions_for_session(session_id: str) -> list[dict]:
    """Derive open positions from FILLED signal_queue entries for this session."""
    db = SessionLocal()
    try:
        fills = db.execute(
            select(SignalQueue)
            .where(SignalQueue.session_id == session_id)
            .where(SignalQueue.status == "FILLED")
            .order_by(SignalQueue.created_at.asc())
        ).scalars().all()
    finally:
        db.close()

    positions: dict[str, dict] = {}
    for fill in fills:
        if fill.action == "BUY":
            if fill.symbol in positions:
                p = positions[fill.symbol]
                new_qty = p["quantity"] + fill.fill_qty
                p["average_price"] = (
                    p["quantity"] * p["average_price"] + fill.fill_qty * fill.fill_price
                ) / new_qty
                p["quantity"] = new_qty
            else:
                positions[fill.symbol] = {
                    "symbol":        fill.symbol,
                    "quantity":      fill.fill_qty,
                    "average_price": fill.fill_price,
                    "entry_date":    str(fill.signal_date),
                    "strategy":      fill.strategy,
                }
        elif fill.action == "SELL" and fill.symbol in positions:
            remaining = positions[fill.symbol]["quantity"] - fill.fill_qty
            if remaining <= 0:
                del positions[fill.symbol]
            else:
                positions[fill.symbol]["quantity"] = remaining

    return list(positions.values())


def _get_latest_prices(symbols: list[str]) -> dict[str, float]:
    """
    Fetch the most recent EOD close price for each symbol from market_ohlc.
    Uses DISTINCT ON for a single efficient query.
    Returns {symbol: close_price}; missing symbols are absent from the dict.
    """
    if not symbols:
        return {}
    db = SessionLocal()
    try:
        rows = db.execute(
            text("""
                SELECT DISTINCT ON (symbol) symbol, close
                FROM market_ohlc
                WHERE symbol = ANY(:syms)
                ORDER BY symbol, timestamp DESC
            """),
            {"syms": symbols},
        ).fetchall()
        return {r.symbol: float(r.close) for r in rows}
    finally:
        db.close()


def _enrich_positions(positions: list[dict], prices: dict[str, float], today: date) -> list[dict]:
    """Add current_price, unrealised_pnl_abs, current_value, unrealised_pnl_pct to each position."""
    enriched = []
    for p in positions:
        entry = date.fromisoformat(p["entry_date"]) if p["entry_date"] else today
        current_price = prices.get(p["symbol"])
        entry_price   = p["average_price"]
        qty           = p["quantity"]

        if current_price is not None:
            unreal_abs = (current_price - entry_price) * qty
            unreal_pct = ((current_price - entry_price) / entry_price * 100) if entry_price else None
            cur_value  = current_price * qty
        else:
            unreal_abs = None
            unreal_pct = None
            cur_value  = None

        enriched.append({
            **p,
            "entry_price":        entry_price,
            "days_held":          (today - entry).days,
            "current_price":      current_price,
            "current_value":      cur_value,
            "unrealised_pnl_abs": unreal_abs,
            "unrealised_pnl_pct": round(unreal_pct, 2) if unreal_pct is not None else None,
        })
    return enriched


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
                "id":           r.order_id or f"{r.symbol}-{r.signal_date}",
                "symbol":       r.symbol,
                "action":       r.action,
                "strategy":     r.strategy,
                "entry_price":  r.raw_price,     # frontend expects entry_price
                "target_qty":   r.target_qty,
                "status":       r.status,
                "regime_label": r.regime_label,
                "notes":        r.notes,
                "date":         str(r.created_at),  # frontend expects date
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
                "entry_price":  r.raw_price,     # frontend expects entry_price
                "fill_price":   r.fill_price,
                "target_qty":   r.target_qty,
                "status":       r.status,
                "date":         str(r.signal_date),  # frontend expects date
                "regime_label": r.regime_label,
                "weight":       r.weight,
                "pnl_pct":      None,   # computed when exits are matched
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
    # 1. Try SQLite first (API-created sessions via POST /paper-trade/start)
    session = store.get_paper_session(session_id)
    if session:
        return session

    # 2. Fall back to Supabase paper_trade_sessions (sessions created directly,
    #    e.g. pt_ujjwal migrated from personal scripts, or frontend-created sessions)
    db = SessionLocal()
    try:
        row = db.execute(
            text(
                "SELECT session_id, strategy_id, strategy_name, starting_capital, created_at "
                "FROM paper_trade_sessions WHERE session_id = :sid"
            ),
            {"sid": session_id},
        ).fetchone()
    finally:
        db.close()

    if row is None:
        raise HTTPException(
            status_code=404, detail=f"Paper trade session '{session_id}' not found."
        )

    return {
        "session_id":       row.session_id,
        "strategy_id":      row.strategy_id,
        "strategy_name":    row.strategy_name,
        "starting_capital": row.starting_capital,
        "start_date":       str(row.created_at),   # created_at serves as session start
    }


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

    # day_count: use the earliest signal date for this session as the true start.
    # Falls back to start_date (session created_at) if no signals exist yet.
    db = SessionLocal()
    try:
        first_signal_row = db.execute(
            text("SELECT MIN(signal_date) AS first FROM signal_queue WHERE session_id = :sid"),
            {"sid": session_id},
        ).fetchone()
    finally:
        db.close()

    if first_signal_row and first_signal_row.first:
        effective_start = first_signal_row.first
    else:
        effective_start = datetime.fromisoformat(paper_session["start_date"]).date()

    day_count = (date.today() - effective_start).days + 1

    raw_positions = _get_positions_for_session(session_id)
    today_signals = _get_signals_for_date(date.today(), session_id)
    today         = date.today()

    # Fetch latest EOD prices for all open positions in one query
    symbols       = [p["symbol"] for p in raw_positions]
    prices        = _get_latest_prices(symbols)
    enriched      = _enrich_positions(raw_positions, prices, today)

    # Portfolio breakdown
    starting_capital = float(paper_session["starting_capital"])
    total_invested   = sum(p["average_price"] * p["quantity"] for p in raw_positions)
    # Realised PnL is not tracked separately yet; cash approximated from deployed cost.
    cash_balance     = starting_capital - total_invested
    total_unreal_abs = sum(
        p["unrealised_pnl_abs"] for p in enriched if p["unrealised_pnl_abs"] is not None
    ) or None
    portfolio_value  = (
        starting_capital + total_unreal_abs
        if total_unreal_abs is not None
        else starting_capital
    )

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
        "total_invested":    total_invested,
        "cash_balance":      cash_balance,
        "unrealised_pnl_abs": total_unreal_abs,
        "open_positions":    enriched,
        "position_count":    len(enriched),
        "todays_signals":    today_signals,
        "signal_count":      len(today_signals),
        "regime":            regime,
    }


@router.get("/{session_id}/positions")
def get_positions(session_id: str):
    """
    Open positions with current prices, unrealised P&L, strategy source, and days held.
    """
    _resolve_session(session_id)
    raw   = _get_positions_for_session(session_id)
    today = date.today()
    prices  = _get_latest_prices([p["symbol"] for p in raw])
    result  = _enrich_positions(raw, prices, today)
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
        "filled_buys":     len(buys_filled),    # renamed from buys_filled
        "filled_sells":    len(sells_filled),   # renamed from sells_filled
        "pending_signals": len(pending),        # renamed from pending
        "notable_trades":  sells_filled[:10],   # last 10 completed exits
    }
