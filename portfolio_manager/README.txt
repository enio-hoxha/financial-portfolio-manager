FINANCIAL PORTFOLIO MANAGER
Student: Enio Hoxha 26046
Course: Programming and Visualisation (M1)
Date: July 2026

[ DESCRIPTION ]
This project is an Object-Oriented Portfolio Management System designed to bridge 
theoretical quantitative finance with real world market data. 

Upgraded from a static baseline, this dynamic version is designed to:
1. Parse local ownership data dynamically from a CSV file.
2. Fetch live, real time market prices and 1-year historical data via Yahoo Finance.
3. Calculate risk metrics: Covariance Matrix, Annualized Volatility.
4. Execute algorithmic rebalancing based on target weights.
5. Generate a panel visual analytics dashboard.

[ FILES INCLUDED ]
1. main.py ............. The primary entry script (Run this to launch the app).
2. visualizer.py ....... Generates the Matplotlib/Seaborn analytics dashboard.
3. portfolio_io.py ..... Robust I/O module with auto-delimiter detection.
4. portfolio.py ........ Core engine for real-time risk analysis and rebalancing.
5. asset.py ............ Class defining financial instruments and histories.
6. position.py ......... Class managing ownership, quantity, Profit&Loss.
7. test_project.py ..... Unit tests to verify system integrity.
8. portfolio_data.csv .. State file containing current holdings and cost basis.
9. requirements.txt .... List of required Python dependencies.

[ HOW TO RUN ]
1. Ensure you have an active internet connection (required for the live API).
2. Install the necessary dependencies:
   pip install -r requirements.txt
   (Or manually: pip install numpy pandas yfinance matplotlib seaborn)

3. Run the analytics demo:
   python main.py

4. Run the unit test suite:
   python test_project.py

[ FEATURES HIGHLIGHTED ]
- Live API Integration: Utilizes `yfinance` to fetch real time pricing and history.
- Advanced Visualization: Implements a panel dashboard (Allocation Pie Chart, 
  Risk Correlation Heatmap, and Normalized 1 Year Profit&Loss Performance Curve).
- Quantitative Data Alignment: Solves the classic "Weekend Problem" by using 
  forward filling to perfectly align 24/7 Crypto markets with Monday-Friday Equity 
  markets before calculating the Covariance Matrix.
- Defensive I/O Architecture: `portfolio_io.py` automatically detects European (;) 
  vs Standard (,) CSV delimiters and handles UTF-8-BOM encoding to prevent crashes 
  across different operating systems and Excel versions.
- Unified Master Ledger: The terminal outputs a clean, formatted table tracking 
  Buy Price, Live Price, Allocation %, and dynamic Profit/Loss.

[ NOTES ]
- The system is completely data agnostic. To analyze a different portfolio, 
  simply edit `portfolio_data.csv`. The Python script will automatically adapt, 
  fetch the new tickers, and recalculate all risk metrics and visualizations 
  without changing a single line of code.