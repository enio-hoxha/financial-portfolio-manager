# test_project.py
import unittest
from asset import Asset
from position import Position
from portfolio import Portfolio


class TestPortfolioManager(unittest.TestCase):

    def setUp(self):
        """Set up fake assets and portfolios to test the math logic safely."""
        self.apple = Asset("Apple Inc", "AAPL", "Stock", current_price=200.00)
        self.tesla = Asset("Tesla", "TSLA", "Stock", current_price=250.00)
        self.test_fund = Portfolio("Test Fund")

    def test_position_market_value_calculation(self):
        """Test if a Position correctly multiplies quantity by current price."""
        # 10 shares of Apple at $200 each should equal $2000
        my_position = Position(self.apple, quantity=10, purchase_price=150.00)
        self.assertEqual(my_position.market_value, 2000.00)

    def test_position_profit_loss_percentage(self):
        """Test if a Position correctly calculates the P/L percentage."""
        # Bought at $150, now worth $200. That is a 33.33% increase.
        my_position = Position(self.apple, quantity=10, purchase_price=150.00)
        self.assertAlmostEqual(my_position.return_percentage, 33.33, places=2)

    def test_portfolio_total_value(self):
        """Test if the Portfolio correctly sums up multiple positions."""
        # Apple pos: 10 * $200 = $2000
        # Tesla pos: 5  * $250 = $1250
        # Total Portfolio Value should be $3250
        self.test_fund.add_position(
            Position(self.apple, quantity=10, purchase_price=150.00))
        self.test_fund.add_position(
            Position(self.tesla, quantity=5, purchase_price=200.00))

        self.assertEqual(self.test_fund.total_value, 3250.00)


if __name__ == '__main__':
    print("======================================================")
    print(" RUNNING SYSTEM UNIT TESTS")
    print("======================================================\n")
    unittest.main(verbosity=2)
