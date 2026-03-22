# app/broker/base.py
#
# BrokerAdapter — abstract interface for all broker integrations.
#
# Implementations:
#   PaperAdapter  (app/broker/paper_adapter.py) — no real orders, logs to DB
#   KiteAdapter   (app/broker/kite_adapter.py)  — Zerodha Kite live trading
#
# run_signals.py and run_orders.py depend only on this interface, making it
# trivial to switch from paper to live by swapping the adapter instance.

from abc import ABC, abstractmethod
from typing import List

from app.broker.models import BrokerPosition, Order


class BrokerAdapter(ABC):

    @abstractmethod
    def place_order(
        self,
        symbol:     str,
        action:     str,        # "BUY" or "SELL"
        quantity:   int,
        order_type: str = "MARKET",
        notes:      str = "",
    ) -> str:
        """
        Submit an order to the broker.
        Returns the broker-assigned order_id string.
        """

    @abstractmethod
    def get_order_status(self, order_id: str) -> Order:
        """Fetch the current status of an order by its broker order_id."""

    @abstractmethod
    def get_positions(self) -> List[BrokerPosition]:
        """
        Return all currently open positions from the broker.
        For paper trading this reads from the live_positions DB table.
        """

    @abstractmethod
    def cancel_order(self, order_id: str) -> bool:
        """
        Cancel a pending order. Returns True on success.
        No-op (returns True) for already-filled or cancelled orders.
        """
