# portfolio_io.py
import csv
import os
from portfolio import Portfolio
from position import Position
from asset import Asset


class PortfolioIO:
    """
    Handles Input/Output operations for the Portfolio.
    Decouples business logic from storage logic.
    """

    @staticmethod
    def load_from_csv(filename):
        """
        Loads a portfolio from a CSV file.
        Dynamically detects European (;) vs Standard (,) formatting.
        """
        if not os.path.exists(filename):
            raise FileNotFoundError(f"File {filename} does not exist.")

        try:
            # utf-8-sig strictly removes any hidden characters from the start of the file
            with open(filename, mode='r', encoding='utf-8-sig') as file:

                # AUTO-DETECT DELIMITER
                first_line = file.readline()
                # Reset file pointer back to the beginning after peeking
                file.seek(0)

                detected_delimiter = ';' if ';' in first_line else ','

                reader = csv.DictReader(file, delimiter=detected_delimiter)

                portfolio = None

                for row in reader:
                    # Strip spaces from keys in case the CSV has weird spacing like " Owner"
                    row = {k.strip(): v.strip() for k, v in row.items()}

                    if portfolio is None:
                        portfolio = Portfolio(owner=row["Owner"])

                    # Create Asset
                    asset = Asset(
                        name=row["Name"],
                        ticker=row["Ticker"],
                        asset_type=row["Type"],
                        current_price=float(row["CurrentPrice"])
                    )

                    # Create Position
                    position = Position(
                        asset=asset,
                        quantity=float(row["Quantity"]),
                        purchase_price=float(row["PurchasePrice"])
                    )

                    portfolio.add_position(position)

                if portfolio:
                    print(
                        f"Loaded Portfolio for {portfolio.owner} (Detected delimiter: '{detected_delimiter}')")
                    return portfolio

                return Portfolio("New User")

        except (IOError, ValueError, KeyError) as e:
            print(f"Error loading portfolio: {e}")
            return Portfolio("Error User")
