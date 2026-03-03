from datetime import datetime

from app.backtest.engine import BacktestEngine
from app.backtest.observer import MarketObserverAgent
from app.data.repository import MarketDataRepository
from app.evaluation.agent import EvaluationAgent
from app.execution.agent import ExecutionAgent
from app.portfolio.engine import PortfolioEngine
from app.portfolio.models import Portfolio
from app.risk.agent import RiskAgent
from app.strategy.cross_sectional import CrossSectionalMomentumStrategy
from app.strategy.dual_ma import DualMovingAverageStrategy

# -----------------------------------------------------------------------
# Configuration
# -----------------------------------------------------------------------
INITIAL_CAPITAL = 100_000

SYMBOLS = [
    "RELIANCE", "TCS", "INFY", "HDFCBANK", "ICICIBANK", "ITC",
    "SBIN", "BHARTIARTL", "ASIANPAINT", "AXISBANK", "MARUTI",
    "HCLTECH", "WIPRO", "BAJFINANCE", "KOTAKBANK", "ULTRACEMCO",
    "TITAN", "SUNPHARMA", "NESTLEIND",
]

# Named time periods to test
PERIODS = {
    "Full  2018–2024": (datetime(2018, 1, 1), datetime(2024, 6, 1)),
    "Bull  2019–2020": (datetime(2019, 1, 1), datetime(2020, 2, 1)),
    "Crash 2020     ": (datetime(2020, 1, 1), datetime(2020, 12, 31)),
    "Recov 2020–2021": (datetime(2020, 4, 1), datetime(2021, 12, 31)),
    "Bear  2022     ": (datetime(2022, 1, 1), datetime(2022, 12, 31)),
    "Recent2022–2024": (datetime(2022, 1, 1), datetime(2024, 6, 1)),
}

# CrossSectional parameter configs
CROSS_CONFIGS = [
    {"label": "CS  L=100 R=20 T=5%", "lookback": 100, "rebalance": 25, "threshold": 0.05},
    {"label": "CS  L=80  R=20 T=5%", "lookback": 80,  "rebalance": 25, "threshold": 0.05},
    {"label": "CS  L=100 R=20 T=3%", "lookback": 100, "rebalance": 25, "threshold": 0.03},
]


# -----------------------------------------------------------------------
# Utility
# -----------------------------------------------------------------------
def build_master_timeline(repository, start_date, end_date):
    records = []
    for symbol in SYMBOLS:
        records.extend(repository.get_ohlc(symbol, start_date, end_date))
    return sorted({r.timestamp for r in records})


# -----------------------------------------------------------------------
# Single backtest run
# -----------------------------------------------------------------------
def run_experiment(repository, strategy, start_date, end_date, max_position_pct=0.2):

    portfolio        = Portfolio(cash=INITIAL_CAPITAL)
    portfolio_engine = PortfolioEngine(portfolio)

    observer        = MarketObserverAgent(repository)
    execution_agent = ExecutionAgent(portfolio_engine)
    risk_agent      = RiskAgent(max_position_pct=max_position_pct, atr_multiplier=2.0)

    engine = BacktestEngine(
        observer=observer,
        strategy_router=strategy,
        risk_agent=risk_agent,
        execution_agent=execution_agent,
        portfolio=portfolio,
        repository=repository,
    )

    historical_dates = build_master_timeline(repository, start_date, end_date)
    if not historical_dates:
        return None

    results, trades = engine.run(SYMBOLS, historical_dates)

    evaluator         = EvaluationAgent()
    portfolio_metrics = evaluator.evaluate(results, INITIAL_CAPITAL)
    trade_metrics     = evaluator.evaluate_trades(trades)

    return {"portfolio_metrics": portfolio_metrics, "trade_metrics": trade_metrics}


# -----------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------
def main():
    repository = MarketDataRepository()

    col_w = 22  # strategy label column width

    for period_label, (start_date, end_date) in PERIODS.items():

        print(f"\n{'=' * 72}")
        print(f"  Period: {period_label}  ({start_date.date()} → {end_date.date()})")
        print(f"{'=' * 72}")
        print(f"  {'Strategy':<{col_w}} {'Sharpe':>6} {'Return':>9} {'MaxDD':>8} {'PF':>7} {'#Trades':>8}")
        print(f"  {'-' * (col_w + 42)}")

        # --- CrossSectional configs ---
        for cfg in CROSS_CONFIGS:
            strategy = CrossSectionalMomentumStrategy(
                lookback_days=cfg["lookback"],
                top_n=3,
                rebalance_frequency=cfg["rebalance"],
                momentum_threshold=cfg["threshold"],
            )
            result = run_experiment(repository, strategy, start_date, end_date)

            if result is None:
                print(f"  {cfg['label']:<{col_w}}  (no data)")
                continue

            pm = result["portfolio_metrics"]
            tm = result["trade_metrics"]
            n  = tm.get("total_trades", 0)

            print(
                f"  {cfg['label']:<{col_w}} "
                f"{pm['sharpe_ratio']:>6.2f} "
                f"{pm['total_return']*100:>8.2f}% "
                f"{pm['max_drawdown']*100:>7.2f}% "
                f"{tm.get('profit_factor', 0):>7.2f} "
                f"{n:>8}"
            )

        # --- Dual Moving Average ---
        strategy = DualMovingAverageStrategy()
        result   = run_experiment(repository, strategy, start_date, end_date)
        label    = "DualMA SMA20/50"

        if result is None:
            print(f"  {label:<{col_w}}  (no data)")
        else:
            pm = result["portfolio_metrics"]
            tm = result["trade_metrics"]
            n  = tm.get("total_trades", 0)

            print(
                f"  {label:<{col_w}} "
                f"{pm['sharpe_ratio']:>6.2f} "
                f"{pm['total_return']*100:>8.2f}% "
                f"{pm['max_drawdown']*100:>7.2f}% "
                f"{tm.get('profit_factor', 0):>7.2f} "
                f"{n:>8}"
            )

    print(f"\n{'=' * 72}\n")


if __name__ == "__main__":
    main()
