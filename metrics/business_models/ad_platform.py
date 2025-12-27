from typing import Optional, List
from metrics.shared_metrics import CapExIntensityMetric
from metrics.core_metrics import Metric
from core.stock_providers import StockDataProvider
from metrics.shared_business_models.incremental_margin import IncrementalMarginMetric
from metrics.shared_business_models.arpu_growth import ARPUGrowthMetric
import math
import numpy as np 

class RevenueVolatilityMetric(Metric):
    """
    Revenue volatility measured as the standard deviation
    of year-over-year revenue growth rates.

    Higher volatility = less durable demand aggregation.
    """

    MIN_OBSERVATIONS = 3  # minimum number of growth rates

    def calculate(self, ticker: str, provider: StockDataProvider) -> Optional[float]:
        """
        Returns revenue growth volatility in percentage points.
        """
        revenues = provider.get_annual_revenue_series(ticker)

        if not revenues or len(revenues) < self.MIN_OBSERVATIONS + 1:
            return None

        # Ensure chronological order (oldest → newest)
        revenues = sorted(revenues)

        growth_rates: List[float] = []

        for prev, curr in zip(revenues[:-1], revenues[1:]):
            if prev is None or curr is None:
                continue
            if prev <= 0:
                continue  # invalid base

            growth = (curr - prev) / prev * 100

            if isinstance(growth, float) and math.isnan(growth):
                continue

            growth_rates.append(growth)

        if len(growth_rates) < self.MIN_OBSERVATIONS:
            return None

        volatility = float(np.std(growth_rates, ddof=1))

        return volatility

    def get_name(self) -> str:
        return "Revenue Volatility"

    def get_key(self) -> str:
        return "revenue_volatility"

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
        CapExIntensityMetric(),
        RevenueVolatilityMetric()
    ]