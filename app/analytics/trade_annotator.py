"""
Trade Analytics Layer
---------------------
Post-hoc enrichment of completed Trade objects with excursion metrics,
post-exit drift, regime at entry, and strategy attribution.

All OHLC data comes from the already-loaded OHLCCache — no extra DB queries.
Observer cache is used for regime reconstruction (already preloaded during run).
"""

from __future__ import annotations

import csv
import os
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import List, Optional


# ---------------------------------------------------------------------------
# Enriched Trade dataclass
# ---------------------------------------------------------------------------

@dataclass
class EnrichedTrade:
    # --- From backtest Trade ---
    strategy: str
    symbol: str
    entry_date: datetime
    exit_date: datetime
    entry_price: float
    exit_price: float
    quantity: float
    pnl: float
    # --- Derived ---
    holding_days: int
    final_return_pct: float
    # --- Excursion metrics ---
    mfe_pct: float            # max favorable excursion during hold
    mae_pct: float            # max adverse excursion during hold (negative)
    mfe_efficiency: float     # final_return / mfe; 1.0 = perfect exit at peak
    # --- Post-exit drift ---
    drift_1d: Optional[float]
    drift_3d: Optional[float]
    drift_5d: Optional[float]
    continuation_success: bool    # True if drift_5d > 0
    breakout_survival_days: int   # consecutive days close >= entry_price
    # --- Context at entry ---
    regime_at_entry: str
    weight_at_entry: float        # strategy weight; 0.0 when not captured
    universe_rank_at_entry: int   # 1-indexed rank; 0 when not in universe
    # --- Period label (set by caller) ---
    period_label: str = ""
    run_label: str = ""


# ---------------------------------------------------------------------------
# Strategy Attribution Tracker
# ---------------------------------------------------------------------------

class TradeAttributionTracker:
    """
    Minimal pnl_tracker-compatible object that captures strategy attribution
    for multi-strategy runs.  Passed as `pnl_tracker` to run_experiment().

    BacktestEngine calls record_fill(..., action="SELL") with owning_strategy
    after each closed trade.  We store (exit_date, pnl) → strategy so the
    TradeAnnotator can look up attribution per trade in post-processing.

    Interface is compatible with StrategyPnLTracker so BacktestEngine accepts
    it without modification.
    """

    def __init__(self, strategy_names: List[str]):
        self.strategy_names = list(strategy_names)
        self.fill_count: int = 0
        self.equity_snapshot_count: int = 0
        self._sells: List[tuple] = []   # (exit_date, pnl_float, strategy_name)

    # --- Write path (called by BacktestEngine) ---

    def record_fill(self, date: datetime, strategy_name: str, action: str, pnl: float) -> None:
        if action != "SELL":
            return
        self._sells.append((date, float(pnl), strategy_name))
        self.fill_count += 1

    def record_daily_equity(self, date: datetime, equity: float) -> None:
        self.equity_snapshot_count += 1

    # --- Read path (called by TradeAnnotator) ---

    def get_strategy(self, exit_date: datetime, pnl: float) -> str:
        """Match a trade by (exit_date, pnl) → strategy name."""
        for d, p, s in self._sells:
            if d == exit_date and abs(p - pnl) < 0.01:
                return s
        return ""

    # --- No-op stubs required by PerformanceFeedbackAgent interface ---

    def is_warm(self, min_days: int = 5) -> bool:
        return False

    def rolling_contribution_pct(self, strategy_name: str, window_days: int) -> Optional[float]:
        return None

    def all_contributions(self, window_days: int) -> dict:
        return {s: None for s in self.strategy_names}


# ---------------------------------------------------------------------------
# Composite tracker: wraps two pnl_trackers so both get fed simultaneously
# ---------------------------------------------------------------------------

class CompositePnLTracker:
    """
    Delegates to two pnl_tracker objects.  Used when both PAA and analytics
    tracking are active (USE_PERFORMANCE_FEEDBACK=True).
    The primary tracker's read-path methods (rolling_contribution_pct etc.)
    are used by PerformanceFeedbackAgent; attribution tracker handles the rest.
    """

    def __init__(self, primary, secondary):
        self._primary   = primary
        self._secondary = secondary
        # Expose counters from primary so PAA verification print in run_experiments
        # still works (it reads .fill_count, .equity_snapshot_count).
        self.fill_count = 0
        self.equity_snapshot_count = 0

    def record_fill(self, date, strategy_name, action, pnl):
        self._primary.record_fill(date, strategy_name, action, pnl)
        self._secondary.record_fill(date, strategy_name, action, pnl)
        if action == "SELL":
            self.fill_count += 1

    def record_daily_equity(self, date, equity):
        self._primary.record_daily_equity(date, equity)
        self._secondary.record_daily_equity(date, equity)
        self.equity_snapshot_count += 1

    # Delegate PAA read-path to primary
    def is_warm(self, min_days=5):
        return self._primary.is_warm(min_days)

    def rolling_contribution_pct(self, strategy_name, window_days):
        return self._primary.rolling_contribution_pct(strategy_name, window_days)

    def all_contributions(self, window_days):
        return self._primary.all_contributions(window_days)

    def any_bleeding(self):
        return getattr(self._primary, "any_bleeding", lambda: [])()


# ---------------------------------------------------------------------------
# Trade Annotator
# ---------------------------------------------------------------------------

class TradeAnnotator:
    """
    Enriches a list of Trade objects with excursion metrics, post-exit drift,
    and context at entry.

    Parameters
    ----------
    ohlc_cache : OHLCCache
        Already-loaded cache; provides get_ohlc(symbol, start, end).
    observer : MarketObserverAgent, optional
        Already-preloaded observer; used for regime-at-entry reconstruction.
    """

    def __init__(self, ohlc_cache, observer=None):
        self._cache    = ohlc_cache
        self._observer = observer

    def annotate(
        self,
        trades,
        strategy_label: str = "",
        attribution_tracker: Optional[TradeAttributionTracker] = None,
        universe_tracker=None,
        period_label: str = "",
        run_label: str = "",
    ) -> List[EnrichedTrade]:
        """
        Enrich raw Trade objects.

        strategy_label        — used for solo-strategy runs (one strategy per run).
        attribution_tracker   — used for multi-strategy runs; maps pnl→strategy.
        universe_tracker      — UniverseTracker from compute_universe_diagnostics();
                                used to look up universe rank at entry.
        """
        enriched = []
        for trade in trades:
            enriched.append(
                self._enrich(
                    trade,
                    strategy_label,
                    attribution_tracker,
                    universe_tracker,
                    period_label,
                    run_label,
                )
            )
        return enriched

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _enrich(
        self, trade, strategy_label, attribution_tracker,
        universe_tracker, period_label, run_label,
    ) -> EnrichedTrade:

        symbol = trade.symbol

        # Strategy
        if attribution_tracker is not None:
            strategy = attribution_tracker.get_strategy(trade.exit_date, trade.pnl) or strategy_label
        else:
            strategy = strategy_label

        holding_days = max((trade.exit_date - trade.entry_date).days, 0)
        final_return_pct = (
            (trade.exit_price - trade.entry_price) / trade.entry_price
            if trade.entry_price > 0 else 0.0
        )

        # OHLC window for hold period (entry → exit)
        hold_window = self._cache.get_ohlc(symbol, trade.entry_date, trade.exit_date)
        mfe_pct, mae_pct = self._excursions(hold_window, trade.entry_price)
        survival_days    = self._breakout_survival(hold_window, trade.entry_price)

        mfe_efficiency = (
            final_return_pct / mfe_pct if mfe_pct > 1e-6
            else (1.0 if final_return_pct >= 0 else 0.0)
        )
        # Clamp to [-1, 2] so extreme values (e.g. exit before any excursion)
        # don't distort aggregate stats.
        mfe_efficiency = max(-1.0, min(2.0, mfe_efficiency))

        # Post-exit drift
        drift_1d = self._drift(symbol, trade.exit_date, 1)
        drift_3d = self._drift(symbol, trade.exit_date, 3)
        drift_5d = self._drift(symbol, trade.exit_date, 5)
        continuation_success = (drift_5d or 0.0) > 0.0

        # Regime at entry
        regime_at_entry = self._regime(symbol, trade.entry_date)

        # Universe rank at entry
        universe_rank = self._universe_rank(symbol, trade.entry_date, universe_tracker)

        return EnrichedTrade(
            strategy=strategy,
            symbol=symbol,
            entry_date=trade.entry_date,
            exit_date=trade.exit_date,
            entry_price=trade.entry_price,
            exit_price=trade.exit_price,
            quantity=trade.quantity,
            pnl=trade.pnl,
            holding_days=holding_days,
            final_return_pct=final_return_pct,
            mfe_pct=mfe_pct,
            mae_pct=mae_pct,
            mfe_efficiency=mfe_efficiency,
            drift_1d=drift_1d,
            drift_3d=drift_3d,
            drift_5d=drift_5d,
            continuation_success=continuation_success,
            breakout_survival_days=survival_days,
            regime_at_entry=regime_at_entry,
            weight_at_entry=0.0,
            universe_rank_at_entry=universe_rank,
            period_label=period_label,
            run_label=run_label,
        )

    def _excursions(self, ohlc_window, entry_price: float):
        """MFE% and MAE% from daily highs/lows during the hold period."""
        if not ohlc_window or entry_price <= 0:
            return 0.0, 0.0
        max_high = max(r.high for r in ohlc_window)
        min_low  = min(r.low  for r in ohlc_window)
        return (
            (max_high - entry_price) / entry_price,
            (min_low  - entry_price) / entry_price,   # negative
        )

    def _breakout_survival(self, ohlc_window, entry_price: float) -> int:
        """Consecutive trading days (from entry) close stayed >= entry_price."""
        if not ohlc_window or entry_price <= 0:
            return 0
        count = 0
        for r in sorted(ohlc_window, key=lambda x: x.timestamp):
            if r.close >= entry_price:
                count += 1
            else:
                break
        return count

    def _drift(self, symbol: str, exit_date: datetime, n_days: int) -> Optional[float]:
        """
        n-day price drift after exit, measured open-of-next-day to close-of-Nth-day.
        Returns None when insufficient post-exit data.
        """
        # Fetch a window large enough to cover n_days of trading (+ holiday buffer)
        window_end = exit_date + timedelta(days=n_days + 7)
        records    = self._cache.get_ohlc(symbol, exit_date, window_end)
        forward    = [r for r in records if r.timestamp > exit_date]
        if len(forward) < n_days:
            return None
        ref_price = forward[0].open
        if ref_price <= 0:
            return None
        target_close = forward[min(n_days - 1, len(forward) - 1)].close
        return (target_close - ref_price) / ref_price

    def _regime(self, symbol: str, entry_date: datetime) -> str:
        """Stock-level regime at entry from the already-preloaded observer cache."""
        if self._observer is None:
            return ""
        try:
            state = self._observer.run_for_day(symbol, entry_date)
            if state and state.indicators:
                return str(state.indicators.get("regime", ""))
        except Exception:
            pass
        return ""

    def _universe_rank(self, symbol: str, entry_date: datetime, tracker) -> int:
        """
        1-indexed position of symbol in the universe on or near entry_date.
        Returns 0 when symbol was not in the universe that day.
        """
        if tracker is None or not tracker.daily_records:
            return 0
        # Find the record whose date is closest to entry_date (within 3 trading days)
        closest = min(
            tracker.daily_records,
            key=lambda r: abs((r.date - entry_date).days),
        )
        if abs((closest.date - entry_date).days) > 3:
            return 0
        try:
            return closest.symbols.index(symbol) + 1
        except ValueError:
            return 0


# ---------------------------------------------------------------------------
# CSV export
# ---------------------------------------------------------------------------

def export_enriched_trades_csv(
    enriched_trades: List[EnrichedTrade], path: str
) -> None:
    """Append enriched trades to a CSV file (creates with header if new)."""
    if not enriched_trades:
        return
    write_header = not os.path.exists(path) or os.path.getsize(path) == 0
    with open(path, "a", newline="") as f:
        w = csv.writer(f)
        if write_header:
            w.writerow([
                "period", "run",
                "strategy", "symbol",
                "entry_date", "exit_date", "holding_days",
                "entry_price", "exit_price",
                "final_return_pct", "pnl",
                "mfe_pct", "mae_pct", "mfe_efficiency",
                "drift_1d", "drift_3d", "drift_5d",
                "continuation_success", "breakout_survival_days",
                "regime_at_entry", "weight_at_entry", "universe_rank_at_entry",
            ])
        for t in enriched_trades:
            def fmt_pct(v):
                return f"{v * 100:.3f}%" if v is not None else "N/A"

            w.writerow([
                t.period_label, t.run_label,
                t.strategy, t.symbol,
                t.entry_date.date(), t.exit_date.date(), t.holding_days,
                f"{t.entry_price:.2f}", f"{t.exit_price:.2f}",
                fmt_pct(t.final_return_pct), f"{t.pnl:.2f}",
                fmt_pct(t.mfe_pct), fmt_pct(t.mae_pct), f"{t.mfe_efficiency:.3f}",
                fmt_pct(t.drift_1d), fmt_pct(t.drift_3d), fmt_pct(t.drift_5d),
                int(t.continuation_success), t.breakout_survival_days,
                t.regime_at_entry, f"{t.weight_at_entry:.3f}", t.universe_rank_at_entry,
            ])
