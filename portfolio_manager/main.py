# main.py
import os
import yfinance as yf
from portfolio_io import PortfolioIO
from visualizer import PortfolioVisualizer


def fetch_real_history(ticker_symbol, period="1y"):
    """
    Downloads real historical daily closing prices from Yahoo Finance.
    """
    print(f"[API] Downloading data for {ticker_symbol}")
    try:
        # Fetch data using yfinance
        ticker_data = yf.Ticker(ticker_symbol)
        hist = ticker_data.history(period=period)

        if hist.empty:
            print(f"[!] Warning: No data found for {ticker_symbol}.")
            return None

        # Return just the 'Close' prices as a Pandas Series
        return hist['Close']
    except Exception as e:
        print(f"[!] Failed to fetch {ticker_symbol}: {e}")
        return None


def run_portfolio_manager():
    print("======================================================")
    print("PORTFOLIO MANAGER")
    print("======================================================\n")

    filename = "portfolio_data.csv"
    if not os.path.exists(filename):
        print(f"Error: Could not find {filename}. Please create it first.")
        return

    # 1. LOAD OWNERSHIP DATA (The CSV File)
    print(f"1: Loading ownership data from '{filename}'")
    my_fund = PortfolioIO.load_from_csv(filename)

    # 2. INJECT LIVE MARKET DATA (yfinance API)
    print("\n2: Connecting to Yahoo Finance API to update prices")

    for position in my_fund.positions:
        ticker = position.asset.ticker
        history = fetch_real_history(ticker)

        if history is not None:
            # Overwrite the stale CSV price with the LIVE price
            live_price = float(history.iloc[-1])
            position.asset.current_price = live_price

            # Inject the 1-year history so the Risk Math works
            position.asset.set_history(history)

    print(f"\n Live Total Value: ${my_fund.total_value:,.2f}")

    # 3. PERFORMANCE & RISK ANALYSIS
    print("\n [3] RISK ANALYSIS")
    print("-" * 40)
    risk_report = my_fund.get_risk_summary()

    print(f"Total Cost Basis:     ${my_fund.total_cost:,.2f}")
    print(f"Current Market Value: ${my_fund.total_value:,.2f}")
    print(f"Total Return:         {my_fund.total_return_percent:.2f}%\n")
    print(
        f"Portfolio Volatility: {risk_report['weighted_volatility']:.2%} (Annualized)")
    print(f"Concentration (HHI):  {risk_report['concentration_index']:.2f}")

    # UNIFIED PORTFOLIO OVERVIEW TABLE
    print("\n[CURRENT PORTFOLIO OVERVIEW]")
    print("-" * 85)
    print(f"{'ASSET':<9} {'BUY PRICE ($)':>13} {'LIVE PRICE ($)':>14} {'QTY':>8} {'VALUE ($)':>14} {'P/L (%)':>9} {'ALLOC %':>9}")
    print("-" * 85)

    total_val = my_fund.total_value
    for p in my_fund.positions:
        # Calculate allocation percentage for display
        alloc_pct = (p.market_value / total_val) * 100

        print(f"{p.asset.ticker:<9} {p.purchase_price:>13,.2f} {p.asset.current_price:>14,.2f} {p.quantity:>8.2f} "
              f"{p.market_value:>14,.2f} {p.return_percentage:>8.2f}% {alloc_pct:>8.1f}%")
    print("-" * 85)

    # 4. REBALANCING
    print("\n[4] EXECUTING ALGORITHMIC REBALANCING")
    print("    Goal: Balanced Portfolio (20% each)")
    print("-" * 45)

    target_weights = {
        "AAPL": 0.20, "TSLA": 0.20, "BTC-USD": 0.20, "GLD": 0.20, "IEF": 0.20
    }

    trades = my_fund.rebalance(target_weights)

    print(f" {'ACTION':<6} {'TICKER':<10} {'QTY':>10} {'VALUE ($)':>14}")
    print("-" * 45)
    for t in trades:
        print(
            f" {t['action']:<6} {t['ticker']:<10} {t['quantity']:>10.2f} {t['value_change']:>14,.2f}")

    print("\nDEMO COMPLETE.")

    # 5. VISUALIZATION
    PortfolioVisualizer.show_dashboard(my_fund, target_weights)


if __name__ == "__main__":
    run_portfolio_manager()
