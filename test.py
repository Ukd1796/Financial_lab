from datetime import date
from app.data.providers.yfinance_provider import YFinanceProvider
from app.data.repository import MarketDataRepository
from app.agents.observer import MarketObserverAgent
from app.portfolio.engine import PortfolioEngine
from app.portfolio.models import Portfolio

provider = YFinanceProvider()
repository = MarketDataRepository()

observer = MarketObserverAgent(repository)

portfolio = Portfolio(cash=100000)
engine = PortfolioEngine(portfolio)

engine.buy("RELIANCE", 10, 2500)
engine.sell("RELIANCE", 5, 2600)

print("Cash:", portfolio.cash)
print("Positions:", portfolio.positions)
print("Realized PnL:", portfolio.realized_pnl)

