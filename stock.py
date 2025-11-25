import yfinance as yf


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


def get_stock_info(ticker_symbol):
    ticker = yf.Ticker(ticker_symbol)
    price = ticker.info.get('currentPrice')
    trailing_pe = ticker.info.get('trailingPE')
    cagr = calculate_cagr(ticker_symbol, years=5)
    debt_to_equity = ticker.info.get('debtToEquity')
    return_on_equity = ticker.info.get('returnOnEquity')
    free_cashflow = ticker.info.get('freeCashflow')

    return {
        'price': price,
        'pe_ratio': trailing_pe,
        'debt_to_equity': debt_to_equity,
        '5_year_cagr': cagr,
        'returnonequity': return_on_equity,
        'free_cashflow': free_cashflow,
    }


# Test with AAPL
print("Stock Info:")
print(get_stock_info("AAPL"))
