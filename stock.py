import yfinance as yf
import pandas as pd


semis = ['NVDA', 'AMD', 'INTC', 'TSM', 'ASML', 'QCOM', 'AVGO', 'MU', 'LRCX', 'KLAC']



def calculate_cagr(ticker_symbol, years=5):
    """Calculate Compound Annual Growth Rate for a stock over specified years."""
    ticker = yf.Ticker(ticker_symbol)
    
    # Get historical data for the specified period
    hist = ticker.history(period=f"{years}y")
    
    if len(hist) < 2:
        return None  # Not enough data
    
    beginning_value = hist['Close'].iloc[0]
    ending_value = hist['Close'].iloc[-1]
    
    # CAGR formula: ((Ending / Beginning) ^ (1 / Years)) - 1
    cagr = (ending_value / beginning_value) ** (1 / years) - 1
    
    return float(cagr * 100)  # Convert to Python float and return as percentage


def get_stock_info(ticker_symbols):
    """
    Get fundamental metrics for one or more stocks.
    
    Args:
        ticker_symbols: Single ticker string (e.g., 'AAPL') or list of tickers (e.g., ['AAPL', 'MSFT', 'GOOGL'])
    
    Returns:
        Dictionary with ticker symbols as keys and their metrics as values
    """
    # Handle single ticker as string
    if isinstance(ticker_symbols, str):
        ticker_symbols = [ticker_symbols]
    
    results = {}
    
    for ticker_symbol in ticker_symbols:
        ticker = yf.Ticker(ticker_symbol)
        price = ticker.info.get('currentPrice')
        trailing_pe = ticker.info.get('trailingPE')
        cagr = calculate_cagr(ticker_symbol, years=5)
        debt_to_equity = ticker.info.get('debtToEquity')
        return_on_equity = ticker.info.get('returnOnEquity')
        free_cashflow = ticker.info.get('freeCashflow')

        results[ticker_symbol] = {
            'price': price,
            'pe_ratio': trailing_pe,
            'debt_to_equity': debt_to_equity,
            '5_year_cagr': cagr,
            'returnonequity': return_on_equity,
            'free_cashflow': free_cashflow,
        }
    
    return results

# Test with multiple stocks
stocks_data = get_stock_info(semis)

# Convert to DataFrame for better display
df = pd.DataFrame(stocks_data).T  # Transpose so stocks are rows
df.index.name = 'Ticker'

# Format numeric columns for readability
df['price'] = df['price'].apply(lambda x: f"${x:.2f}" if x else None)
df['pe_ratio'] = df['pe_ratio'].apply(lambda x: f"{x:.2f}" if x else None)
df['debt_to_equity'] = df['debt_to_equity'].apply(lambda x: f"{x:.2f}" if x else None)
df['5_year_cagr'] = df['5_year_cagr'].apply(lambda x: f"{x:.2f}%" if x else None)
df['returnonequity'] = df['returnonequity'].apply(lambda x: f"{x:.2%}" if x else None)
df['free_cashflow'] = df['free_cashflow'].apply(lambda x: f"${x:,.0f}" if x else None)

# Rename columns for better readability
df.columns = ['Price', 'P/E Ratio', 'Debt/Equity', '5Y CAGR', 'ROE', 'Free Cash Flow']

print("\nStock Fundamentals:")
print(df.to_string())
