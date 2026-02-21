from datetime import date, datetime, timedelta

from app.data.providers.yfinance_provider import YFinanceProvider
from app.data.repository import MarketDataRepository
from app.agents.observer import MarketObserverAgent
from app.strategy.rule_based import MovingAverageStrategy
from app.portfolio.models import Portfolio
from app.portfolio.engine import PortfolioEngine


def main():

    symbol = "RELIANCE"

    # -----------------------------------
    # 1️⃣ Setup provider + repository
    # -----------------------------------
    provider = YFinanceProvider()
    repository = MarketDataRepository()

    print("Fetching historical data...")

    records = provider.fetch_ohlc(
        symbol=symbol,
        start=date(2023, 1, 1),
        end=date(2024, 6, 1)
    )

    repository.bulk_upsert(records)

    print(f"Stored {len(records)} records in DB")

    # -----------------------------------
    # 2️⃣ Observer Agent
    # -----------------------------------
    observer = MarketObserverAgent(repository)

    start_date = datetime(2023, 1, 1)
    end_date = datetime(2025, 6, 1)

    market_state = observer.run(symbol, start_date, end_date)

    print("\nMarket State:")
    print(market_state)

    # -----------------------------------
    # 3️⃣ Initialize Portfolio
    # -----------------------------------
    portfolio = Portfolio(cash=100000)
    portfolio_engine = PortfolioEngine(portfolio)

    # -----------------------------------
    # 4️⃣ Strategy Agent
    # -----------------------------------
    strategy = MovingAverageStrategy(position_size=10)

    decision = strategy.decide(market_state, portfolio)

    print("\nStrategy Decision:")
    print(decision)

    # -----------------------------------
    # 5️⃣ Execution
    # -----------------------------------
    if decision.action == "BUY":
        portfolio_engine.buy(
            decision.symbol,
            decision.quantity,
            market_state.latest_price
        )

    elif decision.action == "SELL":
        portfolio_engine.sell(
            decision.symbol,
            decision.quantity,
            market_state.latest_price
        )

    # -----------------------------------
    # 6️⃣ Portfolio State After Execution
    # -----------------------------------
    print("\nPortfolio After Execution:")
    print("Cash:", portfolio.cash)
    print("Positions:", portfolio.positions)
    print("Realized PnL:", portfolio.realized_pnl)

    current_prices = {symbol: market_state.latest_price}
    print("Total Equity:", portfolio.total_equity(current_prices))
    print("Unrealized PnL:", portfolio.unrealized_pnl(current_prices))


if __name__ == "__main__":
    main()
