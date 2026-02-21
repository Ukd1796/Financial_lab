from datetime import datetime
import pandas as pd

from app.backtest.engine import BacktestEngine
from app.data.repository import MarketDataRepository
from app.agents.observer import MarketObserverAgent
from app.portfolio.models import Portfolio
from app.portfolio.engine import PortfolioEngine
from app.risk.agent import RiskAgent
from app.execution.agent import ExecutionAgent
from app.evaluation.agent import EvaluationAgent
from app.reflection.agent import ReflectionAgent
from app.analysis.regime_agent import RegimeAnalysisAgent
from app.strategy.cross_sectional import CrossSectionalMomentumStrategy


# ---------------------------------------
# Robustness Period
# ---------------------------------------
FULL_PERIOD = (datetime(2018, 1, 1), datetime(2024, 6, 1))

# ---------------------------------------
# Parameter Sweep (sanity check only)
# ---------------------------------------
PARAMETER_SWEEP = [
    {"lookback": 80,  "rebalance": 20, "threshold": 0.05},
    {"lookback": 100, "rebalance": 20, "threshold": 0.05},  # baseline
    {"lookback": 120, "rebalance": 20, "threshold": 0.05},

    {"lookback": 100, "rebalance": 15, "threshold": 0.05},
    {"lookback": 100, "rebalance": 25, "threshold": 0.05},

    {"lookback": 100, "rebalance": 20, "threshold": 0.03},
    {"lookback": 100, "rebalance": 20, "threshold": 0.07},
]

INITIAL_CAPITAL = 100000

SYMBOLS = [
    "RELIANCE", "TCS", "INFY", "HDFCBANK", "ICICIBANK", "ITC",
    "SBIN", "BHARTIARTL", "ASIANPAINT", "AXISBANK", "MARUTI",
    "HCLTECH", "WIPRO", "BAJFINANCE", "KOTAKBANK", "ULTRACEMCO",
    "TITAN", "SUNPHARMA", "NESTLEIND"
]


# ---------------------------------------
# Utility
# ---------------------------------------
def build_master_timeline(repository, start_date, end_date):
    records = []
    for symbol in SYMBOLS:
        recs = repository.get_ohlc(symbol, start_date, end_date)
        records.extend(recs)
    return sorted(list({r.timestamp for r in records}))


# ---------------------------------------
# Backtest Runner
# ---------------------------------------
def run_multi_asset_experiment(risk_params, repository, param_config):

    start_date, end_date = FULL_PERIOD

    observer = MarketObserverAgent(repository)

    portfolio = Portfolio(cash=INITIAL_CAPITAL)
    portfolio_engine = PortfolioEngine(portfolio)
    execution_agent = ExecutionAgent(portfolio_engine)

    risk_agent = RiskAgent(
        max_position_pct=risk_params["max_position_pct"],
        atr_multiplier=2.0
    )

    strategy = CrossSectionalMomentumStrategy(
        lookback_days=param_config["lookback"],
        top_n=3,
        rebalance_frequency=param_config["rebalance"],
        momentum_threshold=param_config["threshold"]
    )

    backtest = BacktestEngine(
        observer=observer,
        strategy_router=strategy,
        risk_agent=risk_agent,
        execution_agent=execution_agent,
        portfolio=portfolio,
        repository=repository
    )

    historical_dates = build_master_timeline(repository, start_date, end_date)

    if not historical_dates:
        return None

    results, trades = backtest.run(SYMBOLS, historical_dates)

    evaluator = EvaluationAgent()
    portfolio_metrics = evaluator.evaluate(results, INITIAL_CAPITAL)
    trade_metrics = evaluator.evaluate_trades(trades)

    return portfolio_metrics, trade_metrics


# ---------------------------------------
# Main Sweep
# ---------------------------------------
def main():

    repository = MarketDataRepository()

    print("\nRunning Parameter Robustness Sweep (Full Period)")
    print("=" * 80)

    for param_config in PARAMETER_SWEEP:

        print(
            f"\nLookback={param_config['lookback']} | "
            f"Rebalance={param_config['rebalance']} | "
            f"Threshold={param_config['threshold']*100:.0f}%"
        )

        result = run_multi_asset_experiment(
            risk_params={"max_position_pct": 0.2},
            repository=repository,
            param_config=param_config
        )

        if result:
            pm, tm = result

            print(
                f"Sharpe {pm['sharpe_ratio']:.2f} | "
                f"Return {pm['total_return']*100:.2f}% | "
                f"Drawdown {pm['max_drawdown']*100:.2f}% | "
                f"ProfitFactor {tm.get('profit_factor', 0):.2f}"
            )


if __name__ == "__main__":
    main()
