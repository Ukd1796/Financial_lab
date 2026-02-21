from datetime import datetime

from app.backtest.engine import BacktestEngine
from app.data.repository import MarketDataRepository
from app.agents.observer import MarketObserverAgent
from app.strategy.rule_based import MovingAverageStrategy
from app.portfolio.models import Portfolio
from app.portfolio.engine import PortfolioEngine
from app.risk.agent import RiskAgent


INITIAL_CAPITAL = 100000


def main():

    symbol = "RELIANCE"

    print(f"\nRunning backtest for {symbol}")
    print("-" * 50)

    # ---------------------------------------
    # Setup core components
    # ---------------------------------------
    repository = MarketDataRepository()
    observer = MarketObserverAgent(repository)

    portfolio = Portfolio(cash=INITIAL_CAPITAL)
    execution_engine = PortfolioEngine(portfolio)

    strategy = MovingAverageStrategy()
    risk_agent = RiskAgent(
        max_position_pct=0.2,  # 20% max allocation
        stop_loss_pct=0.05     # 5% stop loss (if implemented)
    )

    backtest = BacktestEngine(
        observer=observer,
        strategy=strategy,
        risk_agent=risk_agent,
        execution_engine=execution_engine,
        portfolio=portfolio
    )

    # ---------------------------------------
    # Fetch historical dates
    # ---------------------------------------
    records = repository.get_ohlc(
        symbol,
        datetime(2023, 1, 1),
        datetime(2024, 6, 1)
    )

    if not records:
        print("No historical data found in DB.")
        return

    # Deduplicate & sort timestamps
    historical_dates = sorted(list({r.timestamp for r in records}))

    print(f"Total trading days: {len(historical_dates)}")

    # ---------------------------------------
    # Run backtest
    # ---------------------------------------
    results = backtest.run(symbol, historical_dates)

    if not results:
        print("Backtest returned no results.")
        return

    final_equity = results[-1].equity
    total_return = (final_equity - INITIAL_CAPITAL) / INITIAL_CAPITAL

    print("\nBacktest Completed")
    print("-" * 50)
    print(f"Initial Capital: ₹{INITIAL_CAPITAL:,.2f}")
    print(f"Final Equity:    ₹{final_equity:,.2f}")
    print(f"Total Return:    {total_return * 100:.2f}%")
    print(f"Realized PnL:    ₹{portfolio.realized_pnl:,.2f}")

    # Portfolio summary
    print("\nFinal Portfolio State:")
    print(f"Cash: ₹{portfolio.cash:,.2f}")
    print(f"Open Positions: {portfolio.positions}")

    # Optional: print last 5 equity values
    print("\nLast 5 Equity Snapshots:")
    for r in results[-5:]:
        print(f"{r.date.date()} → ₹{r.equity:,.2f}")


if __name__ == "__main__":
    main()
