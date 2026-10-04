# position.py
from asset import Asset


class Position:
    """
    Represents a specific holding of an asset within a portfolio.
    """

    def __init__(self, asset, quantity, purchase_price):
        """
        Args:
            asset: The Asset object associated with this position.
            quantity: Amount owned.
            purchase_price: Price per unit at the time of purchase.
        """
        if quantity <= 0:
            raise ValueError("Quantity must be positive.")
        if purchase_price < 0:
            raise ValueError("Purchase price cannot be negative.")

        # Ensure we are actually storing an Asset object
        if not isinstance(asset, Asset):
            raise TypeError(
                "The asset argument must be an instance of the Asset class.")

        self.asset = asset
        self.quantity = quantity
        self.purchase_price = purchase_price

    @property
    def cost_basis(self):
        """Calculate total cost to acquire this position."""
        return self.quantity * self.purchase_price

    @property
    def market_value(self):
        """Calculate current market value based on asset's current price."""
        return self.quantity * self.asset.current_price

    @property
    def unrealized_gain_loss(self):
        """Calculate absolute profit or loss ($)."""
        return self.market_value - self.cost_basis

    @property
    def return_percentage(self):
        """Calculate percentage return."""
        if self.cost_basis == 0:
            return 0.0
        return (self.unrealized_gain_loss / self.cost_basis) * 100

    def __str__(self):
        return (f"{self.asset.ticker:<6} | Qty: {self.quantity:>5} | "
                f"Mkt Val: ${self.market_value:>10,.2f} | "
                f"P/L: {self.return_percentage:>6.2f}%")
