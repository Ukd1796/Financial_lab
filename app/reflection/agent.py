# app/reflection/agent.py

class ReflectionAgent:

    def analyze(self, portfolio_metrics, trade_metrics):

        recommendations = []

        if not portfolio_metrics:
            return ["No portfolio metrics available."]

        # -----------------------------
        # Portfolio-Level Analysis
        # -----------------------------
        total_return = portfolio_metrics.get("total_return", 0)
        max_drawdown = portfolio_metrics.get("max_drawdown", 0)
        sharpe = portfolio_metrics.get("sharpe_ratio", 0)
        volatility = portfolio_metrics.get("volatility", 0)

        if total_return < 0:
            recommendations.append(
                "Negative total return. Strategy lacks edge."
            )

        if sharpe < 0.5:
            recommendations.append(
                "Low Sharpe ratio. Poor risk-adjusted performance."
            )

        if max_drawdown > 0.15:
            recommendations.append(
                "High drawdown detected. Consider lowering position sizing or adding stop-loss."
            )

        if volatility > 0.02:
            recommendations.append(
                "High daily volatility. Risk management may need tightening."
            )

        # -----------------------------
        # Trade-Level Analysis
        # -----------------------------
        if trade_metrics:

            profit_factor = trade_metrics.get("profit_factor", 0)
            expectancy = trade_metrics.get("expectancy", 0)
            win_rate = trade_metrics.get("win_rate_trade", 0)
            avg_win = trade_metrics.get("avg_win", 0)
            avg_loss = trade_metrics.get("avg_loss", 0)
            max_consec_losses = trade_metrics.get("max_consecutive_losses", 0)

            if profit_factor < 1:
                recommendations.append(
                    "Profit factor below 1. Losses outweigh gains."
                )

            if expectancy < 0:
                recommendations.append(
                    "Negative expectancy per trade. Signal logic likely flawed."
                )

            if abs(avg_loss) > abs(avg_win):
                recommendations.append(
                    "Average loss larger than average win. Poor risk-reward ratio."
                )

            if win_rate < 0.3:
                recommendations.append(
                    "Low win rate. Consider adding trend filter or higher timeframe confirmation."
                )

            if max_consec_losses > 5:
                recommendations.append(
                    "High consecutive loss streaks. Strategy may be unstable."
                )

        if not recommendations:
            recommendations.append("No major structural issues detected.")

        return recommendations
