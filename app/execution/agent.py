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

    def __init__(
        self,
        portfolio_engine,
        commission_pct: float = 0.001,   # 0.10% per side (NSE brokerage + STT + charges)
        slippage_pct:   float = 0.0005,  # 0.05% per side market-impact estimate
        cost_model            = None,    # ZerodhaCostModel; None ⇒ legacy %-model (EQUITY regression-safe)
        cost_segment:   str   = "equity_delivery",  # "equity_delivery" | "etf" — only used when cost_model set
    ):
        self.portfolio_engine = portfolio_engine
        self.commission_pct   = commission_pct
        self.slippage_pct     = slippage_pct
        self.cost_model       = cost_model
        self.cost_segment     = cost_segment

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

        # ------------------------------------------------------------------
        # Effective execution price — bakes slippage + commission into the
        # per-share price so all downstream accounting (cash, avg_price,
        # realized PnL, trade PnL) is automatically post-cost.
        #
        #   BUY  : we pay more  → price * (1 + slip) * (1 + comm)
        #   SELL : we receive less → price * (1 - slip) * (1 - comm)
        # ------------------------------------------------------------------
        # Per-side proportional charge: real Zerodha model when injected
        # (side-asymmetric — e.g. ETF STT is sell-only), else the legacy
        # symmetric commission_pct (default → EQUITY regression byte-identical).
        if self.cost_model is not None:
            buy_comm  = self.cost_model.pct_charge("BUY",  self.cost_segment)
            sell_comm = self.cost_model.pct_charge("SELL", self.cost_segment)
        else:
            buy_comm = sell_comm = self.commission_pct

        if decision.action == "BUY":
            exec_price = current_price * (1 + self.slippage_pct) * (1 + buy_comm)
        elif decision.action == "SELL":
            exec_price = current_price * (1 - self.slippage_pct) * (1 - sell_comm)
        else:
            exec_price = current_price

        # Snapshot BEFORE execution
        portfolio_before = {
            "cash": portfolio.cash,
            "positions": self._serialize_positions(portfolio.positions),
            "realized_pnl": portfolio.realized_pnl
        }

        executed     = False
        trade_pnl    = 0.0
        exec_quantity = decision.quantity  # actual shares transacted (may differ from decision)

        # -------------------------
        # BUY
        # -------------------------
        if decision.action == "BUY" and decision.quantity:

            # RiskAgent sized using raw price; exec_price includes cost markup.
            # Trim down to what cash can actually cover at the effective price.
            exec_quantity = min(int(decision.quantity), int(portfolio.cash // exec_price))
            if exec_quantity > 0:
                self.portfolio_engine.buy(
                    decision.symbol,
                    exec_quantity,
                    exec_price,
                    atr_at_entry=getattr(decision, "atr_at_entry", 0.0),
                    entry_date=getattr(market_state, "timestamp", None),
                )
                executed = True

        # -------------------------
        # SELL
        # -------------------------
        elif decision.action == "SELL" and decision.quantity:

            # Capture cost basis BEFORE selling so trade_pnl reflects net P&L
            # (entry_price already includes buy-side costs from the BUY exec_price)
            if decision.symbol in portfolio.positions:
                entry_price   = portfolio.positions[decision.symbol].average_price
                exec_quantity = portfolio.positions[decision.symbol].quantity
                trade_pnl     = (exec_price - entry_price) * exec_quantity

            self.portfolio_engine.sell(
                decision.symbol,
                exec_quantity,
                exec_price,
            )
            executed = True

            # Flat DP charge (Zerodha): per-scrip, sell-side, value-independent.
            # The %-model folds proportional costs into exec_price; the flat
            # part has no price to fold into, so deduct it explicitly so the
            # equity curve, realized PnL and trade PnL are all net of it.
            # No-op when cost_model is None ⇒ legacy/EQUITY path unchanged.
            if self.cost_model is not None:
                dp = self.cost_model.flat_charge("SELL", self.cost_segment)
                if dp:
                    portfolio.cash         -= dp
                    portfolio.realized_pnl -= dp
                    trade_pnl              -= dp

        # Snapshot AFTER execution
        portfolio_after = {
            "cash": portfolio.cash,
            "positions": self._serialize_positions(portfolio.positions),
            "realized_pnl": portfolio.realized_pnl
        }

        return ExecutionResult(
            executed=executed,
            action=decision.action,
            quantity=exec_quantity,
            price=exec_price,
            portfolio_before=portfolio_before,
            portfolio_after=portfolio_after,
            trade_pnl=trade_pnl
        )
