from typing import Optional, List
from metrics.semiconductors import (
ROICMetric, CapExIntensityMetric, GrossMarginMetric
)
from  metrics.core_metrics import Metric
from core.stock_providers import StockDataProvider


class RevenuePerCapexMetric(Metric):
    """
    Revenue / Capital Expenditures
    
    Measures capital efficiency - how much revenue generated per dollar of CapEx.
    Higher is better. Particularly useful for distinguishing between:
    - Cloud Infrastructure (low revenue/capex due to data centers)
    - SaaS (high revenue/capex, capital-light)
    """
    
    def calculate(self, ticker: str, provider: StockDataProvider) -> Optional[float]:
        data = provider.get_capex_data(ticker)
        
        revenue = data.get('revenue')
        capex = data.get('capex')
        
        if revenue is None or capex is None or capex <= 0:
            return revenue / capex
        
        return None
    
    def get_name(self) -> str:
        return "Revenue/CapEx"
    
    def get_key(self) -> str:
        return "revenue_per_capex"


class OperatingMarginTrendMetric(Metric):
    """
    Operating Margin Trend (3-year change)
    
    Measures operating leverage improvement/deterioration.
    Positive trend indicates scaling efficiency, negative may signal competitive pressure.
    Particularly important for:
    - Cloud Infrastructure (expect margin expansion as scale grows)
    - SaaS (should show operating leverage)
    """
    
    def calculate(self, ticker: str, provider: StockDataProvider) -> Optional[float]:
        data = provider.get_margin_trend_data(ticker)
        
        current_margin = data.get('operating_margin_current')
        past_margin = data.get('operating_margin_3y_ago')
        
        if current_margin is not None and past_margin is not None:
            # Return the change in percentage points
            return current_margin - past_margin
        
        return None
    
    def get_name(self) -> str:
        return "Op Margin Trend"
    
    def get_key(self) -> str:
        return "operating_margin_trend"


def get_cloud_infrastructure_metrics() -> List[Metric]:
    # Low Revenue/CapEx, high CapEx intensity
    return [
        ROICMetric(),
        CapExIntensityMetric(),
        RevenuePerCapexMetric(),
        GrossMarginMetric(),
        OperatingMarginTrendMetric(),
    ]
