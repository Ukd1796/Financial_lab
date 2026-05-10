from datetime import datetime

from app.strategy.models import Decision

_DEFAULT_TARGET_MULTS: dict[str, float] = {
    "LOW_VOL": 1.03,   # slow markets — 3% reachable; 5% tends to fire time-stop instead
    "MID_VOL": 1.05,   # unchanged from prior behaviour
    "HIGH_VOL": 1.08,  # volatile markets — recovery can run further before cutting
}


class TrendPullbackStrategy:
    """
    Buy short-term pullbacks inside a confirmed, rising medium-term uptrend.

    Entry conditions (all must hold simultaneously):
      1. SMA_20 > SMA_50            — medium-term uptrend intact
      2. SMA_20 slope > 0           — trend is still accelerating, not topping
      3. price_3d_ago > SMA_20*1.05 — stock was in a strong trend before the pullback
                                      (eliminates weak-trend false entries)
      4. return_3d < -pullback_pct  — 3-day pullback has occurred

    Exit (profit):  price > SMA_20 * 1.05  — recovered to pre-pullback strength
                    (consistent with entry: we exit when the stock returns to the
                     same "strong trend" zone it was in before the pullback)
    Exit (time):    held > max_hold_days    — no recovery → cut it

    Why price_3d_ago instead of current price:
      The pullback has already happened at the point of signal generation, so checking
      current price > SMA_20 * 1.05 would exclude valid entries where the stock has
      already pulled back to ~SMA_20 * 1.02. Using price_3d_ago (reconstructed from
      return_3d) checks the pre-pullback level accurately.

    Implementation note
    -------------------
    Multi-symbol strategies must emit an explicit HOLD decision for every held position
    that has no other action. Without this, the RiskAgent's ATR stop check is never
    triggered for that symbol (RiskAgent only runs when it receives a Decision).
    """

    def __init__(
        self,
        pullback_threshold: float = 0.03,
        max_hold_days:      int   = 10,
        target_mult_by_vol: dict | None = None,
    ):
        self.pullback_threshold = pullback_threshold
        self.max_hold_days      = max_hold_days
        self.target_mult_by_vol = (
            target_mult_by_vol if target_mult_by_vol is not None
            else _DEFAULT_TARGET_MULTS
        )

        # Track entry date per symbol so max_hold_days can be enforced
        self._entry_dates: dict[str, datetime] = {}

    def _exit_mult(self, regime: str | None) -> float:
        """Exit-target multiplier based on vol-state component of regime.

        Entry check always stays at 1.05 so quality-of-trend filter is unchanged.
        Only the profit exit varies: LOW_VOL gets a closer target (achievable in
        slow markets), HIGH_VOL gets a wider target (lets recoveries run further).
        Falls back to MID_VOL (1.05) for warm-up bars where vol_state is NaN.
        """
        if not regime or not isinstance(regime, str):
            return self.target_mult_by_vol.get("MID_VOL", 1.05)
        parts = regime.split("_")
        if len(parts) < 3:                        # "nan_UPTREND" during ATR warm-up
            return self.target_mult_by_vol.get("MID_VOL", 1.05)
        vol_state = "_".join(parts[:2])           # "LOW_VOL", "MID_VOL", "HIGH_VOL"
        return self.target_mult_by_vol.get(
            vol_state, self.target_mult_by_vol.get("MID_VOL", 1.05)
        )

    def decide(
        self,
        current_date:  datetime,
        symbol_states: dict,
        portfolio,
    ) -> list[Decision]:

        decisions = []

        for symbol, state in symbol_states.items():

            price     = state.latest_price
            sma_20    = state.indicators.get("sma_20")
            sma_50    = state.indicators.get("sma_50")
            return_3d = state.indicators.get("return_3d")
            regime    = state.indicators.get("regime")

            # Previous day's SMA_20 — used to compute slope
            sma_20_prev = state.previous_indicators.get("sma_20")

            if None in (sma_20, sma_50, return_3d, sma_20_prev):
                continue

            # Exit target varies by vol regime; entry check stays fixed at 1.05
            # so the pre-pullback quality filter is never weakened.
            exit_m      = self._exit_mult(regime)
            exit_target = sma_20 * exit_m

            in_position = symbol in portfolio.positions

            if in_position:
                hold_days = (
                    (current_date - self._entry_dates[symbol]).days
                    if symbol in self._entry_dates else 0
                )

                # --- Exit 1: recovered to pre-pullback strength ---
                # Exit threshold is regime-conditional: LOW_VOL uses ×1.03 (reachable
                # in slow markets), HIGH_VOL uses ×1.08 (lets recovery run further).
                # Entry check stays at ×1.05 so we only enter on genuinely strong trends.
                if price > exit_target:
                    if symbol in self._entry_dates:
                        del self._entry_dates[symbol]
                    decisions.append(Decision(
                        symbol=symbol,
                        action="SELL",
                        reasoning=(
                            f"Recovered to pre-pullback strength "
                            f"(price={price:.2f} > SMA_20×{exit_m:.2f}={exit_target:.2f}, "
                            f"held {hold_days}d)"
                        ),
                    ))
                    continue

                # --- Exit 2: max hold days exceeded — trend break, not a pullback ---
                if hold_days >= self.max_hold_days:
                    if symbol in self._entry_dates:
                        del self._entry_dates[symbol]
                    decisions.append(Decision(
                        symbol=symbol,
                        action="SELL",
                        reasoning=(
                            f"Max hold days ({self.max_hold_days}d) exceeded — "
                            f"no recovery (price={price:.2f}, SMA_20={sma_20:.2f})"
                        ),
                    ))
                    continue

                # --- Still holding: emit HOLD so RiskAgent can check ATR stop ---
                decisions.append(Decision(
                    symbol=symbol,
                    action="HOLD",
                    reasoning=f"Waiting for recovery (held {hold_days}d of {self.max_hold_days}d max)",
                ))
                continue

            # --- Entry: strong uptrend + rising SMA_20 + pullback ---
            #
            # price_3d_ago: reconstructed price 3 trading days ago.
            # Checked against SMA_20 * 1.05 to confirm the stock was in a strong
            # trend *before* the pullback began — not just marginally above SMA_20.
            # Avoids entering stocks that are weakening toward SMA_20 with no strength.
            if return_3d <= -1.0:
                # Edge-case guard: return of -100% or worse means data is bad
                continue
            price_3d_ago = price / (1.0 + return_3d)

            if (
                not in_position
                and sma_20 > sma_50                           # medium-term uptrend
                and sma_20 > sma_20_prev                      # SMA_20 slope > 0
                and price_3d_ago > sma_20 * 1.05             # was in strong trend
                and return_3d < -self.pullback_threshold      # pullback occurred
            ):
                self._entry_dates[symbol] = current_date
                decisions.append(Decision(
                    symbol=symbol,
                    action="BUY",
                    reasoning=(
                        f"Pullback in strong rising uptrend "
                        f"(return_3d={return_3d * 100:.1f}%, "
                        f"price_3d_ago={price_3d_ago:.2f} > SMA_20*1.05={sma_20 * 1.05:.2f}, "
                        f"SMA_20 slope={sma_20 - sma_20_prev:.3f})"
                    ),
                ))

        return decisions
