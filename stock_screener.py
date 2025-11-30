from typing import Optional, Dict, List
import pandas as pd
from calculation_functions import calculate_revenue_cagr_from_quarterly
from stock_providers import StockDataProvider

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