from app.strategy.models import Decision


class RiskAgent:

    def __init__(
        self,
        max_position_pct: float = 0.2,
        atr_multiplier:   float = 2.0,
        allowed_regimes         = None,
    ):
        self.max_position_pct = max_position_pct
        self.atr_multiplier   = atr_multiplier
        # None → no regime filter applied (all regimes allowed)
        # list → only regimes in the list pass the BUY gate
        self.allowed_regimes  = allowed_regimes

    # --------------------------------------------------
    # MAIN EVALUATION
    # --------------------------------------------------
    def evaluate(self, decision: Decision, portfolio, market_state, equity_prices: dict = None):
        """
        equity_prices — full {symbol: price} map for the current day,
            covering all held positions (not just the universe subset).
            Used to compute true portfolio equity for position sizing.
            Falls back to single-symbol pricing when not provided.
        """
        symbol        = decision.symbol
        current_price = market_state.latest_price
        atr           = market_state.indicators.get("atr_14")
        regime        = market_state.indicators.get("regime")

        # --- Regime filter (BUY only) ---
        # Skipped entirely when allowed_regimes is None.
        if decision.action == "BUY" and self.allowed_regimes is not None:
            if regime not in self.allowed_regimes:
                return Decision(
                    symbol=symbol,
                    action="HOLD",
                    reasoning=f"Blocked by regime filter ({regime})",
                )

        # --- ATR stop enforcement ---
        if symbol in portfolio.positions and atr:
            position   = portfolio.positions[symbol]
            stop_price = position.average_price - (self.atr_multiplier * atr)
            if current_price <= stop_price:
                return Decision(
                    symbol=symbol,
                    action="SELL",
                    quantity=position.quantity,
                    reasoning=f"ATR stop hit at {stop_price:.2f}",
                )

        # --- HOLD pass-through ---
        if decision.action == "HOLD":
            return decision

        # --- Capital allocation ---
        # Use the full equity_prices map so that all held positions are
        # valued at their current market price, not $0.
        price_map    = equity_prices if equity_prices else {symbol: current_price}
        total_equity = portfolio.total_equity(price_map)
        max_allocatable = total_equity * self.max_position_pct

        # BUY
        if decision.action == "BUY":
            if symbol in portfolio.positions:
                return Decision(symbol=symbol, action="HOLD")

            # max_allocatable is based on total equity (includes unrealized gains)
            # but we can only spend actual cash — cap accordingly
            spendable = min(max_allocatable, portfolio.cash)
            quantity  = spendable // current_price
            if quantity <= 0:
                return Decision(symbol=symbol, action="HOLD")

            return Decision(
                symbol=symbol,
                action="BUY",
                quantity=quantity,
                reasoning=f"Allocation: {self.max_position_pct * 100:.1f}%",
            )

        # SELL
        if decision.action == "SELL":
            if symbol not in portfolio.positions:
                return Decision(symbol=symbol, action="HOLD")

            return Decision(
                symbol=symbol,
                action="SELL",
                quantity=portfolio.positions[symbol].quantity,
                reasoning="Strategy exit",
            )

        return decision
