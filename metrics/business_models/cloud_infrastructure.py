from typing import Optional, List
from metrics.shared_metrics import (
ROICMetric, CapExIntensityMetric, GrossMarginMetric
)
from  metrics.core_metrics import Metric
from core.stock_providers import StockDataProvider
import math

class RevenuePerCapexMetric(Metric):
    """
    Revenue / Capital Expenditures

    Measures capital efficiency — how much revenue is generated per dollar of CapEx.
    Unitless ratio (not a percentage).
    """

    def calculate(self, ticker: str, provider: StockDataProvider) -> Optional[float]:
        data = provider.get_capex_data(ticker) or {}

        revenue = data.get("revenue")
        capex = data.get("capital_expenditure")  # Match provider key name

        # Missing data → impute
        if revenue is None or capex is None:
            return None

        # NaN handling
        if (
            isinstance(revenue, float) and math.isnan(revenue)
            or isinstance(capex, float) and math.isnan(capex)
        ):
            return None

        # CapEx is negative in cash flow statement, take absolute value
        capex_abs = abs(capex)
        
        # Economic validity
        if revenue <= 0 or capex_abs == 0:
            return None

        return revenue / capex_abs

    def get_name(self) -> str:
        return "Revenue / CapEx"

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
