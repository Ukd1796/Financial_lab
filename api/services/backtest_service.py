# api/services/backtest_service.py
#
# Orchestrates a backtest run in a background thread and stores results via
# api/db/store.py.  BacktestEngine is CPU-bound so we use a thread pool rather
# than asyncio coroutines.
#
# Mapping: UI strategy IDs → Financial Lab classes / internal names
#   trend-follow   → DualMA   (DualMovingAverageStrategy)
#   breakout       → Breakout (BreakoutMomentumStrategy)
#   quiet-breakout → QuietBrk (QuietBreakoutStrategy)
#   trend-pullback → TrendPB  (TrendPullbackStrategy)
#   mean-reversion → RSI-MR   (RSIMeanReversionStrategy)

from __future__ import annotations

import os
import traceback
from datetime import datetime, timedelta
from typing import Any

import numpy as np

from app.backtest.engine import BacktestEngine
from app.backtest.models import BacktestResult, Trade
from app.backtest.observer import MarketObserverAgent
from app.data.repository import MarketDataRepository
from app.evaluation.agent import EvaluationAgent
from app.execution.agent import ExecutionAgent
from app.meta.adaptive_selector import AdaptiveStrategySelector
from app.meta.regime_context_agent import RegimeContextAgent
from app.portfolio.engine import PortfolioEngine
from app.portfolio.models import Portfolio
from app.risk.agent import RiskAgent
from app.strategy.breakout_momentum import BreakoutMomentumStrategy
from app.strategy.dual_ma import DualMovingAverageStrategy
from app.strategy.multi_router import MultiStrategyRouter
from app.strategy.quiet_breakout import QuietBreakoutStrategy
from app.strategy.rsi_mean_reversion import RSIMeanReversionStrategy
from app.strategy.trend_pullback import TrendPullbackStrategy
from app.universe.agent import UniverseSelectionAgent
from app.universe.dynamic_agent import DynamicUniverseAgent
from app.universe.filters import (
    BreakoutUniverseFilter,
    DualMAUniverseFilter,
    MeanReversionUniverseFilter,
    PullbackUniverseFilter,
    UnionUniverseFilter,
)

import api.db.store as store
from api.services.narrative_service import generate_narrative

# Mirrors run_experiments.py
from run_experiments import NIFTY_50, NIFTY_NEXT_50, NIFTY_MIDCAP_50

NIFTY_100     = NIFTY_50 + NIFTY_NEXT_50
BROAD_UNIVERSE = NIFTY_50 + NIFTY_NEXT_50 + NIFTY_MIDCAP_50

UNIVERSE_SYMBOLS: dict[str, list[str]] = {
    "nifty50":  NIFTY_50,
    "nifty100": NIFTY_100,
    "broad150": BROAD_UNIVERSE,
}

# Regime allowlists (mirrors run_experiments.py)
_UPTREND_ONLY = ["LOW_VOL_UPTREND", "MID_VOL_UPTREND", "HIGH_VOL_UPTREND"]
_TREND_AND_SIDEWAYS = [
    "LOW_VOL_UPTREND", "MID_VOL_UPTREND", "HIGH_VOL_UPTREND",
    "LOW_VOL_SIDEWAYS", "MID_VOL_SIDEWAYS", "HIGH_VOL_SIDEWAYS",
]
_UPTREND_AND_SIDEWAYS = _TREND_AND_SIDEWAYS[:]

# Internal name → (allowed_regimes, universe_filter_factory, strategy_factory)
_STRATEGY_REGISTRY: dict[str, dict] = {
    "DualMA": {
        "factory":  lambda: DualMovingAverageStrategy(),
        "filter":   lambda: DualMAUniverseFilter(max_cross_age=5, top_n=30),
        "regimes":  _UPTREND_ONLY,
        "max_pos":  0.15,
    },
    "Breakout": {
        "factory":  lambda: BreakoutMomentumStrategy(),
        "filter":   lambda: BreakoutUniverseFilter(top_n=20),
        "regimes":  _TREND_AND_SIDEWAYS,
        "max_pos":  0.10,
    },
    "QuietBrk": {
        "factory":  lambda: QuietBreakoutStrategy(),
        "filter":   lambda: BreakoutUniverseFilter(vol_threshold=1.2, return_threshold=0.008, top_n=20),
        "regimes":  _UPTREND_ONLY,
        "max_pos":  0.10,
    },
    "TrendPB": {
        "factory":  lambda: TrendPullbackStrategy(pullback_threshold=0.05),
        "filter":   lambda: PullbackUniverseFilter(top_n=20),
        "regimes":  _TREND_AND_SIDEWAYS,
        "max_pos":  0.10,
    },
    "RSI-MR": {
        "factory":  lambda: RSIMeanReversionStrategy(rsi_oversold=5, rsi_overbought=80, max_hold_days=7),
        "filter":   lambda: MeanReversionUniverseFilter(top_n=20),
        "regimes":  _UPTREND_AND_SIDEWAYS,
        "max_pos":  0.10,
    },
}

# UI id → internal name
_UI_TO_INTERNAL = {
    "trend-follow":   "DualMA",
    "breakout":       "Breakout",
    "quiet-breakout": "QuietBrk",
    "trend-pullback": "TrendPB",
    "mean-reversion": "RSI-MR",
}

# Internal name → UI id (for trade log)
_INTERNAL_TO_UI = {v: k for k, v in _UI_TO_INTERNAL.items()}

# Standard periods for period breakdown (label, start, end, regime_label)
_PERIODS = [
    ("Bull Run",    "2019-01-01", "2020-02-01", "BULL_CONFIRMED"),
    ("COVID Crash", "2020-01-01", "2020-12-31", "BEAR_CONFIRMED"),
    ("Recovery",    "2020-04-01", "2021-12-31", "BULL_EARLY"),
    ("Bear 2022",   "2022-01-01", "2022-12-31", "BEAR_CONFIRMED"),
    ("Recent",      "2022-01-01", "2024-06-01", "SIDEWAYS_CHOPPY"),
    ("Live",        "2025-01-01", "2026-03-24", "BULL_WATCH"),
]


# ---------------------------------------------------------------------------
# Weight computation from UI config
# ---------------------------------------------------------------------------

def _compute_weights(strategies_cfg: list) -> dict[str, float]:
    """
    Map enabled UI strategies to internal names with weights.
    Floor weights are honoured; remainder is distributed equally.
    """
    enabled = [s for s in strategies_cfg if s["enabled"]]
    if not enabled:
        return {}

    floor_sum = sum(s.get("floor_weight", 0.0) for s in enabled)
    remainder = max(0.0, 1.0 - floor_sum)
    equal_share = remainder / len(enabled)

    weights: dict[str, float] = {}
    for s in enabled:
        internal = _UI_TO_INTERNAL.get(s["id"])
        if not internal:
            continue
        weights[internal] = s.get("floor_weight", 0.0) + equal_share

    # Normalise
    total = sum(weights.values())
    if total > 0:
        weights = {k: v / total for k, v in weights.items()}

    return weights


# ---------------------------------------------------------------------------
# Benchmark fetch (Nifty 50 index from yfinance)
# ---------------------------------------------------------------------------

def _fetch_nifty_prices(start_dt: datetime, end_dt: datetime) -> dict[str, float]:
    """Returns {date_str: close_price} for ^NSEI."""
    try:
        import yfinance as yf
        df = yf.download("^NSEI", start=start_dt.date(), end=end_dt.date(), auto_adjust=True, progress=False)
        if df.empty:
            return {}
        close = df["Close"] if "Close" in df.columns else df.iloc[:, 0]
        return {str(ts.date()): float(v) for ts, v in close.items() if not np.isnan(v)}
    except Exception:
        return {}


def _benchmark_return(nifty_prices: dict, start: str, end: str) -> float:
    """Return Nifty % return over [start, end] using the first/last available prices."""
    dates = sorted(k for k in nifty_prices if start <= k <= end)
    if len(dates) < 2:
        return 0.0
    p0, p1 = nifty_prices[dates[0]], nifty_prices[dates[-1]]
    return round((p1 - p0) / p0 * 100, 2) if p0 else 0.0


# ---------------------------------------------------------------------------
# Period breakdown helper
# ---------------------------------------------------------------------------

def _period_breakdown(
    results: list[BacktestResult],
    nifty_prices: dict,
    initial_capital: float,
) -> list[dict]:
    """
    Split equity_curve by standard periods and compute per-period metrics.
    """
    evaluator = EvaluationAgent()
    breakdown = []

    for label, start_str, end_str, regime in _PERIODS:
        start_dt = datetime.fromisoformat(start_str)
        end_dt   = datetime.fromisoformat(end_str)

        period_results = [r for r in results if start_dt <= r.date <= end_dt]
        if len(period_results) < 2:
            continue

        p0 = period_results[0].equity
        metrics = evaluator.evaluate(period_results, p0)

        vs_nifty = _benchmark_return(nifty_prices, start_str, end_str[:10])
        period_return = round(metrics.get("total_return", 0) * 100, 2)

        breakdown.append({
            "period":       label,
            "start_date":   start_str,
            "end_date":     end_str,
            "regime":       regime,
            "return_pct":   period_return,
            "max_dd_pct":   round(-abs(metrics.get("max_drawdown", 0)) * 100, 2),
            "sharpe":       round(metrics.get("sharpe_ratio", 0), 2),
            "vs_nifty_pct": round(period_return - vs_nifty, 2),
        })

    return breakdown


# ---------------------------------------------------------------------------
# Core backtest executor (runs in a thread pool)
# ---------------------------------------------------------------------------

def execute_backtest(run_id: str, config: dict) -> None:
    """
    Full backtest run. Called via asyncio.to_thread from the router.
    Updates the run record progressively so the polling endpoint reflects live status.
    """
    try:
        store.update_run_status(run_id, "running")
        store.update_run_progress(run_id, 5)

        # ------------------------------------------------------------------
        # Parse config
        # ------------------------------------------------------------------
        universe_key     = config.get("universe", "nifty100")
        universe_symbols = UNIVERSE_SYMBOLS.get(universe_key, NIFTY_100)
        risk_cfg         = config.get("risk", {})
        capital          = float(risk_cfg.get("capital_amount", 1_000_000))
        max_pos_pct      = float(risk_cfg.get("max_position_pct", 10.0)) / 100.0

        strategies_cfg = config.get("strategies", [])
        weights        = _compute_weights(strategies_cfg)

        if not weights:
            raise ValueError("No enabled strategies in config.")

        # ------------------------------------------------------------------
        # Date range: use config dates if provided, else fall back to defaults
        # ------------------------------------------------------------------
        today_dt = datetime.combine(datetime.utcnow().date(), datetime.min.time())
        start_dt = (
            datetime.fromisoformat(config["backtest_start"])
            if config.get("backtest_start")
            else datetime(2019, 1, 1)
        )
        end_dt = (
            datetime.fromisoformat(config["backtest_end"])
            if config.get("backtest_end")
            else today_dt
        )
        today_dt  = min(end_dt, today_dt)   # never exceed today
        buffer_dt = start_dt - timedelta(days=220)   # warm-up buffer

        store.update_run_progress(run_id, 10)

        # ------------------------------------------------------------------
        # Build shared infrastructure (mirrors PeriodContext in run_experiments)
        # ------------------------------------------------------------------
        repository = MarketDataRepository()

        dynamic_agent = DynamicUniverseAgent(
            repository=repository,
            symbols=BROAD_UNIVERSE,
            top_n=80,
        )
        dynamic_agent.preload(buffer_dt, today_dt)

        store.update_run_progress(run_id, 25)

        rca            = RegimeContextAgent(dynamic_agent)
        observer       = MarketObserverAgent(repository)
        universe_agent = UniverseSelectionAgent(
            volume_threshold=1.5, volatility_threshold=0.02, top_n=20
        )

        # Build union filter from active strategies
        active_internals = list(weights.keys())
        filter_instances = [_STRATEGY_REGISTRY[n]["filter"]() for n in active_internals]
        union_filter     = UnionUniverseFilter(filter_instances)

        # Timeline from dynamic agent cache
        timestamps = set()
        for df in dynamic_agent._cache.values():
            for ts in df.index:
                if start_dt <= ts <= today_dt:  # today_dt already capped to end_dt
                    timestamps.add(ts)
        historical_dates = sorted(timestamps)

        if not historical_dates:
            raise RuntimeError("No trading dates found in DB for the requested period.")

        store.update_run_progress(run_id, 35)

        # ------------------------------------------------------------------
        # Build MultiStrategyRouter
        # ------------------------------------------------------------------
        strategy_instances = {
            name: _STRATEGY_REGISTRY[name]["factory"]()
            for name in active_internals
        }
        allowed_regimes = {
            name: _STRATEGY_REGISTRY[name]["regimes"]
            for name in active_internals
        }

        router = MultiStrategyRouter(
            strategies=strategy_instances,
            weights=weights,
            allowed_regimes=allowed_regimes,
        )

        # ------------------------------------------------------------------
        # Build engine components
        # ------------------------------------------------------------------
        portfolio        = Portfolio(cash=capital)
        portfolio_engine = PortfolioEngine(portfolio)
        execution_agent  = ExecutionAgent(
            portfolio_engine,
            commission_pct=0.001,
            slippage_pct=0.0005,
        )
        max_downtrend_pct = float(risk_cfg.get("pause_threshold_pct", 35.0)) / 100.0

        risk_agent = RiskAgent(
            max_position_pct=max_pos_pct,
            atr_multiplier=2.0,
            risk_per_trade_pct=float(risk_cfg.get("risk_per_trade_pct", 0.5)) / 100.0,
            use_vol_sizing=True,
            breadth_circuit_breaker=True,
            max_downtrend_pct=max_downtrend_pct,
            min_atr_cost_ratio=3.0,
        )

        # LLM-driven weekly rebalance — mirrors run_experiments.py Step 15.
        # Only instantiated when OPENAI_API_KEY is present; otherwise the router
        # holds its initial weights for the full backtest duration.
        def _llm_decision_callback(decided_at, regime, confidence, weights,
                                   snapshot, raw_response, model):
            store.log_llm_decision(
                decided_at=decided_at.isoformat(),
                regime=regime,
                confidence=confidence,
                weights=weights,
                snapshot=snapshot,
                raw_llm_response=raw_response,
                model=model,
                call_seq=adaptive_selector.call_count if adaptive_selector else 0,
                run_id=run_id,
                source="backtest",
            )

        adaptive_selector = (
            AdaptiveStrategySelector(
                strategy_names=active_internals,
                rebalance_frequency_days=5,
                model="gpt-4o-mini",
                verbose=False,
                on_rebalance=_llm_decision_callback,
            )
            if os.environ.get("OPENAI_API_KEY")
            else None
        )

        engine = BacktestEngine(
            observer=observer,
            strategy_router=router,
            risk_agent=risk_agent,
            execution_agent=execution_agent,
            portfolio=portfolio,
            repository=None,
            dynamic_universe_agent=dynamic_agent,
            universe_agent=union_filter,
            adaptive_selector=adaptive_selector,
            regime_context_agent=rca,
        )

        store.update_run_progress(run_id, 40)

        # ------------------------------------------------------------------
        # Run adaptive backtest (LLM-driven weights)
        # ------------------------------------------------------------------
        results, trades = engine.run(universe_symbols, historical_dates)

        store.update_run_progress(run_id, 65)

        # ------------------------------------------------------------------
        # Baseline pass: same setup but fixed weights, no LLM rebalancing.
        # Reuses already-preloaded dynamic_agent + observer — no extra DB queries.
        # Only run when the adaptive selector was active (key present).
        # ------------------------------------------------------------------
        baseline_summary: dict | None = None
        if adaptive_selector is not None:
            baseline_router = MultiStrategyRouter(
                strategies={name: _STRATEGY_REGISTRY[name]["factory"]() for name in active_internals},
                weights=weights,
                allowed_regimes=allowed_regimes,
            )
            baseline_portfolio = Portfolio(cash=capital)
            baseline_engine = BacktestEngine(
                observer=observer,
                strategy_router=baseline_router,
                risk_agent=RiskAgent(
                    max_position_pct=max_pos_pct,
                    atr_multiplier=2.0,
                    risk_per_trade_pct=float(risk_cfg.get("risk_per_trade_pct", 0.5)) / 100.0,
                    use_vol_sizing=True,
                    breadth_circuit_breaker=True,
                    max_downtrend_pct=max_downtrend_pct,
                    min_atr_cost_ratio=3.0,
                ),
                execution_agent=ExecutionAgent(
                    PortfolioEngine(baseline_portfolio),
                    commission_pct=0.001,
                    slippage_pct=0.0005,
                ),
                portfolio=baseline_portfolio,
                repository=None,
                dynamic_universe_agent=dynamic_agent,
                universe_agent=union_filter,
                adaptive_selector=None,
                regime_context_agent=rca,
            )
            b_results, b_trades = baseline_engine.run(universe_symbols, historical_dates)
            evaluator_b    = EvaluationAgent()
            b_port_metrics = evaluator_b.evaluate(b_results, capital)
            b_trade_metrics = evaluator_b.evaluate_trades(b_trades)
            baseline_summary = {
                "return_pct":  round(b_port_metrics.get("total_return", 0) * 100, 2),
                "sharpe":      round(b_port_metrics.get("sharpe_ratio", 0), 2),
                "max_dd_pct":  round(-abs(b_port_metrics.get("max_drawdown", 0)) * 100, 2),
                "num_trades":  b_trade_metrics.get("num_trades", 0),
            }

        store.update_run_progress(run_id, 75)

        # ------------------------------------------------------------------
        # Compute adaptive metrics
        # ------------------------------------------------------------------
        evaluator         = EvaluationAgent()
        port_metrics      = evaluator.evaluate(results, capital)
        trade_metrics     = evaluator.evaluate_trades(trades)

        # Benchmark
        nifty_prices        = _fetch_nifty_prices(start_dt, today_dt)
        benchmark_return    = _benchmark_return(nifty_prices, "2019-01-01", today_dt.strftime("%Y-%m-%d"))
        benchmark_returns   = list(nifty_prices.values())
        benchmark_dd        = 0.0
        if len(benchmark_returns) > 1:
            benchmark_dd = -abs(evaluator.calculate_max_drawdown(benchmark_returns)) * 100

        total_return_pct = round(port_metrics.get("total_return", 0) * 100, 2)
        max_dd_pct       = round(-abs(port_metrics.get("max_drawdown", 0)) * 100, 2)

        summary = {
            "total_return_pct":    total_return_pct,
            "max_drawdown_pct":    max_dd_pct,
            "sharpe_ratio":        round(port_metrics.get("sharpe_ratio", 0), 2),
            "win_rate_pct":        round(trade_metrics.get("win_rate_trade", 0) * 100, 1),
            "total_trades":        trade_metrics.get("num_trades", 0),
            "benchmark_return_pct": benchmark_return,
            "benchmark_max_dd_pct": round(benchmark_dd, 2),
            "benchmark_sharpe":    0.0,
        }

        # Equity curve (monthly sampling for UI)
        equity_curve = _build_equity_curve(results, nifty_prices, capital)

        # Period breakdown
        period_breakdown = _period_breakdown(results, nifty_prices, capital)

        # Trade log (last 200 trades for performance)
        trade_log = _build_trade_log(trades[-200:] if len(trades) > 200 else trades)

        store.update_run_progress(run_id, 90)

        # ------------------------------------------------------------------
        # Save A/B comparison if adaptive run happened
        # ------------------------------------------------------------------
        if adaptive_selector is not None and baseline_summary is not None:
            store.save_ab_result(
                run_id=run_id,
                adaptive={
                    "return_pct": total_return_pct,
                    "sharpe":     summary["sharpe_ratio"],
                    "max_dd_pct": max_dd_pct,
                    "num_trades": summary["total_trades"],
                },
                baseline=baseline_summary,
                llm_call_count=adaptive_selector.call_count,
            )

        # AI narrative (non-blocking — generated after results are ready)
        ai_narrative = generate_narrative(summary, period_breakdown)

        # ------------------------------------------------------------------
        # Store complete result
        # ------------------------------------------------------------------
        ab_result = store.get_ab_result(run_id)

        result_payload = {
            "summary":          summary,
            "equity_curve":     equity_curve,
            "period_breakdown": period_breakdown,
            "trade_log":        trade_log,
            "ai_narrative":     ai_narrative,
            "config_snapshot":  config,
            "llm_comparison":   ab_result,   # None if no LLM key / baseline not run
        }

        complete_run_record = {
            "strategy_id":    config.get("strategy_id"),
            **result_payload,
        }

        store.complete_run(run_id, complete_run_record)

    except Exception as exc:
        store.fail_run(run_id, f"{type(exc).__name__}: {exc}\n{traceback.format_exc()}")


# ---------------------------------------------------------------------------
# Helpers for response shaping
# ---------------------------------------------------------------------------

def _build_equity_curve(
    results: list[BacktestResult],
    nifty_prices: dict,
    initial_capital: float,
) -> list[dict]:
    """Monthly-sampled equity curve with benchmark overlay."""
    if not results:
        return []

    # Sample roughly monthly (every ~21 trading days)
    step       = max(1, len(results) // 60)
    sampled    = results[::step]
    if results[-1] not in sampled:
        sampled = list(sampled) + [results[-1]]

    nifty_sorted = sorted(nifty_prices.items())
    nifty_lookup  = dict(nifty_sorted)

    # Find benchmark start price
    result_start = sampled[0].date.strftime("%Y-%m-%d")
    bm_dates     = sorted(k for k in nifty_lookup if k >= result_start)
    bm_start     = nifty_lookup[bm_dates[0]] if bm_dates else None

    curve = []
    for r in sampled:
        date_str = r.date.strftime("%Y-%m-%d")
        bm_price = nifty_lookup.get(date_str)

        if bm_start and bm_price:
            bm_value = round(initial_capital * (bm_price / bm_start), 2)
        else:
            # Fall back to the most recent known benchmark price before this date
            prior_dates = [d for d in nifty_lookup if d <= date_str]
            if prior_dates and bm_start:
                bm_value = round(initial_capital * (nifty_lookup[max(prior_dates)] / bm_start), 2)
            else:
                bm_value = initial_capital

        curve.append({
            "date":      date_str,
            "portfolio": round(r.equity, 2),
            "benchmark": bm_value,
        })

    return curve


def _build_trade_log(trades: list[Trade]) -> list[dict]:
    """Convert Trade objects to the API trade_log format."""
    log = []
    for t in trades:
        pnl_pct = (
            round((t.exit_price - t.entry_price) / t.entry_price * 100, 2)
            if t.entry_price else 0.0
        )
        log.append({
            "date":            t.exit_date.strftime("%Y-%m-%d"),
            "symbol":          t.symbol,
            "action":          "SELL",
            "strategy":        "multi-strategy",
            "entry_price":     round(t.entry_price, 2),
            "exit_price":      round(t.exit_price, 2),
            "pnl_pct":         pnl_pct,
            "regime_at_entry": "",
            "reason":          "",
        })
    return log
