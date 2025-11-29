"""
Stock Screener - Value investing focused
Elegantly decoupled for future data source flexibility.
"""

import yfinance as yf
import pandas as pd
from abc import ABC, abstractmethod
from typing import Optional, Dict, List
from datetime import datetime


# ============================================================================
# DATA LAYER - Abstract away the data source
# ============================================================================

class StockDataProvider(ABC):
    """Abstract interface for fetching stock data. Swap implementations freely."""
    
    @abstractmethod
    def get_price(self, ticker: str) -> Optional[float]:
        """Current stock price."""
        pass
    
    @abstractmethod
    def get_quarterly_revenue(self, ticker: str) -> Optional[pd.Series]:
        """Quarterly revenue series (indexed by date, most recent first)."""
        pass
    
    @abstractmethod
    def get_fundamentals(self, ticker: str) -> Dict[str, Optional[float]]:
        """PE ratio, debt/equity, ROE, FCF, etc."""
        pass


class YFinanceProvider(StockDataProvider):
    """Current implementation using yfinance. Can swap for FMP/Alpha Vantage later."""
    
    def get_price(self, ticker: str) -> Optional[float]:
        try:
            return yf.Ticker(ticker).info.get('currentPrice')
        except:
            return None
    
    def get_quarterly_revenue(self, ticker: str) -> Optional[pd.Series]:
        """Fetch quarterly revenue. yfinance gives us ~4 years of quarters."""
        try:
            fin = yf.Ticker(ticker).quarterly_financials
            if fin is None or 'Total Revenue' not in fin.index:
                return None
            return fin.loc['Total Revenue'].dropna()
        except:
            return None
    
    def get_fundamentals(self, ticker: str) -> Dict[str, Optional[float]]:
        """Grab the usual suspects from yfinance.info"""
        try:
            info = yf.Ticker(ticker).info
            return {
                'pe_ratio': info.get('trailingPE'),
                'debt_to_equity': info.get('debtToEquity'),
                'return_on_equity': info.get('returnOnEquity'),
                'free_cashflow': info.get('freeCashflow'),
            }
        except:
            return {
                'pe_ratio': None,
                'debt_to_equity': None,
                'return_on_equity': None,
                'free_cashflow': None,
            }


# ============================================================================
# CALCULATION LAYER - Pure functions, source-agnostic
# ============================================================================

def calculate_revenue_cagr_from_quarterly(quarterly_revenue: pd.Series, years: int = 5) -> Optional[float]:
    """
    Calculate revenue CAGR from quarterly data.
    Workaround for yfinance's 4-year annual limit.
    
    Args:
        quarterly_revenue: Series of quarterly revenues (most recent first)
        years: Target years for CAGR calculation
    
    Returns:
        CAGR as percentage, or None if insufficient data
    """
    if quarterly_revenue is None or len(quarterly_revenue) < 2:
        return None
    
    # Need 4 quarters per year + 1 extra to span the period
    quarters_needed = (years * 4) + 1
    
    if len(quarterly_revenue) < quarters_needed:
        # Fallback to whatever we have (minimum 2 quarters = 0.5 years)
        if len(quarterly_revenue) < 2:
            return None
        quarters_needed = len(quarterly_revenue)
    
    # Sum first 4 quarters (most recent year) and last 4 quarters (oldest year)
    ending_revenue = quarterly_revenue.iloc[:4].sum()
    beginning_revenue = quarterly_revenue.iloc[quarters_needed-4:quarters_needed].sum()
    
    # Calculate actual time span
    actual_years = (quarterly_revenue.index[0] - quarterly_revenue.index[quarters_needed-1]).days / 365.25
    
    if beginning_revenue <= 0 or actual_years <= 0:
        return None
    
    cagr = (ending_revenue / beginning_revenue) ** (1 / actual_years) - 1
    return float(cagr * 100)


def calculate_cagr_generic(values: pd.Series, years: int = 5) -> Optional[float]:
    """
    Generic CAGR calculator. Works for any time series.
    Supply price history, revenue, earnings, whatever.
    """
    if values is None or len(values) < 2:
        return None
    
    beginning = values.iloc[-1]  # Oldest
    ending = values.iloc[0]  # Most recent
    
    if beginning <= 0:
        return None
    
    # Time span from the data itself
    time_diff = (values.index[0] - values.index[-1]).days / 365.25
    actual_years = time_diff if time_diff > 0 else years
    
    cagr = (ending / beginning) ** (1 / actual_years) - 1
    return float(cagr * 100)


# ============================================================================
# BUSINESS LOGIC - Screen stocks with your criteria
# ============================================================================

class StockScreener:
    """Orchestrates data fetching and metric calculation."""
    
    def __init__(self, provider: StockDataProvider):
        self.provider = provider
    
    def screen_stock(self, ticker: str) -> Dict[str, Optional[float]]:
        """
        Fetch and calculate all metrics for a single stock.
        Returns a clean dict ready for your DataFrame.
        """
        price = self.provider.get_price(ticker)
        fundamentals = self.provider.get_fundamentals(ticker)
        
        # Revenue CAGR using quarterly workaround
        quarterly_rev = self.provider.get_quarterly_revenue(ticker)
        revenue_cagr = calculate_revenue_cagr_from_quarterly(quarterly_rev, years=5)
        
        return {
            'price': price,
            'pe_ratio': fundamentals['pe_ratio'],
            'debt_to_equity': fundamentals['debt_to_equity'],
            '5_year_cagr': revenue_cagr,
            'returnonequity': fundamentals['return_on_equity'],
            'free_cashflow': fundamentals['free_cashflow'],
        }
    
    def screen_multiple(self, tickers: List[str]) -> Dict[str, Dict]:
        """Screen a list of tickers. Returns {ticker: metrics_dict}."""
        results = {}
        for ticker in tickers:
            results[ticker] = self.screen_stock(ticker)
        return results


# ============================================================================
# PRESENTATION LAYER - Format output prettily
# ============================================================================

def format_screener_output(results: Dict[str, Dict]) -> pd.DataFrame:
    """Transform raw metrics into a beautiful table."""
    df = pd.DataFrame(results).T
    df.index.name = 'Ticker'
    
    # Format columns for human consumption
    df['price'] = df['price'].apply(lambda x: f"${x:.2f}" if x else None)
    df['pe_ratio'] = df['pe_ratio'].apply(lambda x: f"{x:.2f}" if x else None)
    df['debt_to_equity'] = df['debt_to_equity'].apply(lambda x: f"{x:.2f}" if x else None)
    df['5_year_cagr'] = df['5_year_cagr'].apply(lambda x: f"{x:.2f}%" if x else None)
    df['returnonequity'] = df['returnonequity'].apply(lambda x: f"{x:.2%}" if x else None)
    df['free_cashflow'] = df['free_cashflow'].apply(lambda x: f"${x:,.0f}" if x else None)
    
    # Readable column names
    df.columns = ['Price', 'P/E Ratio', 'Debt/Equity', '5Y CAGR', 'ROE', 'Free Cash Flow']
    
    return df


# ============================================================================
# MAIN - Wire it all together
# ============================================================================

if __name__ == "__main__":
    # Your watchlist
    semis = ['NVDA', 'AMD', 'INTC', 'TSM', 'ASML', 'QCOM', 'AVGO', 'MU', 'LRCX', 'KLAC']
    
    # Instantiate with yfinance (swap for FMP later by changing one line)
    provider = YFinanceProvider()
    screener = StockScreener(provider)
    
    # Run the screen
    stocks_data = screener.screen_multiple(semis)
    
    # Pretty print
    df = format_screener_output(stocks_data)
    print("\nStock Fundamentals:")
    print(df.to_string())

# def calculate_revenue_cagr(ticker_symbol, years=5):
#     """Calculate Revenue Compound Annual Growth Rate for a stock over specified years."""
#     ticker = yf.Ticker(ticker_symbol)

#     # Get annual financial statements
#     fin = ticker.financials
#     if fin is None or "Total Revenue" not in fin.index:
#         return None
    
#     rev = fin.loc["Total Revenue"].dropna()  # Pandas Series of revenues, drop NaN

#     # yfinance typically returns only 4 years of annual data
#     # Use available data or fallback to shorter period
#     if len(rev) < 2:
#         return None
    
#     # Use the requested years or whatever we have available
#     actual_periods = min(years, len(rev) - 1)
    
#     ending_rev = rev.iloc[0]
#     beginning_rev = rev.iloc[actual_periods]

#     actual_years = (rev.index[0] - rev.index[actual_periods]).days / 365.25
#     cagr = (ending_rev / beginning_rev) ** (1 / actual_years) - 1
#     return float(cagr * 100)


# def calculate_cagr(ticker_symbol, years=5):
#     """Calculate Compound Annual Growth Rate for a stock over specified years."""
#     ticker = yf.Ticker(ticker_symbol)
    
#     # Get historical data for the specified period
#     hist = ticker.history(period=f"{years}y")
    
#     if len(hist) < 2:
#         return None  # Not enough data
    
#     beginning_value = hist['Close'].iloc[0]
#     ending_value = hist['Close'].iloc[-1]
    
#     # CAGR formula: ((Ending / Beginning) ^ (1 / Years)) - 1
#     cagr = (ending_value / beginning_value) ** (1 / years) - 1
    
#     return float(cagr * 100)  # Convert to Python float and return as percentage


# def get_stock_info(ticker_symbols):
#     """
#     Get fundamental metrics for one or more stocks.
    
#     Args:
#         ticker_symbols: Single ticker string (e.g., 'AAPL') or list of tickers (e.g., ['AAPL', 'MSFT', 'GOOGL'])
    
#     Returns:
#         Dictionary with ticker symbols as keys and their metrics as values
#     """
#     # Handle single ticker as string
#     if isinstance(ticker_symbols, str):
#         ticker_symbols = [ticker_symbols]
    
#     results = {}
    
#     for ticker_symbol in ticker_symbols:
#         ticker = yf.Ticker(ticker_symbol)
#         price = ticker.info.get('currentPrice')
#         trailing_pe = ticker.info.get('trailingPE')
#         cagr = calculate_revenue_cagr(ticker_symbol, years=5)
#         debt_to_equity = ticker.info.get('debtToEquity')
#         return_on_equity = ticker.info.get('returnOnEquity')
#         free_cashflow = ticker.info.get('freeCashflow')

#         results[ticker_symbol] = {
#             'price': price,
#             'pe_ratio': trailing_pe,
#             'debt_to_equity': debt_to_equity,
#             '5_year_cagr': cagr,
#             'returnonequity': return_on_equity,
#             'free_cashflow': free_cashflow,
#         }
    
#     return results

# # Test with multiple stocks
# stocks_data = get_stock_info(semis)

# # Convert to DataFrame for better display
# df = pd.DataFrame(stocks_data).T  # Transpose so stocks are rows
# df.index.name = 'Ticker'

# # Format numeric columns for readability
# df['price'] = df['price'].apply(lambda x: f"${x:.2f}" if x else None)
# df['pe_ratio'] = df['pe_ratio'].apply(lambda x: f"{x:.2f}" if x else None)
# df['debt_to_equity'] = df['debt_to_equity'].apply(lambda x: f"{x:.2f}" if x else None)
# df['5_year_cagr'] = df['5_year_cagr'].apply(lambda x: f"{x:.2f}%" if x else None)
# df['returnonequity'] = df['returnonequity'].apply(lambda x: f"{x:.2%}" if x else None)
# df['free_cashflow'] = df['free_cashflow'].apply(lambda x: f"${x:,.0f}" if x else None)

# # Rename columns for better readability
# df.columns = ['Price', 'P/E Ratio', 'Debt/Equity', '5Y CAGR', 'ROE', 'Free Cash Flow']

# print("\nStock Fundamentals:")
# print(df.to_string())
