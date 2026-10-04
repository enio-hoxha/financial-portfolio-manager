# visualizer.py
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


class PortfolioVisualizer:
    @staticmethod
    def show_dashboard(portfolio, target_weights):
        """Generates a visual dashboard for the portfolio."""

        fig, axes = plt.subplots(1, 3, figsize=(20, 6))
        fig.suptitle(
            f"Portfolio Analytics Dashboard: {portfolio.owner}", fontsize=16, fontweight='bold')

        # PLOT 1: Current Allocation (Pie Chart)
        labels = [p.asset.ticker for p in portfolio.positions]
        sizes = [p.market_value for p in portfolio.positions]

        explode = [0.05 if size == max(sizes) else 0 for size in sizes]

        axes[0].pie(sizes, labels=labels, autopct='%1.1f%%',
                    startangle=140, explode=explode, shadow=True)
        axes[0].set_title("Current Asset Allocation")

        # PREPARE DATA FOR PLOTS 2 & 3
        price_dict = {}
        for p in portfolio.positions:
            if p.asset.history is not None:
                hist_series = p.asset.history.copy()

                # Convert index to pure Date strings to solve the Weekend/Timezone bug
                if hasattr(hist_series.index, 'strftime'):
                    hist_series.index = hist_series.index.strftime('%Y-%m-%d')

                price_dict[p.asset.ticker] = hist_series

        if price_dict:
            # Combine all raw prices and forward-fill weekends
            df_prices = pd.DataFrame(price_dict)
            df_prices = df_prices.ffill().dropna()

            # PLOT 2: Asset Correlation Heatmap
            df_returns = df_prices.pct_change().dropna()
            correlation_matrix = df_returns.corr()

            sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", vmin=-1, vmax=1,
                        ax=axes[1], linewidths=0.5)
            axes[1].set_title("Asset Correlation Heatmap (1 Year)")

            # PLOT 3: Profit&Loss Performance Curve
            # 1. Convert string dates back to DateTime so Matplotlib can format the X-axis nicely
            df_prices.index = pd.to_datetime(df_prices.index)

            # 2. Normalize the data: (Current Price / Starting Price) * 100 - 100 = % P&L
            df_normalized = (df_prices / df_prices.iloc[0]) * 100 - 100

            # 3. Plot each asset's curve
            for column in df_normalized.columns:
                axes[2].plot(df_normalized.index,
                             df_normalized[column], label=column, linewidth=2)

            axes[2].set_title("1-Year Historical Profit&Loss (%)")
            axes[2].set_ylabel("Profit / Loss (%)")

            # Add a thick black line at 0% (The Breakeven Line)
            axes[2].axhline(y=0, color='black', linestyle='-', linewidth=1.5)

            axes[2].grid(True, linestyle='--', alpha=0.6)
            axes[2].legend(loc="upper left")

            # Auto-format the dates so they don't overlap on the X-axis
            fig.autofmt_xdate()

        else:
            axes[1].text(0.5, 0.5, "No Historical Data Available",
                         ha='center', va='center')
            axes[2].text(0.5, 0.5, "No Historical Data Available",
                         ha='center', va='center')

        # Adjust layout and show the plots
        plt.tight_layout()
        plt.show()
