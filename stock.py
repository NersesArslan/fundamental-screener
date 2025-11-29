"""
Stock Screener - Value investing focused
Elegantly decoupled for future data source flexibility.
"""

import yfinance as yf
import pandas as pd
from abc import ABC, abstractmethod
from typing import Optional, Dict, List


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
    """Use yfinance for all stock data - free and reliable."""
    
    def get_price(self, ticker: str) -> Optional[float]:
        try:
            return yf.Ticker(ticker).info.get('currentPrice')
        except:
            return None
    
    def get_quarterly_revenue(self, ticker: str) -> Optional[pd.Series]:
        """
        Fetch revenue data - uses TTM when enough quarterly data, otherwise annual.
        """
        try:
            # Get quarterly data
            quarterly_fin = yf.Ticker(ticker).quarterly_financials
            if quarterly_fin is None or 'Total Revenue' not in quarterly_fin.index:
                return None
            
            quarterly_rev = quarterly_fin.loc['Total Revenue'].dropna()
            
            # Need at least 8 quarters (2 years) to calculate meaningful TTM-based CAGR
            if len(quarterly_rev) < 8:
                # Fall back to annual data
                annual_fin = yf.Ticker(ticker).financials
                if annual_fin is not None and 'Total Revenue' in annual_fin.index:
                    return annual_fin.loc['Total Revenue'].dropna()
                return None
            
            # Calculate rolling TTM (Trailing Twelve Months)
            ttm_values = []
            ttm_dates = []
            
            for i in range(len(quarterly_rev) - 3):
                ttm = quarterly_rev.iloc[i:i+4].sum()
                ttm_values.append(ttm)
                ttm_dates.append(quarterly_rev.index[i])
            
            if not ttm_values:
                return None
            
            return pd.Series(ttm_values, index=ttm_dates)
        except:
            return None
    
    def get_fundamentals(self, ticker: str) -> Dict[str, Optional[float]]:
        """Grab the usual suspects from yfinance.info and cash flow statement"""
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            
            # Calculate TTM FCF from quarterly cash flow statement (more reliable)
            fcf = None
            try:
                cf_q = stock.quarterly_cashflow
                if cf_q is not None and 'Free Cash Flow' in cf_q.index:
                    fcf_series = cf_q.loc['Free Cash Flow'].dropna()
                    if len(fcf_series) >= 4:
                        fcf = fcf_series.iloc[:4].sum()  # TTM
                        
                        # Handle currency conversion for international stocks
                        financial_currency = info.get('financialCurrency', 'USD')
                        quote_currency = info.get('currency', 'USD')
                        
                        # If financials are in different currency, convert using approximate rates
                        # This is a simple approximation - real solution would use live FX rates
                        if financial_currency != 'USD' and quote_currency == 'USD':
                            # Common conversions (approximate rates as of late 2025)
                            conversion_rates = {
                                'TWD': 32,    # Taiwan Dollar
                                'EUR': 0.92,  # Euro
                                'JPY': 150,   # Japanese Yen
                                'KRW': 1300,  # Korean Won
                                'GBP': 0.79,  # British Pound
                            }
                            
                            rate = conversion_rates.get(financial_currency, 1)
                            fcf = fcf / rate
            except:
                pass
            
            return {
                'pe_ratio': info.get('trailingPE'),
                'debt_to_equity': info.get('debtToEquity'),
                'return_on_equity': info.get('returnOnEquity'),
                'free_cashflow': fcf,
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
    Calculate revenue CAGR from quarterly OR annual data.
    Handles both quarterly and annual revenue series.
    
    Args:
        quarterly_revenue: Series of revenues (most recent first) - can be quarterly or annual
        years: Target years for CAGR calculation (will use all available data if less than target)
    
    Returns:
        CAGR as percentage, or None if insufficient data
    
    Note: Automatically falls back to whatever data is available (typically 3-4 years for most stocks)
    """
    if quarterly_revenue is None or len(quarterly_revenue) < 2:
        return None
    
    # Detect if this is annual or quarterly data by checking time gaps
    if len(quarterly_revenue) >= 2:
        avg_gap_days = (quarterly_revenue.index[0] - quarterly_revenue.index[-1]).days / (len(quarterly_revenue) - 1)
        is_annual = avg_gap_days > 200  # If average gap > 200 days, treat as annual
    else:
        is_annual = False
    
    if is_annual:
        # Annual data - simpler calculation
        if len(quarterly_revenue) < 2:
            return None
        
        # Use all available data
        ending_revenue = quarterly_revenue.iloc[0]
        beginning_revenue = quarterly_revenue.iloc[-1]
        actual_years = (quarterly_revenue.index[0] - quarterly_revenue.index[-1]).days / 365.25
        
        if beginning_revenue <= 0 or actual_years <= 0:
            return None
        
        cagr = (ending_revenue / beginning_revenue) ** (1 / actual_years) - 1
        return float(cagr * 100)
    else:
        # Quarterly data - need to group into years
        quarters_needed = (years * 4) + 1
        
        if len(quarterly_revenue) < quarters_needed:
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
        
        # Revenue CAGR from TTM (Trailing Twelve Months) data
        # Note: Uses rolling TTM to capture most current performance
        ttm_revenue = self.provider.get_quarterly_revenue(ticker)
        revenue_cagr = calculate_revenue_cagr_from_quarterly(ttm_revenue)
        
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
    df['debt_to_equity'] = df['debt_to_equity'].apply(lambda x: f"{x:.2f}%" if x else None)
    df['5_year_cagr'] = df['5_year_cagr'].apply(lambda x: f"{x:.2f}%" if x else None)
    df['returnonequity'] = df['returnonequity'].apply(lambda x: f"{x:.2%}" if x else None)
    df['free_cashflow'] = df['free_cashflow'].apply(lambda x: f"${x:,.0f}" if x else None)
    
    # Readable column names
    df.columns = ['Price', 'P/E Ratio', 'Debt/Equity', '3Y CAGR', 'ROE', 'Free Cash Flow (TTM)']
    
    return df


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
