# app/execution/agent.py

from dataclasses import dataclass
from typing import Optional
from app.strategy.models import Decision


@dataclass
class ExecutionResult:
    executed: bool
    action: str
    quantity: float
    price: float
    portfolio_before: dict
    portfolio_after: dict
    trade_pnl: float = 0.0


class ExecutionAgent:

    def __init__(self, portfolio_engine):
        self.portfolio_engine = portfolio_engine

    def _serialize_positions(self, positions):
        return {
            symbol: {
                "quantity": pos.quantity,
                "average_price": pos.average_price
            }
            for symbol, pos in positions.items()
        }

    def execute(self, decision, market_state, portfolio):

        current_price = market_state.latest_price

        # Snapshot BEFORE execution
        portfolio_before = {
            "cash": portfolio.cash,
            "positions": self._serialize_positions(portfolio.positions),
            "realized_pnl": portfolio.realized_pnl
        }

        executed = False
        trade_pnl = 0.0

        # -------------------------
        # BUY
        # -------------------------
        if decision.action == "BUY" and decision.quantity:

            self.portfolio_engine.buy(
                decision.symbol,
                decision.quantity,
                current_price
            )
            executed = True

        # -------------------------
        # SELL
        # -------------------------
        elif decision.action == "SELL" and decision.quantity:

            # Capture entry price BEFORE selling
            if decision.symbol in portfolio.positions:
                entry_price = portfolio.positions[decision.symbol].average_price
                quantity = portfolio.positions[decision.symbol].quantity

                trade_pnl = (current_price - entry_price) * quantity

            self.portfolio_engine.sell(
                decision.symbol,
                decision.quantity,
                current_price
            )
            executed = True

        # Snapshot AFTER execution
        portfolio_after = {
            "cash": portfolio.cash,
            "positions": self._serialize_positions(portfolio.positions),
            "realized_pnl": portfolio.realized_pnl
        }

        return ExecutionResult(
            executed=executed,
            action=decision.action,
            quantity=decision.quantity,
            price=current_price,
            portfolio_before=portfolio_before,
            portfolio_after=portfolio_after,
            trade_pnl=trade_pnl
        )
