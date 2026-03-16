from datetime import datetime

from app.strategy.models import Decision


class RSIMeanReversionStrategy:
    """
    Short-term mean-reversion strategy using RSI_3.

    Entry:  RSI_3 drops below `rsi_oversold`  — extreme oversold, expect a bounce.
    Exit:   RSI_3 rises above `rsi_overbought` — mean-reversion target reached.
    Exit:   Position held for `max_hold_days`   — time-based stop.

    Horizon: 1–5 days.

    Implementation note
    -------------------
    Multi-symbol strategies must emit an explicit HOLD decision for every held position
    that has no other action. Without this, the RiskAgent's ATR stop check is never
    triggered for that symbol (RiskAgent only runs when it receives a Decision).
    For a 1–5 day mean-reversion strategy the ATR stop is the primary protection
    against a position that gaps down before the time-stop fires.
    """

    def __init__(
        self,
        rsi_oversold:   float = 10.0,
        rsi_overbought: float = 70.0,
        max_hold_days:  int   = 5,
    ):
        self.rsi_oversold   = rsi_oversold
        self.rsi_overbought = rsi_overbought
        self.max_hold_days  = max_hold_days

        self._entry_dates: dict[str, datetime] = {}

    def decide(
        self,
        current_date:  datetime,
        symbol_states: dict,
        portfolio,
    ) -> list[Decision]:

        # Remove stale tracking for positions closed outside this strategy
        stale = [s for s in self._entry_dates if s not in portfolio.positions]
        for s in stale:
            del self._entry_dates[s]

        decisions = []

        for symbol, state in symbol_states.items():

            rsi_3 = state.indicators.get("rsi_3")
            if rsi_3 is None:
                continue

            in_position = symbol in portfolio.positions

            # --- Exit ---
            if in_position:

                # Time-based stop
                if symbol in self._entry_dates:
                    days_held = (current_date - self._entry_dates[symbol]).days
                    if days_held >= self.max_hold_days:
                        decisions.append(Decision(
                            symbol=symbol,
                            action="SELL",
                            reasoning=(
                                f"Max hold period reached "
                                f"({days_held}d >= {self.max_hold_days}d)"
                            ),
                        ))
                        del self._entry_dates[symbol]
                        continue

                # Mean-reversion target
                if rsi_3 > self.rsi_overbought:
                    decisions.append(Decision(
                        symbol=symbol,
                        action="SELL",
                        reasoning=(
                            f"Mean reversion exit "
                            f"(RSI_3={rsi_3:.1f} > {self.rsi_overbought})"
                        ),
                    ))
                    self._entry_dates.pop(symbol, None)
                    continue

                # --- Still holding: emit HOLD so RiskAgent can check ATR stop ---
                # Without this explicit HOLD, RiskAgent.evaluate() is never called
                # for this symbol and the ATR stop is silently skipped.
                days_held = (
                    (current_date - self._entry_dates[symbol]).days
                    if symbol in self._entry_dates else 0
                )
                decisions.append(Decision(
                    symbol=symbol,
                    action="HOLD",
                    reasoning=(
                        f"Awaiting mean-reversion exit "
                        f"(RSI_3={rsi_3:.1f}, held {days_held}d of {self.max_hold_days}d)"
                    ),
                ))
                continue

            # --- Entry ---
            elif rsi_3 < self.rsi_oversold:
                decisions.append(Decision(
                    symbol=symbol,
                    action="BUY",
                    reasoning=(
                        f"Oversold bounce signal "
                        f"(RSI_3={rsi_3:.1f} < {self.rsi_oversold})"
                    ),
                ))
                self._entry_dates[symbol] = current_date

        return decisions
