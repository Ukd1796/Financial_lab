#!/usr/bin/env python3
# run_orders.py
#
# ==============================================================
# DEPRECATED — do not run or schedule.
# Replaced by api/run_paper_orders.py which is session-aware
# and processes fills per paper_trade_sessions entry.
# Remove from cron: was scheduled at  45 10 * * 1-5
# ==============================================================
#
# EOD order fill job for paper trading.
# Must run AFTER run_signals.py (which ingests today's OHLC at 3:35 PM IST).
# Schedule via cron at 3:45 PM IST on trading days:
#   45 10 * * 1-5 cd /path/to/Financial_lab && python run_orders.py >> logs/orders.log 2>&1
#
# What it does:
#   1. Cancel stale PENDING/PLACED signals (older than 1 trading day)
#   2. Load yesterday's PENDING or PLACED signals (PLACED = placed but not yet filled)
#   3. For each signal: call broker.get_order_status() to attempt fill
#      PaperAdapter simulates fill at next-day open from market_ohlc
#      (today's OHLC is available because run_signals.py already ran)
#   4. Print fill summary

import sys
from datetime import date, datetime, timedelta

from dotenv import load_dotenv
load_dotenv()

from app.broker.paper_adapter import PaperAdapter
from app.core.database import SessionLocal
from app.core.notify import send_email
from app.data.calendar import NSECalendar
from app.data.models import SignalQueue
from sqlalchemy import select


def main():
    today    = date.today()
    calendar = NSECalendar()

    if not calendar.is_trading_day(today):
        print(f"[run_orders] {today} is not a trading day — exiting.")
        sys.exit(0)

    print(f"\n{'='*60}")
    print(f"  run_orders.py — {today}  (paper trading)")
    print(f"{'='*60}")

    session = SessionLocal()
    broker  = PaperAdapter()

    try:
        # ------------------------------------------------------------------
        # Step 1: Cancel stale PENDING signals (older than 1 trading day)
        # ------------------------------------------------------------------
        prev_trading_day = calendar.previous_trading_day(today)
        stale_rows = session.execute(
            select(SignalQueue)
            .where(SignalQueue.status == "PENDING")   # PLACED = already in market, never cancel
            .where(SignalQueue.signal_date < prev_trading_day)
            .where(SignalQueue.session_id == None)   # noqa: E711 — personal signals only
        ).scalars().all()

        if stale_rows:
            print(f"\n  Cancelling {len(stale_rows)} stale signal(s):")
            for row in stale_rows:
                row.status = "CANCELLED"
                row.notes  = (row.notes or "") + " | Stale — cancelled by run_orders.py"
                print(f"    {row.symbol} {row.action} (signal date: {row.signal_date})")
            session.commit()

        # ------------------------------------------------------------------
        # Step 2: Load today's PENDING signals (from yesterday's run_signals.py)
        # ------------------------------------------------------------------
        pending_rows = session.execute(
            select(SignalQueue)
            .where(SignalQueue.status.in_(["PENDING", "PLACED"]))
            .where(SignalQueue.signal_date == prev_trading_day)
            .where(SignalQueue.session_id == None)   # noqa: E711 — personal signals only
            .order_by(SignalQueue.action.desc())   # SELLs first
        ).scalars().all()

        if not pending_rows:
            print(f"\n  No pending signals for {prev_trading_day} — nothing to place.")
            session.close()
            return

        print(f"\n  Processing {len(pending_rows)} pending signal(s) from {prev_trading_day}:")

        # ------------------------------------------------------------------
        # Step 3: Assign order_id and attempt fill via PaperAdapter
        # ------------------------------------------------------------------
        import uuid
        fills   = []
        pending = []

        for row in pending_rows:
            # Assign a paper order_id if not already set
            if not row.order_id:
                row.order_id = f"PAPER-{uuid.uuid4().hex[:8].upper()}"
                row.status   = "PLACED"
            session.commit()

            # Try to fill (PaperAdapter looks up next-day open from market_ohlc)
            order = broker.get_order_status(row.order_id)

            if order.status == "FILLED":
                fills.append((row, order))
            else:
                pending.append(row)

        # ------------------------------------------------------------------
        # Step 4: Summary
        # ------------------------------------------------------------------
        print(f"\n  Results:")
        print(f"    Filled:  {len(fills)}")
        print(f"    Pending: {len(pending)}  (next-day open not yet available)")

        if fills:
            print(f"\n  Fills:")
            for row, order in fills:
                pnl_str = ""
                if row.action == "SELL":
                    pnl_str = f"  (entry avg unknown in paper mode)"
                print(
                    f"    {row.action:<4} {row.symbol:<14} "
                    f"qty={order.fill_qty}  fill=₹{order.fill_price:.2f}  "
                    f"[{row.strategy}]{pnl_str}"
                )

        # Build email strings while session is still open
        fill_lines = "\n".join(
            f"  {row.action:<4} {row.symbol:<14} qty={order.fill_qty}  fill=₹{order.fill_price:.2f}  [{row.strategy}]"
            for row, order in fills
        ) or "  (none)"
        pending_lines = "\n".join(f"  {r.symbol}" for r in pending) or "  (none)"

    finally:
        session.close()

    # ------------------------------------------------------------------
    # Email summary
    # ------------------------------------------------------------------
    email_body = f"""Financial Lab — Order Fill Report {today}

Fills:   {len(fills)}
Pending: {len(pending)}  (next-day open not yet available)

Filled orders:
{fill_lines}

Pending (will retry tomorrow):
{pending_lines}
"""
    send_email(
        subject=f"[FinLab] Orders {today} — {len(fills)} filled, {len(pending)} pending",
        body=email_body,
    )

    print(f"\n{'='*60}\n")


if __name__ == "__main__":
    main()
