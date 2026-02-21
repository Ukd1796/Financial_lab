from app.strategy.models import Decision


class RiskAgent:

    def __init__(
        self,
        max_position_pct: float = 0.2,
        atr_multiplier: float = 2.0,
        allowed_regimes=None
    ):
        self.max_position_pct = max_position_pct
        self.atr_multiplier = atr_multiplier

        # Default: only trade in uptrend regimes
        self.allowed_regimes = allowed_regimes or [
            "LOW_VOL_UPTREND",
            "MID_VOL_UPTREND",
            "HIGH_VOL_UPTREND",
        ]

    def evaluate(self, decision: Decision, portfolio, market_state):

        symbol = decision.symbol
        current_price = market_state.latest_price
        atr = market_state.indicators.get("atr_14")

        # ---------------------------------------------------
        # 0️⃣ Regime Filter (NEW FIX)
        # ---------------------------------------------------
        regime = market_state.indicators.get("regime")

        if decision.action == "BUY":

            if regime not in self.allowed_regimes:
                return Decision(
                    symbol=symbol,
                    action="HOLD",
                    reasoning=f"Blocked by regime filter ({regime})"
                )

        # ---------------------------------------------------
        # 1️⃣ ATR Stop Enforcement
        # ---------------------------------------------------
        if symbol in portfolio.positions and atr:

            position = portfolio.positions[symbol]
            entry_price = position.average_price

            stop_price = entry_price - (self.atr_multiplier * atr)

            if current_price <= stop_price:
                return Decision(
                    symbol=symbol,
                    action="SELL",
                    quantity=position.quantity,
                    reasoning=f"ATR stop hit at {stop_price:.2f}"
                )

        # ---------------------------------------------------
        # 2️⃣ HOLD Case
        # ---------------------------------------------------
        if decision.action == "HOLD":
            return decision

        total_equity = portfolio.total_equity(
            {symbol: current_price}
        )

        max_allocatable = total_equity * self.max_position_pct

        # ---------------------------------------------------
        # 3️⃣ BUY Logic
        # ---------------------------------------------------
        if decision.action == "BUY":

            if symbol in portfolio.positions:
                return Decision(symbol=symbol, action="HOLD")

            quantity = max_allocatable // current_price

            if quantity <= 0:
                return Decision(symbol=symbol, action="HOLD")

            return Decision(
                symbol=symbol,
                action="BUY",
                quantity=quantity,
                reasoning=f"Risk-adjusted allocation ({self.max_position_pct*100}%)"
            )

        # ---------------------------------------------------
        # 4️⃣ SELL Logic
        # ---------------------------------------------------
        if decision.action == "SELL":

            if symbol not in portfolio.positions:
                return Decision(symbol=symbol, action="HOLD")

            quantity = portfolio.positions[symbol].quantity

            return Decision(
                symbol=symbol,
                action="SELL",
                quantity=quantity,
                reasoning="Strategy exit"
            )

        return decision