# asset.py
import numpy as np
import pandas as pd


class Asset:
    """
    Represents a financial instrument (e.g., Stock, Bond) with analytics capabilities.
    Stores both static data (ticker, price) and dynamic historical data.
    """

    # Allowed asset types for validation
    # Upper case because cannot be changed
    VALID_TYPES = ["Stock", "Bond", "ETF", "Crypto", "Cash"]

    def __init__(self, name, ticker, asset_type, current_price):
        """
        Initialize an Asset.

        Args:
            name (str): Full name (e.g., "Apple Inc.")
            ticker (str): Symbol (e.g., "AAPL")
            asset_type (str): Must be in Asset.VALID_TYPES
            current_price (float): Current market price per unit
        """
        if current_price < 0:
            raise ValueError("Price cannot be negative.")
        if asset_type not in self.VALID_TYPES:
            raise ValueError(f"Invalid asset type: {asset_type}")

        self.name = name
        self.ticker = ticker.upper()
        self.asset_type = asset_type
        self.current_price = current_price

        # Placeholders for analytic data
        self.history = None

    def set_history(self, prices):
        """
        Assigns historical price data to the asset for risk calculations.

        Args:
            prices: A list, numpy array, or pandas Series of daily closing prices.
        """
        if isinstance(prices, list):
            self.history = pd.Series(prices)
        elif isinstance(prices, (np.ndarray, pd.Series)):
            self.history = pd.Series(prices)
        else:
            raise TypeError(
                "History must be a list, numpy array, or pandas Series.")

    @property
    def volatility(self):
        """
        Calculates annualized volatility based on historical returns.

        Returns:
            float: The annualized standard deviation (e.g., 0.15 for 15%).
                   Returns 0.0 if no history is present.
        """
        if self.history is None or len(self.history) < 2:
            return 0.0

        # Calculate daily percentage returns
        returns = self.history.pct_change().dropna()

        # Standard deviation of daily returns
        daily_std = returns.std()

        # Annualize (multiply by square root of 252 trading days)
        annualized_vol = daily_std * np.sqrt(252)

        return annualized_vol

    def __str__(self):
        """String representation for printing."""
        return f"{self.ticker} ({self.asset_type}): ${self.current_price:,.2f}"
