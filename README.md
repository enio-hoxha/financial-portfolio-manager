# Financial Portfolio Management System

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)]()
[![Build](https://img.shields.io/badge/Tests-Passing-brightgreen.svg)]()

An Object-Oriented Portfolio Management System developed in Python, bridging theoretical quantitative finance and risk analytics with live market data feeds.

---

## Overview

Upgraded from a static baseline, this dynamic analytical engine parses local portfolio ownership states, connects to real-time market data, calculates fundamental risk metrics, and executes automated algorithmic rebalancing.

### Key Highlights
* **Dynamic Live Feeds:** Fetches live pricing and 1-year historical OHLCV data through the `yfinance` API.
* **Quantitative Data Alignment:** Resolves the cross-market **"Weekend Problem"** by forward-filling time series to align 24/7 cryptocurrency markets with standard Monday–Friday equity trading schedules prior to computing the covariance matrix.
* **Defensive I/O Architecture:** The `portfolio_io.py` module automatically detects European (`;`) versus Standard (`,`) CSV delimiters and safely decodes UTF-8-BOM files to prevent crashes across operating systems and Excel exports.
* **Algorithmic Rebalancing:** Computes current versus target allocations and generates rebalancing orders.
* **Automated Visual Analytics:** Generates a multi-panel dashboard displaying asset allocations, correlation heatmaps, and normalized 1-year performance trajectories.
* **Test-Driven Reliability:** Includes automated unit testing (`test_project.py`) to verify system integrity and financial calculations.

---

##  System Architecture

The project strictly adheres to Object-Oriented Programming (OOP) principles:

```text
├── main.py              # Primary application entry point
├── portfolio.py         # Core analytical engine for risk calculations and rebalancing
├── position.py          # Tracks individual asset ownership, cost basis, and dynamic P&L
├── asset.py             # Base class representing financial instruments and time series
├── portfolio_io.py      # Robust file I/O layer with automatic delimiter and encoding detection
├── visualizer.py        # Analytics visualization dashboard (Matplotlib / Seaborn)
├── test_project.py      # Automated unit tests
├── portfolio_data.csv   # State configuration file (holdings and target weights)
└── requirements.txt     # Python dependencies

Installation & Usage
1. Clone the repository
git clone [https://github.com/tuo-username/financial-portfolio-manager.git](https://github.com/tuo-username/financial-portfolio-manager.git)
cd financial-portfolio-manager

2. Install dependencies
pip install -r requirements.txt

3. Run the application
python main.py

4. Run the test suite
python test_project.py

Data Customization
The pipeline is completely data-agnostic. To analyze any custom portfolio, update portfolio_data.csv with your tickers and holdings:
Ticker,Quantity,CostBasis,TargetWeight
AAPL,15,150.0,0.30
BTC-USD,0.5,30000.0,0.20
MSFT,10,240.0,0.30
SPY,20,400.0,0.20

Author
Enio Hoxha – M.Sc. in Data Analytics for Economics and Management, Libera Università di Bolzano (unibz)
