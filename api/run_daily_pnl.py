#!/usr/bin/env python3
# api/run_daily_pnl.py
#
# Daily P&L summary push notification — runs at 10:15 UTC (15:45 IST) on trading days,
# just before market close so users see how their portfolio is positioned for the day.
#
# Cron (add to the same crontab as signals/orders):
#   15 10 * * 1-5 cd /path/to/Financial_lab && python -m api.run_daily_pnl >> logs/daily_pnl.log 2>&1
#
# What it does per active session:
#   1. Reconstruct open positions from FILLED signal_queue rows
#   2. Fetch latest EOD close price from market_ohlc for each held symbol
#   3. Compute unrealized P&L (absolute + %)
#   4. Send push notification with a compact summary

import sys
from datetime import date, datetime

from dotenv import load_dotenv
load_dotenv()

from sqlalchemy import select, text

from app.core.database import SessionLocal
from app.core.push import send_push_to_session_user
from app.data.calendar import NSECalendar
from app.data.models import SignalQueue


def _load_active_sessions() -> list[dict]:
    db = SessionLocal()
    try:
        rows = db.execute(text(
            "SELECT session_id, strategy_name, starting_capital "
            "FROM paper_trade_sessions WHERE status = 'active'"
        )).fetchall()
        return [dict(r._mapping) for r in rows]
    except Exception as exc:
        print(f"  [Config] Could not read paper_trade_sessions ({exc})")
        return []
    finally:
        db.close()


def _get_positions(session_id: str) -> list[dict]:
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
                new_qty = p["qty"] + fill.fill_qty
                p["avg"] = (p["qty"] * p["avg"] + fill.fill_qty * fill.fill_price) / new_qty
                p["qty"] = new_qty
            else:
                positions[fill.symbol] = {"qty": fill.fill_qty, "avg": fill.fill_price}
        elif fill.action == "SELL" and fill.symbol in positions:
            remaining = positions[fill.symbol]["qty"] - fill.fill_qty
            if remaining <= 0:
                del positions[fill.symbol]
            else:
                positions[fill.symbol]["qty"] = remaining

    return [{"symbol": sym, **pos} for sym, pos in positions.items()]


def _get_cash_balance(session_id: str, starting_capital: float) -> float:
    """Compute true cash balance by replaying all filled transactions."""
    db = SessionLocal()
    try:
        fills = db.execute(
            select(SignalQueue)
            .where(SignalQueue.session_id == session_id)
            .where(SignalQueue.status == "FILLED")
        ).scalars().all()
    finally:
        db.close()
    return starting_capital + sum(
        (f.fill_price * f.fill_qty) * (1 if f.action == "SELL" else -1)
        for f in fills
        if f.fill_price and f.fill_qty
    )


def _latest_prices(symbols: list[str]) -> dict[str, float]:
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


def _summarise_session(sess: dict) -> None:
    sid = sess["session_id"]
    starting_capital = float(sess["starting_capital"])
    name = sess.get("strategy_name", sid)

    positions = _get_positions(sid)
    if not positions:
        send_push_to_session_user(
            sid,
            title=f"Daily P&L — {name}",
            body="No open positions. Watching the market.",
            data={"screen": "PaperTrade"},
        )
        return

    symbols = [p["symbol"] for p in positions]
    prices = _latest_prices(symbols)

    # True portfolio P&L: cash (including realised gains from closed trades) + open position market value
    cash_balance    = _get_cash_balance(sid, starting_capital)
    invested        = sum(p["qty"] * p["avg"] for p in positions)
    current         = sum(p["qty"] * prices.get(p["symbol"], p["avg"]) for p in positions)
    portfolio_value = cash_balance + current
    total_pnl_abs   = portfolio_value - starting_capital
    total_pnl_pct   = (total_pnl_abs / starting_capital * 100) if starting_capital else 0.0

    # Return on deployed capital only (unrealised gain / cost basis of open positions)
    unreal_abs       = current - invested
    invested_pnl_pct = (unreal_abs / invested * 100) if invested else 0.0

    # Top gainers for the summary line
    enriched = sorted(
        [
            {
                **p,
                "pnl_pct": (
                    (prices[p["symbol"]] - p["avg"]) / p["avg"] * 100
                    if p["symbol"] in prices else 0.0
                ),
            }
            for p in positions
        ],
        key=lambda x: x["pnl_pct"],
        reverse=True,
    )
    top = enriched[0] if enriched else None
    bot = enriched[-1] if len(enriched) > 1 else None

    sign = "+" if total_pnl_abs >= 0 else ""
    inv_sign = "+" if unreal_abs >= 0 else ""
    body = (
        f"₹{starting_capital:,.0f} base · "
        f"{sign}₹{total_pnl_abs:,.0f} ({sign}{total_pnl_pct:.1f}% overall"
        f" · {inv_sign}{invested_pnl_pct:.1f}% on deployed)"
        f" · {len(positions)} positions"
    )
    if top:
        body += f"\nBest: {top['symbol']} {'+' if top['pnl_pct'] >= 0 else ''}{top['pnl_pct']:.1f}%"
    if bot and bot["symbol"] != (top["symbol"] if top else None):
        body += f"  Worst: {bot['symbol']} {'+' if bot['pnl_pct'] >= 0 else ''}{bot['pnl_pct']:.1f}%"

    send_push_to_session_user(
        sid,
        title=f"Daily P&L — {name}",
        body=body,
        data={"screen": "PaperTrade"},
    )
    print(f"     {sid}: {sign}₹{total_pnl_abs:,.0f} ({sign}{total_pnl_pct:.1f}% overall · {inv_sign}{invested_pnl_pct:.1f}% on deployed) · {len(positions)} positions")


def main():
    today    = date.today()
    calendar = NSECalendar()

    if not calendar.is_trading_day(today):
        print(f"[daily_pnl] {today} is not a trading day — exiting.")
        sys.exit(0)

    print(f"\n{'='*70}")
    print(f"  api/run_daily_pnl.py — {today}")
    print(f"{'='*70}")

    sessions = _load_active_sessions()
    if not sessions:
        print("  No active paper sessions — exiting.")
        sys.exit(0)

    print(f"  Active sessions: {len(sessions)}")
    for sess in sessions:
        try:
            _summarise_session(sess)
        except Exception as exc:
            print(f"  [ERROR] Session {sess['session_id']}: {exc}")

    print(f"\n{'='*70}")
    print(f"  Done — {today}")
    print(f"{'='*70}\n")


if __name__ == "__main__":
    main()
