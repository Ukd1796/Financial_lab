# app/risk/strategy_pnl_tracker.py
#
# StrategyPnLTracker — pure bookkeeping of per-strategy realized P&L over
# rolling trading-day windows.
#
# Used by PerformanceFeedbackAgent to feed recent strategy performance back
# into the LLM prompt (PAA / "performance-aware adaptive" experiment, Phase 1).
#
# Design notes
# ------------
# - Pure stdlib; no app imports. Easy to unit-test in isolation.
# - Realized P&L only. We could attribute unrealized P&L too by joining
#   `portfolio.positions` with `router.position_owners`, but for the
#   rebalance decision the realized number is the cleanest signal —
#   "what has each strategy actually earned for the portfolio in the last
#   N trading days?" Unrealized swings can flip from one rebalance to the
#   next; realized fills are committed evidence.
# - Window normalisation: contribution % = sum(realized_pnl in window) /
#   mean(equity in window). This is approximate ("contribution as % of
#   average portfolio size") rather than time-weighted return — sufficient
#   for the LLM's purposes (the relative ranking between strategies is
#   what matters, not exact return measurement).
# - All windows share a single max-horizon deque per strategy. Aggregating
#   sub-windows is just iterating the suffix.

from __future__ import annotations

from collections import deque
from datetime import datetime
from typing import Optional


class StrategyPnLTracker:
    """
    Per-strategy realized-P&L bookkeeping over rolling trading-day windows.

    Parameters
    ----------
    strategy_names : list[str]
        Names matching MultiStrategyRouter / Decision.source.
    max_window_days : int, default 30
        Longest rolling window we will ever query. Bounds the per-strategy
        fill deque and the equity deque. Queries beyond this are clamped.
    """

    def __init__(self, strategy_names: list[str], max_window_days: int = 30):
        self.strategy_names = list(strategy_names)
        self.max_window_days = max_window_days

        # Per strategy: deque of (date, pnl) for every SELL fill, capped to
        # max_window_days * a generous trades-per-day multiplier. We don't
        # actually cap by trade count — we filter by date at query time, so
        # the cap is just to avoid unbounded memory growth.
        self._fills: dict[str, deque] = {
            s: deque(maxlen=max_window_days * 50) for s in strategy_names
        }
        # End-of-day equity snapshots, capped to max_window_days entries.
        self._equity: deque = deque(maxlen=max_window_days)

        # Lifetime counters for harness-level verification ("did this thing
        # actually get fed during the run?"). Never reset; safe to log at
        # end-of-period to confirm wiring is intact.
        self.fill_count: int = 0
        self.equity_snapshot_count: int = 0

    # ------------------------------------------------------------------
    # WRITE PATH — called by BacktestEngine
    # ------------------------------------------------------------------
    def record_fill(
        self,
        date: datetime,
        strategy_name: str,
        action: str,
        pnl: float,
    ) -> None:
        """
        Record a SELL fill's net P&L for the named strategy. BUYs and HOLDs
        are no-ops (entry P&L is implicit in the eventual exit's trade_pnl).

        `strategy_name` should be `Decision.source` as set by MultiStrategyRouter
        — the strategy that originally opened the position (router's ownership
        rule guarantees the SELL comes from the owner).
        """
        if action != "SELL":
            return
        if strategy_name not in self._fills:
            # Unknown strategy (e.g. ATR trailing stop with no source) — skip
            # rather than raise; this keeps the tracker robust to engine quirks.
            return
        self._fills[strategy_name].append((date, float(pnl)))
        self.fill_count += 1

    def record_daily_equity(self, date: datetime, equity: float) -> None:
        """Record end-of-day portfolio equity. Called once per trading day."""
        self._equity.append((date, float(equity)))
        self.equity_snapshot_count += 1

    # ------------------------------------------------------------------
    # READ PATH — called by PerformanceFeedbackAgent
    # ------------------------------------------------------------------
    def is_warm(self, min_days: int = 5) -> bool:
        """True once we have ≥ min_days of equity snapshots."""
        return len(self._equity) >= min_days

    def rolling_contribution_pct(
        self,
        strategy_name: str,
        window_days: int,
    ) -> Optional[float]:
        """
        Return strategy contribution as a fraction (e.g. -0.052 for -5.2%)
        over the last `window_days` trading days. None if not warm enough.

        Formula:
            contribution_pct = sum(pnl_in_window) / mean(equity_in_window)

        Edge cases:
            - If window_days > current equity history length, uses what we have.
            - If mean equity is 0 (unusual), returns 0.0.
        """
        if strategy_name not in self._fills:
            return None
        if not self._equity:
            return None

        # Effective window — clamp to what we actually have.
        n = min(window_days, len(self._equity))
        if n <= 0:
            return None

        # Reference date: the most recent equity snapshot.
        # Fills counted: those with date > (ref - n equity entries) in date order.
        # We use the date of the (-n)th equity snapshot as the cutoff so the
        # window aligns with trading days, not calendar days.
        cutoff_date = self._equity[-n][0]

        fills = self._fills[strategy_name]
        pnl_sum = sum(p for (d, p) in fills if d >= cutoff_date)

        equity_window = list(self._equity)[-n:]
        mean_equity = sum(e for (_, e) in equity_window) / len(equity_window)
        if mean_equity <= 0:
            return 0.0

        return pnl_sum / mean_equity

    def all_contributions(self, window_days: int) -> dict[str, Optional[float]]:
        """Convenience: contribution for every tracked strategy at one window."""
        return {
            s: self.rolling_contribution_pct(s, window_days)
            for s in self.strategy_names
        }
