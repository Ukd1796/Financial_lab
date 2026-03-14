import bisect

from app.strategy.models import Decision


class CrossSectionalMomentumStrategy:
    """
    Cross-sectional momentum strategy.

    Ranks symbols by N-day return, buys top-K, sells positions that drop out.
    Rebalances every `rebalance_frequency` trading days.

    Price feed modes
    ----------------
    Preferred — call preload_price_feed(price_feed) before the backtest loop.
        `price_feed` is a dict {symbol: {date: close_price}} covering the full
        backtest range with a warm-up buffer. Momentum is then computed from
        actual historical data on every rebalance day regardless of how many
        times a stock appeared in the daily filtered universe.

    Fallback — if preload_price_feed() is never called, price history is
        accumulated incrementally from symbol_states (original behaviour).
        This only works when a symbol appears in symbol_states consistently
        for at least `lookback_days` consecutive sessions.
    """

    def __init__(
        self,
        lookback_days:       int   = 100,
        top_n:               int   = 3,
        rebalance_frequency: int   = 20,
        momentum_threshold:  float = 0.05,
    ):
        self.lookback_days        = lookback_days
        self.top_n                = top_n
        self.rebalance_frequency  = rebalance_frequency
        self.momentum_threshold   = momentum_threshold

        self.last_rebalance_date  = None

        # Pre-loaded price feed (set via preload_price_feed)
        self._price_feed:    dict = {}   # symbol → {date: close_price}
        self._sorted_dates:  dict = {}   # symbol → sorted list of dates (cache)

        # Fallback incremental history
        self.price_history:  dict = {}

    # ------------------------------------------------------------------
    # PRELOAD
    # ------------------------------------------------------------------
    def preload_price_feed(self, price_feed: dict) -> None:
        """
        Accept a pre-built {symbol: {date: close_price}} dict so that
        momentum lookbacks are computed against real historical data rather
        than the incrementally-accumulated symbol_states history.

        Called once per backtest run from run_experiment() before engine.run().
        """
        self._price_feed   = price_feed
        self._sorted_dates = {
            symbol: sorted(dates.keys())
            for symbol, dates in price_feed.items()
        }

    # ------------------------------------------------------------------
    # DECIDE
    # ------------------------------------------------------------------
    def decide(self, current_date, symbol_states: dict, portfolio):

        # Rebalance gate
        if self.last_rebalance_date is None:
            self.last_rebalance_date = current_date

        if (current_date - self.last_rebalance_date).days < self.rebalance_frequency:
            return []

        self.last_rebalance_date = current_date

        # Compute momentum for every visible symbol
        momentum_scores = []
        for symbol, state in symbol_states.items():
            momentum = self._compute_momentum(symbol, state.latest_price, current_date)
            if momentum is not None and momentum > self.momentum_threshold:
                momentum_scores.append((symbol, momentum))

        if not momentum_scores:
            return []

        selected = [
            s for s, _ in
            sorted(momentum_scores, key=lambda x: x[1], reverse=True)[: self.top_n]
        ]

        decisions = []

        # Exit positions that dropped out of the top-N
        for held in list(portfolio.positions):
            if held not in selected:
                decisions.append(Decision(
                    symbol=held,
                    action="SELL",
                    quantity=portfolio.positions[held].quantity,
                    reasoning="Dropped from top momentum ranking",
                ))

        # Enter new top-N positions
        for symbol in selected:
            if symbol not in portfolio.positions:
                decisions.append(Decision(
                    symbol=symbol,
                    action="BUY",
                    quantity=None,
                    reasoning="Selected by momentum ranking",
                ))

        return decisions

    # ------------------------------------------------------------------
    # INTERNAL
    # ------------------------------------------------------------------
    def _compute_momentum(
        self,
        symbol:       str,
        latest_price: float,
        current_date,
    ) -> float | None:
        """
        Return the N-day price momentum for `symbol` as of `current_date`.

        Uses the pre-loaded price feed when available (preferred), otherwise
        falls back to the incrementally accumulated price_history.
        """
        if self._price_feed:
            dates = self._sorted_dates.get(symbol)
            if not dates:
                return None

            # Index of the last date strictly before current_date
            idx = bisect.bisect_left(dates, current_date) - 1
            if idx < self.lookback_days:
                return None

            past_price = self._price_feed[symbol][dates[idx - self.lookback_days]]
            if past_price == 0:
                return None

            return (latest_price / past_price) - 1

        # Fallback: accumulate from symbol_states
        self.price_history.setdefault(symbol, []).append(latest_price)
        history = self.price_history[symbol]
        if len(history) < self.lookback_days:
            return None
        return (latest_price / history[-self.lookback_days]) - 1
