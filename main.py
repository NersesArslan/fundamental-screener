"""
Stock Screener - Value investing focused
Elegantly decoupled for future data source flexibility.

MODULAR METRICS SYSTEM:
- Easily add/remove metrics by customizing the metrics list
- Pre-configured sets: get_default_metrics(), get_growth_metrics(), get_value_metrics()
- Or create your own custom list!
"""
from stock_providers import YFinanceProvider
from stock_screener import StockScreener
from screener_output import format_screener_output
from metrics import (
    get_default_metrics, 
    get_growth_metrics, 
    get_value_metrics,
    PriceMetric,
    PERatioMetric,
    RevenueCagr3YearMetric,
    ROEMetric,
    FreeCashFlowMetric,
)


# ============================================================================
# MAIN - Wire it all together
# ============================================================================

if __name__ == "__main__":
    # Your watchlist
    semis = ['NVDA', 'AMD', 'INTC', 'TSM', 'ASML', 'QCOM', 'AVGO', 'MU', 'LRCX', 'KLAC']
    
    # Data provider
    provider = YFinanceProvider()
    
    # ========================================================================
    # CHOOSE YOUR METRICS - Uncomment the one you want!
    # ========================================================================
    
    # Option 1: Default metrics (balanced view)
    screener = StockScreener(provider, metrics=get_default_metrics())
    
    # Option 2: Focus on growth
    # screener = StockScreener(provider, metrics=get_growth_metrics())
    
    # Option 3: Focus on value
    # screener = StockScreener(provider, metrics=get_value_metrics())
    
    # Option 4: Custom metrics - pick exactly what you want!
    # custom_metrics = [
    #     PriceMetric(),
    #     PERatioMetric(),
    #     RevenueCagr3YearMetric(),  # Only 3-year, not 5-year
    #     ROEMetric(),
    #     FreeCashFlowMetric(),
    # ]
    # screener = StockScreener(provider, metrics=custom_metrics)
    
    # Run the screen
    print("\nFetching stock data...")
    stocks_data = screener.screen_multiple(semis)
    
    # Pretty print with metric names
    metric_names = screener.get_metric_names()
    df = format_screener_output(stocks_data, metric_names)
    print("\nStock Fundamentals:")
    print(df.to_string())
    print("\n💡 Tip: Edit main.py to customize which metrics you want to see!")
