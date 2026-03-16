from app.strategy.models import Decision


class RiskAgent:

    def __init__(
        self,
        max_position_pct:    float = 0.2,
        atr_multiplier:      float = 2.0,
        allowed_regimes            = None,
        risk_per_trade_pct:  float = 0.005,  # 0.5% of portfolio at risk per trade
        use_vol_sizing:      bool  = True,   # ATR-based sizing; falls back to max_position_pct
        breadth_circuit_breaker: bool  = False, # suppress BUY when market is broadly falling
        max_downtrend_pct:   float = 0.60,   # block BUY when >60% of universe in DOWNTREND
    ):
        self.max_position_pct        = max_position_pct
        self.atr_multiplier          = atr_multiplier
        self.allowed_regimes         = allowed_regimes
        self.risk_per_trade_pct      = risk_per_trade_pct
        self.use_vol_sizing          = use_vol_sizing
        self.breadth_circuit_breaker = breadth_circuit_breaker
        self.max_downtrend_pct       = max_downtrend_pct

    # --------------------------------------------------
    # MAIN EVALUATION
    # --------------------------------------------------
    def evaluate(
        self,
        decision: Decision,
        portfolio,
        market_state,
        equity_prices: dict = None,
        market_downtrend_pct: float = 0.0,
    ):
        """
        equity_prices        — full {symbol: price} map for the current day.
        market_downtrend_pct — fraction (0–1) of active universe stocks currently
                               in a DOWNTREND regime. Used by the breadth circuit
                               breaker to suppress BUY signals during systemic selloffs.
        """
        symbol        = decision.symbol
        current_price = market_state.latest_price
        atr           = market_state.indicators.get("atr_14")
        regime        = market_state.indicators.get("regime")

        # --- Breadth circuit breaker (BUY only) ---
        # Suppresses all new entries when the broad market is in a systemic
        # downtrend, regardless of individual stock regime or RSI level.
        if (
            decision.action == "BUY"
            and self.breadth_circuit_breaker
            and market_downtrend_pct >= self.max_downtrend_pct
        ):
            return Decision(
                symbol=symbol,
                action="HOLD",
                reasoning=f"Market breadth circuit breaker: {market_downtrend_pct:.0%} in DOWNTREND",
            )

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

        # BUY
        if decision.action == "BUY":
            if symbol in portfolio.positions:
                return Decision(symbol=symbol, action="HOLD")

            quantity = self._size_position(total_equity, current_price, atr)
            if quantity <= 0:
                return Decision(symbol=symbol, action="HOLD")

            # Cap to actual available cash (unrealized gains cannot be spent)
            max_cash_qty = portfolio.cash // current_price
            quantity = min(quantity, max_cash_qty)
            if quantity <= 0:
                return Decision(symbol=symbol, action="HOLD")

            return Decision(
                symbol=symbol,
                action="BUY",
                quantity=quantity,
                reasoning=self._sizing_reasoning(total_equity, current_price, atr, quantity),
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

    # --------------------------------------------------
    # POSITION SIZING
    # --------------------------------------------------
    def _size_position(self, total_equity: float, price: float, atr) -> int:
        """
        Volatility-adjusted sizing: each position risks a fixed fraction of
        portfolio equity regardless of the stock's absolute volatility.

            quantity = (portfolio_risk_budget) / (atr_stop_distance_per_share)
                     = (equity * risk_per_trade_pct) / (atr_multiplier * atr)

        Falls back to fixed max_position_pct allocation when ATR is missing.
        The result is further capped at max_position_pct of equity to prevent
        a single position from becoming too large in low-vol environments.
        """
        if self.use_vol_sizing and atr and atr > 0:
            risk_budget = total_equity * self.risk_per_trade_pct
            stop_distance = self.atr_multiplier * atr   # per-share risk in price units
            vol_qty = risk_budget / stop_distance        # shares to risk exactly risk_budget

            # Hard cap: no position > max_position_pct of equity
            max_qty = (total_equity * self.max_position_pct) // price
            quantity = min(int(vol_qty), int(max_qty))
        else:
            # Fallback to fixed-% sizing
            quantity = int((total_equity * self.max_position_pct) // price)

        return quantity

    def _sizing_reasoning(self, total_equity, price, atr, quantity) -> str:
        if self.use_vol_sizing and atr and atr > 0:
            risk_budget = total_equity * self.risk_per_trade_pct
            return (
                f"VolSizing: {quantity} shares × {self.atr_multiplier}×ATR({atr:.2f}) "
                f"= ₹{quantity * self.atr_multiplier * atr:,.0f} risk "
                f"(budget ₹{risk_budget:,.0f})"
            )
        return f"FixedAlloc: {self.max_position_pct * 100:.1f}% of equity"
