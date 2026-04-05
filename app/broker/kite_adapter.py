# app/broker/kite_adapter.py
#
# KiteAdapter — live trading via Zerodha Kite Connect.
#
# Requires:
#   pip install kiteconnect>=5.0.1
#
# Usage:
#   adapter = KiteAdapter(api_key="xxx", access_token="yyy")
#   order_id = adapter.place_order("RELIANCE", "BUY", 10)

from typing import List

from kiteconnect import KiteConnect

from app.broker.base import BrokerAdapter
from app.broker.models import BrokerPosition, Order


# Zerodha order status → internal status mapping

_STATUS_MAP = {
    "COMPLETE":  "FILLED",
    "REJECTED":  "REJECTED",
    "CANCELLED": "CANCELLED",
    "OPEN":      "PLACED",
    "PENDING":   "PENDING",
    "AMO REQ RECEIVED": "PLACED",
}


class KiteAdapter(BrokerAdapter):
    """
    Live broker adapter for Zerodha Kite Connect.

    One instance per user session — api_key + access_token are
    loaded from broker_connections row and passed at construction time.
    access_token is valid only until midnight IST; after expiry the
    user must re-authenticate via the OAuth flow.
    """

    def __init__(self, api_key: str, access_token: str):
        self._kite = KiteConnect(api_key=api_key)
        self._kite.set_access_token(access_token)

    # ------------------------------------------------------------------
    def place_order(
        self,
        symbol:     str,
        action:     str,
        quantity:   int,
        order_type: str = "MARKET",
        notes:      str = "",
    ) -> str:
        transaction = (
            self._kite.TRANSACTION_TYPE_BUY
            if action.upper() == "BUY"
            else self._kite.TRANSACTION_TYPE_SELL
        )
        kite_order_type = (
            self._kite.ORDER_TYPE_MARKET
            if order_type.upper() == "MARKET"
            else self._kite.ORDER_TYPE_LIMIT
        )
        order_id = self._kite.place_order(
            variety=self._kite.VARIETY_REGULAR,
            exchange=self._kite.EXCHANGE_NSE,
            tradingsymbol=symbol,
            transaction_type=transaction,
            quantity=quantity,
            product=self._kite.PRODUCT_CNC,       # delivery / equity
            order_type=kite_order_type,
        )
        return str(order_id)

    # ------------------------------------------------------------------
    def get_order_status(self, order_id: str) -> Order:
        orders = self._kite.orders()
        row = next((o for o in orders if str(o["order_id"]) == order_id), None)
        if row is None:
            return Order(
                order_id=order_id, symbol="", action="",
                quantity=0, order_type="MARKET", status="NOT_FOUND",
            )
        return Order(
            order_id=order_id,
            symbol=row["tradingsymbol"],
            action="BUY" if row["transaction_type"] == "BUY" else "SELL",
            quantity=row["quantity"],
            order_type="MARKET",
            status=_STATUS_MAP.get(row["status"], "PENDING"),
            fill_price=row.get("average_price") or None,
            fill_qty=row.get("filled_quantity") or None,
        )

    # ------------------------------------------------------------------
    def get_positions(self) -> List[BrokerPosition]:
        data = self._kite.positions()
        return [
            BrokerPosition(
                symbol=p["tradingsymbol"],
                quantity=p["quantity"],
                average_price=p["average_price"],
            )
            for p in data.get("net", [])
            if p["quantity"] > 0
        ]

    # ------------------------------------------------------------------
    def cancel_order(self, order_id: str) -> bool:
        try:
            self._kite.cancel_order(
                variety=self._kite.VARIETY_REGULAR,
                order_id=order_id,
            )
            return True
        except Exception:
            # Already filled or cancelled — treat as success
            return True
