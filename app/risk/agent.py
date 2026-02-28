from app.strategy.models import Decision
from app.meta.strategy_mode import ModePolicy
from app.meta.strategy_mode import StrategyMode

MODE_POLICIES = {
    StrategyMode.AGGRESSIVE: ModePolicy(
        max_position_pct=0.30,
        atr_multiplier=3.0,
        allowed_regimes=[
            "LOW_VOL_UPTREND",
            "MID_VOL_UPTREND",
            "HIGH_VOL_UPTREND",
            "SIDEWAYS"
        ]
    ),

    StrategyMode.BALANCED: ModePolicy(
        max_position_pct=0.20,
        atr_multiplier=2.0,
        allowed_regimes=[
            "LOW_VOL_UPTREND",
            "MID_VOL_UPTREND",
            "HIGH_VOL_UPTREND"
        ]
    ),

    StrategyMode.DEFENSIVE: ModePolicy(
        max_position_pct=0.10,
        atr_multiplier=1.5,
        allowed_regimes=[
            "LOW_VOL_UPTREND"
        ]
    ),
}

class RiskAgent:

    def __init__(
        self,
        max_position_pct: float = 0.2,
        atr_multiplier: float = 2.0,
        allowed_regimes=None
    ):
        self.max_position_pct = max_position_pct
        self.atr_multiplier = atr_multiplier

        # 🔥 Meta-controlled multiplier (default 1.0)
        self.allocation_multiplier = 1.0

        self.allowed_regimes = allowed_regimes or [
            "LOW_VOL_UPTREND",
            "MID_VOL_UPTREND",
            "HIGH_VOL_UPTREND",
        ]

    # ---------------------------------------------------
    # 🔥 Meta Hook
    # ---------------------------------------------------
    def update_allocation_multiplier(self, multiplier: float):
        self.allocation_multiplier = multiplier

    def apply_mode_policy(self, policy: ModePolicy):
        self.max_position_pct = policy.max_position_pct
        self.atr_multiplier = policy.atr_multiplier
        self.allowed_regimes = policy.allowed_regimes

    # ---------------------------------------------------
    # MAIN EVALUATION
    # ---------------------------------------------------
    def evaluate(self, decision: Decision, portfolio, market_state):

        symbol = decision.symbol
        current_price = market_state.latest_price
        atr = market_state.indicators.get("atr_14")
        regime = market_state.indicators.get("regime")

        # ---------------------------------------------------
        # 0️⃣ Regime Filter
        # ---------------------------------------------------
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
        # 2️⃣ HOLD
        # ---------------------------------------------------
        if decision.action == "HOLD":
            return decision

        # ---------------------------------------------------
        # 3️⃣ Capital Allocation
        # ---------------------------------------------------
        total_equity = portfolio.total_equity(
            {symbol: current_price}
        )

        effective_pct = self.max_position_pct * self.allocation_multiplier
        max_allocatable = total_equity * effective_pct

        # ---------------------------------------------------
        # BUY
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
                reasoning=(
                    f"Allocation: {effective_pct*100:.1f}% "
                    f"(multiplier {self.allocation_multiplier:.2f})"
                )
            )

        # ---------------------------------------------------
        # SELL
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