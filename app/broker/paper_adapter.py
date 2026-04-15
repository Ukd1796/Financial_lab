# app/broker/paper_adapter.py
#
# PaperAdapter — simulates a live broker with no real orders.
#
# Design:
#   place_order()      → writes to signal_queue (status=PLACED), returns fake order_id
#   get_order_status() → returns FILLED at next-day open price from market_ohlc
#   get_positions()    → reads live_positions table
#   cancel_order()     → sets signal_queue status=CANCELLED
#
# Simulated fill price: next trading day's open from market_ohlc.
# If next-day open is not yet available (signal just generated), returns PENDING.
# run_orders.py calls get_order_status() the following morning to confirm fills.

from datetime import datetime, date, timedelta
from typing import List

from sqlalchemy import select

from app.broker.base import BrokerAdapter
from app.broker.models import BrokerPosition, Order
from app.core.database import SessionLocal
from app.data.models import LivePosition, MarketOHLC, SignalQueue


class PaperAdapter(BrokerAdapter):
    """
    Paper trading broker.

    All "orders" are written to the signal_queue table.
    Fills are simulated at the next trading day's open price.
    Positions are persisted in live_positions.
    """

    # ------------------------------------------------------------------
    def place_order(
        self,
        symbol:     str,
        action:     str,
        quantity:   int,
        order_type: str = "MARKET",
        notes:      str = "",
    ) -> str:
        raise NotImplementedError(
            "PaperAdapter.place_order() is called by run_orders.py, not directly. "
            "Signals are written to signal_queue by run_signals.py."
        )

    # ------------------------------------------------------------------
    def get_order_status(self, order_id: str) -> Order:
        """
        Look up a signal_queue row by order_id.
        If status is PLACED and next-day open is available, mark as FILLED
        and update live_positions accordingly.
        """
        session = SessionLocal()
        try:
            row = session.execute(
                select(SignalQueue).where(SignalQueue.order_id == order_id)
            ).scalar_one_or_none()

            if row is None:
                return Order(
                    order_id=order_id, symbol="", action="",
                    quantity=0, order_type="MARKET", status="NOT_FOUND",
                )

            if row.status != "PLACED":
                return self._row_to_order(row)

            # Try to fill at next-day open
            next_open = self._get_next_open(session, row.symbol, row.signal_date)
            if next_open is None:
                return self._row_to_order(row)   # not yet available

            # Simulate fill — signal_queue is authoritative; live_positions is
            # maintained as a convenience cache for frontend display.
            row.status     = "FILLED"
            row.fill_price = next_open
            row.fill_qty   = row.target_qty
            row.notes      = (row.notes or "") + f" | Paper fill @ {next_open:.2f}"
            self._update_live_position(session, row)
            session.commit()
            return self._row_to_order(row)

        finally:
            session.close()

    # ------------------------------------------------------------------
    def get_positions(self) -> List[BrokerPosition]:
        """Return all live positions from the live_positions table."""
        session = SessionLocal()
        try:
            rows = session.execute(select(LivePosition)).scalars().all()
            return [
                BrokerPosition(
                    symbol=r.symbol,
                    quantity=r.quantity,
                    average_price=r.average_price,
                    strategy=r.strategy,
                )
                for r in rows
            ]
        finally:
            session.close()

    # ------------------------------------------------------------------
    def cancel_order(self, order_id: str) -> bool:
        session = SessionLocal()
        try:
            row = session.execute(
                select(SignalQueue).where(SignalQueue.order_id == order_id)
            ).scalar_one_or_none()
            if row is None:
                return False
            if row.status in ("FILLED", "CANCELLED", "REJECTED"):
                return True
            row.status = "CANCELLED"
            session.commit()
            return True
        finally:
            session.close()

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------
    @staticmethod
    def _get_next_open(session, symbol: str, signal_date: date) -> float | None:
        """Fetch the open price of the first trading day after signal_date.

        Timestamps in market_ohlc are stored as UTC-naive datetimes. NSE daily
        candles from yfinance use IST midnight as the candle timestamp, so
        'April 10 IST' is stored as 'April 9 18:30:00 UTC' (midnight IST minus
        the 5h30m offset). We must subtract the IST offset when building query
        boundaries, otherwise the search window starts 5h30m too late and misses
        the correct candle.
        """
        _IST = timedelta(hours=5, minutes=30)
        next_day = signal_date + timedelta(days=1)
        cutoff   = signal_date + timedelta(days=5)   # look ahead up to 5 calendar days
        row = session.execute(
            select(MarketOHLC)
            .where(MarketOHLC.symbol == symbol)
            .where(MarketOHLC.timestamp >= datetime.combine(next_day, datetime.min.time()) - _IST)
            .where(MarketOHLC.timestamp <= datetime.combine(cutoff, datetime.max.time()) - _IST)
            .order_by(MarketOHLC.timestamp.asc())
            .limit(1)
        ).scalar_one_or_none()
        return row.open if row else None

    @staticmethod
    def _update_live_position(session, signal: SignalQueue) -> None:
        """Upsert live_positions after a simulated fill."""
        existing = session.execute(
            select(LivePosition).where(LivePosition.symbol == signal.symbol)
        ).scalar_one_or_none()

        now = datetime.utcnow()

        if signal.action == "BUY":
            if existing:
                # Average down / up
                total_qty   = existing.quantity + signal.fill_qty
                total_cost  = (existing.quantity * existing.average_price
                               + signal.fill_qty * signal.fill_price)
                existing.quantity      = total_qty
                existing.average_price = total_cost / total_qty
                existing.last_synced_at = now
            else:
                session.add(LivePosition(
                    symbol        = signal.symbol,
                    quantity      = signal.fill_qty,
                    average_price = signal.fill_price,
                    entry_date    = signal.signal_date,
                    strategy      = signal.strategy,
                    last_synced_at = now,
                ))

        elif signal.action == "SELL" and existing:
            remaining = existing.quantity - signal.fill_qty
            if remaining <= 0:
                session.delete(existing)
            else:
                existing.quantity       = remaining
                existing.last_synced_at = now

    @staticmethod
    def _row_to_order(row: SignalQueue) -> Order:
        return Order(
            order_id   = row.order_id,
            symbol     = row.symbol,
            action     = row.action,
            quantity   = row.target_qty,
            order_type = "MARKET",
            status     = row.status,
            placed_at  = row.created_at,
            fill_price = row.fill_price,
            fill_qty   = row.fill_qty,
            notes      = row.notes or "",
        )
