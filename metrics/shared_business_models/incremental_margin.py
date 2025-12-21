from typing import Optional
from metrics.core_metrics import Metric
from core.stock_providers import StockDataProvider
import math

class IncrementalMarginMetric(Metric):

    def calculate(self, ticker: str, provider: StockDataProvider) -> Optional[float]:
        # Get time series data for revenue and operating income
        data = provider.get_incremental_margin_data(ticker) or {}
        
        revenue_current = data.get("revenue_current")
        revenue_prior = data.get("revenue_prior")
        op_income_current = data.get("operating_income_current")
        op_income_prior = data.get("operating_income_prior")
        
        # Missing data → impute
        if any(x is None for x in [revenue_current, revenue_prior, op_income_current, op_income_prior]):
            return None
        
        # NaN handling
        if any(
            isinstance(x, float) and math.isnan(x)
            for x in [revenue_current, revenue_prior, op_income_current, op_income_prior]
        ):
            return None
        
        # Calculate changes
        revenue_change = revenue_current - revenue_prior
        op_income_change = op_income_current - op_income_prior
        
        # Invalid → drop (need positive revenue growth to be meaningful)
        if revenue_change <= 0:
            return None
        
        # Calculate incremental margin
        incremental_margin = (op_income_change / revenue_change) 
        
        return incremental_margin
    
    def get_name(self) -> str:
        return "Incremental Margin"
    
    def get_key(self) -> str:
        return "incremental_margin"