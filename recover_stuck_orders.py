#!/usr/bin/env python3
# recover_stuck_orders.py
#
# One-off script to fill all PENDING/PLACED signals that got stuck
# because run_orders.py was running before OHLC data was available.
#
# Safe to run multiple times — already-FILLED signals are skipped.
# Delete this script after running.

import uuid
from dotenv import load_dotenv
load_dotenv()

from sqlalchemy import select
from app.broker.paper_adapter import PaperAdapter
from app.core.database import SessionLocal
from app.data.models import SignalQueue

def main():
    session = SessionLocal()
    broker  = PaperAdapter()

    try:
        stuck = session.execute(
            select(SignalQueue)
            .where(SignalQueue.status.in_(["PENDING", "PLACED"]))
            .where(SignalQueue.session_id == None)   # noqa: E711 — personal signals only
            .order_by(SignalQueue.signal_date.asc(), SignalQueue.action.desc())
        ).scalars().all()

        if not stuck:
            print("No stuck signals found — nothing to do.")
            return

        print(f"Found {len(stuck)} stuck signal(s):\n")

        filled  = []
        no_data = []

        for row in stuck:
            if not row.order_id:
                row.order_id = f"PAPER-{uuid.uuid4().hex[:8].upper()}"
                row.status   = "PLACED"
                session.commit()

            order = broker.get_order_status(row.order_id)

            if order.status == "FILLED":
                filled.append((row, order))
                print(f"  FILLED  {row.action:<4} {row.symbol:<14} "
                      f"signal_date={row.signal_date}  fill=₹{order.fill_price:.2f}  qty={order.fill_qty}")
            else:
                no_data.append(row)
                print(f"  NO DATA {row.action:<4} {row.symbol:<14} "
                      f"signal_date={row.signal_date}  (no OHLC available — left as PLACED)")

        print(f"\nResult: {len(filled)} filled, {len(no_data)} still pending (no OHLC data yet)")

        if no_data:
            print("\nSignals with no OHLC data — will be picked up automatically on next trading day run.")

    finally:
        session.close()


if __name__ == "__main__":
    main()
