from typing import Optional, List
from metrics.shared_metrics import CapExIntensityMetric
from metrics.core_metrics import Metric
from core.stock_providers import StockDataProvider
from metrics.shared_business_models.incremental_margin import IncrementalMarginMetric
from metrics.shared_business_models.arpu_growth import ARPUGrowthMetric
import math 


class RnDIntensityMetric(Metric):
    """
    R&D Intensity = R&D Expense / Revenue (%)
    
    Indicates investment in innovation.
    Particularly meaningful for:
    - SaaS
    - Enterprise software
    - Semiconductor designers
    """
    
    def calculate(self, ticker: str, provider: StockDataProvider) -> Optional[float]:
        data = provider.get_rnd_data(ticker) or {}
        
        rnd_expense = data.get("research_development")
        revenue = data.get("revenue")
        
        # Missing data → impute
        if rnd_expense is None or revenue is None:
            return None
        
        # Invalid revenue → not meaningful
        if revenue <= 0:
            return None
        
        # Handle NaN explicitly
        if (
            isinstance(rnd_expense, float) and math.isnan(rnd_expense)
            or isinstance(revenue, float) and math.isnan(revenue)
        ):
            return None
        
        return (rnd_expense / revenue) 
    
    def get_name(self) -> str:
        return "R&D Intensity"
    
    def get_key(self) -> str:
        return "rnd_intensity"
    
def get_ad_platform_metrics() -> List[Metric]:
    # User engagement, monetization efficiency
    return [
        ARPUGrowthMetric(),
        IncrementalMarginMetric(),
        RnDIntensityMetric(),
        CapExIntensityMetric()
    ]