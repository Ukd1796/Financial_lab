# app/evaluation/agent.py

import numpy as np


class EvaluationAgent:

    # ==================================================
    # Portfolio-Level Metrics
    # ==================================================
    def evaluate(self, backtest_results, initial_capital):

        if not backtest_results:
            return {}

        equity_values = [r.equity for r in backtest_results]

        total_return = (equity_values[-1] - initial_capital) / initial_capital

        daily_returns = np.diff(equity_values) / equity_values[:-1] \
            if len(equity_values) > 1 else []

        max_drawdown = self.calculate_max_drawdown(equity_values)

        avg_daily_return = np.mean(daily_returns) if len(daily_returns) > 0 else 0
        volatility = np.std(daily_returns) if len(daily_returns) > 0 else 0

        sharpe = (
            (avg_daily_return / volatility) * np.sqrt(252)
            if volatility > 0 else 0
        )

        return {
            "total_return": total_return,
            "max_drawdown": max_drawdown,
            "avg_daily_return": avg_daily_return,
            "volatility": volatility,
            "sharpe_ratio": sharpe
        }

    def calculate_max_drawdown(self, equity_curve):
        peak = equity_curve[0]
        max_dd = 0

        for value in equity_curve:
            if value > peak:
                peak = value
            drawdown = (peak - value) / peak
            max_dd = max(max_dd, drawdown)

        return max_dd


    # ==================================================
    # Trade-Level Metrics
    # ==================================================
    def evaluate_trades(self, trades):

        if not trades:
            return {}

        pnls = [t.pnl for t in trades]

        wins = [p for p in pnls if p > 0]
        losses = [p for p in pnls if p < 0]

        num_trades = len(pnls)
        win_rate = len(wins) / num_trades if num_trades > 0 else 0

        avg_win = np.mean(wins) if wins else 0
        avg_loss = np.mean(losses) if losses else 0

        gross_profit = sum(wins)
        gross_loss = abs(sum(losses))

        profit_factor = (
            gross_profit / gross_loss
            if gross_loss > 0 else float("inf")
        )

        expectancy = (
            win_rate * avg_win +
            (1 - win_rate) * avg_loss
        )

        max_consecutive_losses = self.calculate_max_consecutive_losses(pnls)

        avg_holding_period = self.calculate_avg_holding_period(trades)

        return {
            "num_trades": num_trades,
            "win_rate_trade": win_rate,
            "avg_win": avg_win,
            "avg_loss": avg_loss,
            "profit_factor": profit_factor,
            "expectancy": expectancy,
            "max_consecutive_losses": max_consecutive_losses,
            "avg_holding_period_days": avg_holding_period
        }

    def calculate_max_consecutive_losses(self, pnls):
        max_streak = 0
        current_streak = 0

        for p in pnls:
            if p < 0:
                current_streak += 1
                max_streak = max(max_streak, current_streak)
            else:
                current_streak = 0

        return max_streak

    def calculate_avg_holding_period(self, trades):
        if not trades:
            return 0

        holding_periods = [
            (t.exit_date - t.entry_date).days
            for t in trades
        ]

        return np.mean(holding_periods) if holding_periods else 0

