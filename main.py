"""
Stock Screener - Value investing focused
Elegantly decoupled for future data source flexibility.
"""
from stock_providers import YFinanceProvider
from stock_screener import StockScreener
from screener_output import format_screener_output



# ============================================================================
# MAIN - Wire it all together
# ============================================================================

if __name__ == "__main__":
    # Your watchlist
    semis = ['NVDA', 'AMD', 'INTC', 'TSM', 'ASML', 'QCOM', 'AVGO', 'MU', 'LRCX', 'KLAC']
    
    # Use YFinanceProvider - calculates CAGR from available quarterly data
    # Note: For some stocks like NVDA, this gives us ~3-4 years of data
    # which is still useful for growth analysis
    provider = YFinanceProvider()
    screener = StockScreener(provider)
    
    # Run the screen
    print("\nFetching stock data (calculating CAGR from TTM revenue)...")
    stocks_data = screener.screen_multiple(semis)
    
    # Pretty print
    df = format_screener_output(stocks_data)
    print("\nStock Fundamentals:")
    print(df.to_string())
    print("\nNote: Revenue CAGR calculated from Trailing Twelve Months (TTM) data")
