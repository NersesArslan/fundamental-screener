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