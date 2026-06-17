from app.strategy.models import Decision


class DualMovingAverageStrategy:

    def decide(self, current_date, symbol_states: dict, portfolio) -> list[Decision]:
        decisions = []
        for symbol, market_state in symbol_states.items():
            fast_today     = market_state.indicators.get("sma_20")
            slow_today     = market_state.indicators.get("sma_50")
            fast_yesterday = market_state.previous_indicators.get("sma_20")
            slow_yesterday = market_state.previous_indicators.get("sma_50")

            if None in [fast_today, slow_today, fast_yesterday, slow_yesterday]:
                continue

            if (
                fast_yesterday <= slow_yesterday
                and fast_today > slow_today
                and symbol not in portfolio.positions
            ):
                decisions.append(Decision(
                    symbol=symbol,
                    action="BUY",
                    quantity=None,
                    reasoning="Bullish dual MA crossover",
                ))
            elif (
                fast_yesterday >= slow_yesterday
                and fast_today < slow_today
                and symbol in portfolio.positions
            ):
                decisions.append(Decision(
                    symbol=symbol,
                    action="SELL",
                    quantity=None,
                    reasoning="Bearish dual MA crossover",
                ))

        return decisions
