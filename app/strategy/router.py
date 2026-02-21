# app/strategy/router.py

from app.strategy.models import Decision


class RegimeConditionedStrategyRouter:

    def __init__(self, regime_strategy_map: dict):
        """
        regime_strategy_map:
            {
                "LOW_VOL_UPTREND": strategy_instance,
                "MID_VOL_UPTREND": strategy_instance,
                ...
            }
        """
        self.regime_strategy_map = regime_strategy_map

    def decide(self, market_state, portfolio):

        regime = market_state.indicators.get("regime")

        if regime not in self.regime_strategy_map:
            return Decision(
                symbol=market_state.symbol,
                action="HOLD",
                reasoning=f"No strategy mapped for regime {regime}"
            )

        selected_strategy = self.regime_strategy_map[regime]

        decision = selected_strategy.decide(
            market_state,
            portfolio
        )

        # Optional: annotate reasoning
        decision.reasoning = (
            f"[{regime}] " + (decision.reasoning or "")
        )

        return decision