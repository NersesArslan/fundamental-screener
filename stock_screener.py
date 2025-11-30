from typing import Optional, Dict, List
import pandas as pd
from stock_providers import StockDataProvider
from metrics import Metric, get_default_metrics

# ============================================================================
# BUSINESS LOGIC - Screen stocks with your criteria
# ============================================================================

class StockScreener:
    """Orchestrates data fetching and metric calculation with modular metrics."""
    
    def __init__(self, provider: StockDataProvider, metrics: List[Metric] = None):
        """
        Args:
            provider: Data source (YFinanceProvider, etc.)
            metrics: List of Metric objects to calculate. If None, uses default set.
        """
        self.provider = provider
        self.metrics = metrics if metrics is not None else get_default_metrics()
    
    def screen_stock(self, ticker: str) -> Dict[str, Optional[float]]:
        """
        Fetch and calculate all metrics for a single stock.
        Returns a clean dict ready for your DataFrame.
        """
        results = {}
        
        # Calculate each metric
        for metric in self.metrics:
            try:
                value = metric.calculate(ticker, self.provider)
                results[metric.get_key()] = value
            except Exception as e:
                # If a metric fails, set to None rather than crashing
                results[metric.get_key()] = None
        
        return results
    
    def screen_multiple(self, tickers: List[str]) -> Dict[str, Dict]:
        """Screen a list of tickers. Returns {ticker: metrics_dict}."""
        results = {}
        for ticker in tickers:
            results[ticker] = self.screen_stock(ticker)
        return results
    
    def get_metric_names(self) -> Dict[str, str]:
        """Return mapping of metric keys to display names."""
        return {metric.get_key(): metric.get_name() for metric in self.metrics}