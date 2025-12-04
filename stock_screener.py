from typing import Optional, Dict, List
import pandas as pd
from stock_providers import StockDataProvider
from metrics.core import Metric, get_core_metrics

# ============================================================================
# BUSINESS LOGIC - Screen stocks with your criteria (Industry-Aware)
# ============================================================================

class StockScreener:
    """
    Industry-aware stock screener that loads core + industry-specific metrics.
    
    Usage:
        # Semiconductors
        screener = StockScreener(provider, industry='semis')
        
        # Big tech
        screener = StockScreener(provider, industry='tech')
        
        # Custom metrics
        screener = StockScreener(provider, metrics=[...])
    """
    
    def __init__(self, provider: StockDataProvider, metrics: List[Metric] = None, industry: str = None):
        """
        Args:
            provider: Data source (YFinanceProvider, etc.)
            metrics: List of Metric objects. If None, uses core + industry overrides.
            industry: Industry type ('semis', 'tech', etc.). If None, uses only core metrics.
        """
        self.provider = provider
        
        if metrics is not None:
            # User provided custom metrics
            self.metrics = metrics
        elif industry:
            # Load core + industry-specific metrics
            self.metrics = self._load_industry_metrics(industry)
        else:
            # Default to core metrics only
            self.metrics = get_core_metrics()
    
    def _load_industry_metrics(self, industry: str) -> List[Metric]:
        """Load core metrics + industry-specific overrides."""
        core = get_core_metrics()
        
        if industry == 'semis' or industry == 'semiconductors':
            from metrics.semis_overrides import get_semis_metrics
            return core + get_semis_metrics()
        elif industry == 'tech':
            from metrics.tech_overrides import get_tech_metrics
            return core + get_tech_metrics()
        else:
            # Unknown industry, just use core
            return core
    
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