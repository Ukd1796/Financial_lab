"""
run_backtest.py — Quick CLI backtest for a single strategy over a custom date range.

Mirrors the architecture used by the API backtest service and run_experiments.py:
  - MultiStrategyRouter + UnionUniverseFilter
  - DynamicUniverseAgent (broad 150-symbol universe)
  - RegimeContextAgent for breadth-aware risk gating
  - Same RiskAgent params as production (max_downtrend_pct=0.35, min_atr_cost_ratio=3.0)

Usage:
    python run_backtest.py
"""

import os
from datetime import datetime, timedelta

from app.backtest.engine import BacktestEngine
from app.backtest.observer import MarketObserverAgent
from app.data.repository import MarketDataRepository
from app.evaluation.agent import EvaluationAgent
from app.execution.agent import ExecutionAgent
from app.meta.adaptive_selector import AdaptiveStrategySelector
from app.meta.regime_context_agent import RegimeContextAgent
from app.portfolio.engine import PortfolioEngine
from app.portfolio.models import Portfolio
from app.risk.agent import RiskAgent
from app.strategy.dual_ma import DualMovingAverageStrategy
from app.strategy.multi_router import MultiStrategyRouter
from app.universe.dynamic_agent import DynamicUniverseAgent
from app.universe.filters import DualMAUniverseFilter

from run_experiments import NIFTY_50, NIFTY_NEXT_50, NIFTY_MIDCAP_50

BROAD_UNIVERSE  = NIFTY_50 + NIFTY_NEXT_50 + NIFTY_MIDCAP_50
INITIAL_CAPITAL = 100_000

START_DATE = datetime(2022, 1, 1)
END_DATE   = datetime(2024, 6, 1)


def main():
    print(f"\nRunning backtest: {START_DATE.date()} → {END_DATE.date()}")
    print("-" * 60)

    buffer_dt  = START_DATE - timedelta(days=220)
    repository = MarketDataRepository()

    # Stage 1 universe: dynamic scoring over the broad 150-symbol universe
    dynamic_agent = DynamicUniverseAgent(
        repository=repository,
        symbols=BROAD_UNIVERSE,
        top_n=80,
    )
    dynamic_agent.preload(buffer_dt, END_DATE)

    # Stage 2 universe: per-strategy filter
    universe_filter = DualMAUniverseFilter(max_cross_age=5, top_n=30)

    # Regime context for breadth-aware signals
    rca     = RegimeContextAgent(dynamic_agent)
    observer = MarketObserverAgent(repository)

    # Strategy router (single strategy for this quick script)
    _UPTREND_ONLY = ["LOW_VOL_UPTREND", "MID_VOL_UPTREND", "HIGH_VOL_UPTREND"]
    router = MultiStrategyRouter(
        strategies={"DualMA": DualMovingAverageStrategy()},
        weights={"DualMA": 1.0},
        allowed_regimes={"DualMA": _UPTREND_ONLY},
    )

    # Optional LLM-driven rebalance (no-op if OPENAI_API_KEY not set)
    adaptive_selector = (
        AdaptiveStrategySelector(
            strategy_names=["DualMA"],
            rebalance_frequency_days=5,
            model="gpt-4o-mini",
            verbose=True,
        )
        if os.environ.get("OPENAI_API_KEY")
        else None
    )

    portfolio        = Portfolio(cash=INITIAL_CAPITAL)
    portfolio_engine = PortfolioEngine(portfolio)
    execution_agent  = ExecutionAgent(
        portfolio_engine,
        commission_pct=0.001,
        slippage_pct=0.0005,
    )
    risk_agent = RiskAgent(
        max_position_pct=0.15,
        atr_multiplier=2.0,
        allowed_regimes=None,       # router handles per-strategy gating
        risk_per_trade_pct=0.005,
        use_vol_sizing=True,
        breadth_circuit_breaker=True,
        max_downtrend_pct=0.35,
        min_atr_cost_ratio=3.0,
    )

    engine = BacktestEngine(
        observer=observer,
        strategy_router=router,
        risk_agent=risk_agent,
        execution_agent=execution_agent,
        portfolio=portfolio,
        repository=None,
        dynamic_universe_agent=dynamic_agent,
        universe_agent=universe_filter,
        adaptive_selector=adaptive_selector,
        regime_context_agent=rca,
    )

    # Build timeline from dynamic agent cache (same approach as backtest_service.py)
    timestamps = set()
    for df in dynamic_agent._cache.values():
        for ts in df.index:
            if START_DATE <= ts <= END_DATE:
                timestamps.add(ts)
    historical_dates = sorted(timestamps)

    if not historical_dates:
        print("No trading dates found in DB for this period.")
        return

    print(f"Trading days: {len(historical_dates)}")

    results, trades = engine.run(BROAD_UNIVERSE, historical_dates)

    if not results:
        print("Backtest returned no results.")
        return

    evaluator    = EvaluationAgent()
    port_metrics = evaluator.evaluate(results, INITIAL_CAPITAL)
    trade_metrics = evaluator.evaluate_trades(trades)

    final_equity = results[-1].equity
    total_return = (final_equity - INITIAL_CAPITAL) / INITIAL_CAPITAL

    print("\nBacktest Completed")
    print("-" * 60)
    print(f"Initial Capital : ₹{INITIAL_CAPITAL:>12,.2f}")
    print(f"Final Equity    : ₹{final_equity:>12,.2f}")
    print(f"Total Return    : {total_return * 100:>8.2f}%")
    print(f"Sharpe Ratio    : {port_metrics.get('sharpe_ratio', 0):>8.2f}")
    print(f"Max Drawdown    : {port_metrics.get('max_drawdown', 0) * 100:>7.2f}%")
    print(f"Win Rate        : {trade_metrics.get('win_rate_trade', 0) * 100:>7.1f}%")
    print(f"Total Trades    : {trade_metrics.get('num_trades', 0):>8}")

    print("\nLast 5 equity snapshots:")
    for r in results[-5:]:
        print(f"  {r.date.date()} → ₹{r.equity:,.2f}")


if __name__ == "__main__":
    main()
