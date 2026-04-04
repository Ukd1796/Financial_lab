#!/usr/bin/env python3
# api/run_paper_orders.py
#
# Morning order fill job for paper trading — processes fills for ALL active sessions.
# Schedule via cron at 9:15 AM IST on trading days:
#   15 3 * * 1-5  cd /path/to/Financial_lab && python -m api.run_paper_orders >> logs/paper_orders.log 2>&1
#
# What it does per session:
#   1. Cancel stale PENDING signals older than 1 trading day
#   2. Load yesterday's PENDING signals for this session_id
#   3. Assign order_id (PLACED), attempt fill via PaperAdapter (next-day open)
#   4. Send per-session email with fill summary
#
# Differences from run_orders.py (personal script):
#   - Reads sessions from Supabase B paper_trade_sessions (all active)
#   - Filters signal_queue by session_id — each user's fills are isolated

import sys
import uuid
from datetime import date, datetime

from dotenv import load_dotenv
load_dotenv()

from sqlalchemy import select, and_

from app.broker.paper_adapter import PaperAdapter
from app.core.database import SessionLocal
from app.core.notify import send_email
from app.data.calendar import NSECalendar
from app.data.models import SignalQueue
from sqlalchemy import text


# ---------------------------------------------------------------------------
# Session loader — mirrors run_paper_signals.py
# ---------------------------------------------------------------------------

def _load_active_sessions() -> list[dict]:
    db = SessionLocal()
    try:
        rows = db.execute(text(
            "SELECT session_id, strategy_id, strategy_name, starting_capital "
            "FROM paper_trade_sessions WHERE status = 'active'"
        )).fetchall()
        return [dict(r._mapping) for r in rows]
    except Exception as exc:
        print(f"  [Config] Could not read paper_trade_sessions ({exc})")
        return []
    finally:
        db.close()


# ---------------------------------------------------------------------------
# Per-session order processing
# ---------------------------------------------------------------------------

def _process_session(sess: dict, today: date, prev_day: date, broker: PaperAdapter) -> None:
    sid = sess["session_id"]
    print(f"\n  ── Session {sid}  ({sess.get('strategy_name', sess['strategy_id'])}) ──")

    db = SessionLocal()
    try:
        # ------------------------------------------------------------------
        # Step 1: Cancel stale PENDING signals for this session
        # ------------------------------------------------------------------
        stale = db.execute(
            select(SignalQueue).where(
                and_(
                    SignalQueue.session_id == sid,
                    SignalQueue.status     == "PENDING",
                    SignalQueue.signal_date < prev_day,
                )
            )
        ).scalars().all()

        if stale:
            for row in stale:
                row.status = "CANCELLED"
                row.notes  = (row.notes or "") + " | Stale — cancelled by run_paper_orders.py"
            db.commit()
            print(f"     Cancelled {len(stale)} stale signal(s)")

        # ------------------------------------------------------------------
        # Step 2: Load yesterday's PENDING signals for this session
        # ------------------------------------------------------------------
        pending_rows = db.execute(
            select(SignalQueue).where(
                and_(
                    SignalQueue.session_id  == sid,
                    SignalQueue.status      == "PENDING",
                    SignalQueue.signal_date == prev_day,
                )
            ).order_by(SignalQueue.action.desc())   # SELLs first
        ).scalars().all()

        if not pending_rows:
            print(f"     No pending signals for {prev_day}")
            return

        print(f"     Processing {len(pending_rows)} pending signal(s) from {prev_day}:")

        # ------------------------------------------------------------------
        # Step 3: Assign order_id, attempt fill
        # ------------------------------------------------------------------
        fills   = []
        pending = []

        for row in pending_rows:
            if not row.order_id:
                row.order_id = f"PAPER-{uuid.uuid4().hex[:8].upper()}"
                row.status   = "PLACED"
            db.commit()

            order = broker.get_order_status(row.order_id)
            if order.status == "FILLED":
                fills.append((row, order))
            else:
                pending.append(row)

        # ------------------------------------------------------------------
        # Step 4: Summary + email
        # ------------------------------------------------------------------
        print(f"     Filled: {len(fills)}  |  Pending: {len(pending)}")
        for row, order in fills:
            print(f"       {row.action:<4} {row.symbol:<14} qty={order.fill_qty}  "
                  f"fill=₹{order.fill_price:.2f}  [{row.strategy}]")

        fill_lines = "\n".join(
            f"  {row.action:<4} {row.symbol:<14} qty={order.fill_qty}  "
            f"fill=₹{order.fill_price:.2f}  [{row.strategy}]"
            for row, order in fills
        ) or "  (none)"
        pending_lines = "\n".join(f"  {r.symbol}" for r in pending) or "  (none)"

        send_email(
            subject=(f"[FinLab Paper] {sid} — Orders {today} | "
                     f"{len(fills)} filled, {len(pending)} pending"),
            body=(
                f"Paper Trade Order Report — {today}\n\n"
                f"Session:  {sid}  ({sess.get('strategy_name', '')})\n"
                f"Signals from: {prev_day}\n\n"
                f"Filled ({len(fills)}):\n{fill_lines}\n\n"
                f"Pending ({len(pending)}):\n{pending_lines}\n"
            ),
        )

    finally:
        db.close()


# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------

def main():
    today    = date.today()
    calendar = NSECalendar()

    if not calendar.is_trading_day(today):
        print(f"[paper_orders] {today} is not a trading day — exiting.")
        sys.exit(0)

    print(f"\n{'='*70}")
    print(f"  api/run_paper_orders.py — {today}")
    print(f"{'='*70}")

    sessions = _load_active_sessions()
    if not sessions:
        print("  No active paper sessions — exiting.")
        sys.exit(0)

    print(f"  Active sessions: {len(sessions)}")

    prev_day = calendar.previous_trading_day(today)
    broker   = PaperAdapter()

    for sess in sessions:
        try:
            _process_session(sess, today, prev_day, broker)
        except Exception as exc:
            print(f"  [ERROR] Session {sess['session_id']}: {exc}")

    print(f"\n{'='*70}")
    print(f"  Done — {today}")
    print(f"{'='*70}\n")


if __name__ == "__main__":
    main()
