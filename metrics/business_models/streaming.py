from typing import List, Optional
from metrics.shared_business_models.arpu_growth import ARPUGrowthMetric
from  metrics.core_metrics import Metric
from core.stock_providers import StockDataProvider
import math

class ContentSpendIntensityMetric(Metric):
    """
    Content Spend Intensity = Content Spend / Revenue

    Measures how much of revenue is reinvested in content.
    Returned as a percentage (e.g. 35 = 35%).

    Most meaningful for:
    - Streaming platforms
    - Media businesses
    """

    def calculate(self, ticker: str, provider: StockDataProvider) -> Optional[float]:
        data = provider.get_content_spend_data(ticker) or {}

        content_spend = data.get("content_spend")
        revenue = data.get("revenue")

        # Missing data → impute
        if content_spend is None or revenue is None:
            return None

        # NaN handling
        if (
            isinstance(content_spend, float) and math.isnan(content_spend)
            or isinstance(revenue, float) and math.isnan(revenue)
        ):
            return None

        # Economic validity
        if revenue <= 0 or content_spend < 0:
            return None

        return (content_spend / revenue)_


def get_streaming_metrics() -> List[Metric]:
    # Content-heavy, subscriber-based
    return [
    ARPUGrowthMetric(),
    ContentSpendIntensityMetric()
    ]