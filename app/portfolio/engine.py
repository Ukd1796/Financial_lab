from app.portfolio.models import Portfolio, Position


class PortfolioEngine:

    def __init__(self, portfolio: Portfolio):
        self.portfolio = portfolio

    def buy(self, symbol: str, quantity: float, price: float):

        cost = quantity * price

        if cost > self.portfolio.cash:
            raise ValueError("Insufficient cash")

        # Deduct cash
        self.portfolio.cash -= cost

        # Update or create position
        if symbol in self.portfolio.positions:
            existing = self.portfolio.positions[symbol]
            total_quantity = existing.quantity + quantity
            new_avg_price = (
                (existing.quantity * existing.average_price + cost)
                / total_quantity
            )
            existing.quantity = total_quantity
            existing.average_price = new_avg_price
        else:
            self.portfolio.positions[symbol] = Position(
                symbol=symbol,
                quantity=quantity,
                average_price=price
            )

    def sell(self, symbol: str, quantity: float, price: float):

        if symbol not in self.portfolio.positions:
            raise ValueError("No position to sell")

        position = self.portfolio.positions[symbol]

        if quantity > position.quantity:
            raise ValueError("Cannot sell more than owned")

        proceeds = quantity * price
        pnl = (price - position.average_price) * quantity

        # Update cash
        self.portfolio.cash += proceeds

        # Update realized PnL
        self.portfolio.realized_pnl += pnl

        # Update position
        position.quantity -= quantity

        if position.quantity == 0:
            del self.portfolio.positions[symbol]
