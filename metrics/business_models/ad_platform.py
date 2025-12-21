from typing import Optional, List
from metrics.semiconductors import CapExIntensityMetric
from  metrics.core_metrics import Metric
from core.stock_providers import StockDataProvider
from shared_business_models.incremental_margin import IncrementalMarginMetric
import math 


class ARPUGrowthMetric(Metric):

    def __init__(self, years: int = 3):
        self.years = years

    def calculate(self, ticker: str, provider: StockDataProvider) -> Optional[float]:
        # Get time series data for revenue and user counts
        data = provider.get_user_metrics_data(ticker) or {}
        
        revenues = data.get("annual_revenues")  # List of annual revenues
        users = data.get("annual_active_users")  # List of annual user counts

        # Missing data → impute
        if revenues is None or users is None:
            return None

        # Insufficient time series data
        if len(revenues) < self.years + 1 or len(users) < self.years + 1:
            return None

        rev_start, rev_end = revenues[-(self.years + 1)], revenues[-1]
        users_start, users_end = users[-(self.years + 1)], users[-1]

        # NaN handling
        if any(
            isinstance(x, float) and math.isnan(x)
            for x in [rev_start, rev_end, users_start, users_end]
        ):
            return None

        arpu_start = rev_start / users_start
        arpu_end = rev_end / users_end

        if arpu_start <= 0 or arpu_end <= 0:
            return None

        # Invalid → drop
        if (
            rev_start <= 0
            or rev_end <= 0
            or users_start <= 0
            or users_end <= 0
        ):
            return None



        # Calculate CAGR and return as percentage
        cagr = ((arpu_end / arpu_start) ** (1 / self.years) - 1) 
        return cagr

    def get_name(self) -> str:
        return f"ARPU CAGR ({self.years}Y)"

    def get_key(self) -> str:
        return "arpu_cagr"

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