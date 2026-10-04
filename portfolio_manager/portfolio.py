# portfolio.py
import numpy as np
import pandas as pd


class Portfolio:
    def __init__(self, owner):
        self.owner = owner
        self.positions = []

    def add_position(self, position):
        self.positions.append(position)

    @property
    def total_value(self):
        """Sum of the market value of all positions."""
        return sum(p.market_value for p in self.positions)

    @property
    def total_cost(self):
        """Sum of the cost basis of all positions."""
        return sum(p.cost_basis for p in self.positions)

    @property
    def total_return_percent(self):
        """Overall portfolio return percentage."""
        if self.total_cost == 0:
            return 0.0
        profit = self.total_value - self.total_cost
        return (profit / self.total_cost) * 100

    def get_risk_summary(self):
        """
        Calculates portfolio level risk metrics.
        Returns a dictionary of metrics.
        """
        if not self.positions:
            return {}

        # Check if assets actually have history loaded
        if any(p.asset.history is None for p in self.positions):
            print("Warning: Some assets lack historical data. Volatility may be 0.")

        total_val = self.total_value

        # 1. Calculate Weights
        weights = [p.market_value / total_val for p in self.positions]

        # 2. Calculate Portfolio Volatility (Covariance Matrix Method)
        try:
            # Create a DataFrame of all asset returns.
            # Using a dictionary comprehension automatically aligns dates if histories differ.
            all_returns = pd.DataFrame({
                p.asset.ticker: p.asset.history.pct_change().dropna()
                for p in self.positions
                if p.asset.history is not None
            }).fillna(0)

            if not all_returns.empty:
                # Calculate Covariance Matrix (Annualized by 252 trading days which is the average days of trading in a Year.)
                cov_matrix = all_returns.cov() * 252

                # Convert weights to NumPy array
                weights_array = np.array(weights)

                # Portfolio Variance formula: w^T * Cov * w
                port_variance = np.dot(
                    weights_array.T, np.dot(cov_matrix, weights_array))
                portfolio_vol = np.sqrt(port_variance)
            else:
                portfolio_vol = 0.0

        except Exception as e:
            print(f"Error calculating covariance: {e}. Defaulting to 0.")
            portfolio_vol = 0.0

        # 3. Concentration Risk (Herfindahl-Hirschman Index - HHI)
        hhi = np.sum(np.square(weights))

        return {
            "total_value": total_val,
            "weighted_volatility": portfolio_vol,
            "concentration_index": hhi,
            "diversification_status": "High" if hhi < 0.25 else "Low"
        }

    def rebalance(self, target_allocations):
        """
        Generates a trade plan to match target allocations.
        """
        # Check if targets sum to 1.0 (allow small float error)
        if not (0.99 <= sum(target_allocations.values()) <= 1.01):
            raise ValueError("Target allocations must sum to 1.0 (100%).")

        total_val = self.total_value
        trade_plan = []

        print(f"\nRebalancing Plan for ${total_val:,.2f} Portfolio")

        for position in self.positions:
            ticker = position.asset.ticker
            target_pct = target_allocations.get(ticker, 0.0)

            target_value = total_val * target_pct
            current_value = position.market_value
            difference = target_value - current_value

            price = position.asset.current_price
            qty_to_trade = difference / price

            if abs(difference) < 1.0:
                continue

            action = "BUY" if difference > 0 else "SELL"

            trade_plan.append({
                "ticker": ticker,
                "action": action,
                "quantity": abs(qty_to_trade),
                "value_change": difference
            })

        return trade_plan
