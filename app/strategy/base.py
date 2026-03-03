from abc import ABC, abstractmethod
from app.strategy.models import Decision
from app.data.models import MarketState
from app.portfolio.models import Portfolio


class BaseStrategyAgent(ABC):

    @abstractmethod
    def decide(
        self,
        market_state: MarketState,
        portfolio: Portfolio
    ) -> Decision:
        pass
