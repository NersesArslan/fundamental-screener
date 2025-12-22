from typing import Optional, List
from metrics.shared_metrics import (
 CapExIntensityMetric, GrossMarginMetric
)
from  metrics.core_metrics import Metric
from core.stock_providers import StockDataProvider
import math

class ServicesRevenueMixMetric(Metric):
    """
    Services Revenue Mix = Services Revenue / Total Revenue

    Measures revenue composition.
    Returned as a percentage (e.g. 42 = 42%).
    """

    def calculate(self, ticker: str, provider: StockDataProvider) -> Optional[float]:
        data = provider.get_segment_revenue_data(ticker) or {}

        services_rev = data.get("services_revenue")
        total_rev = data.get("total_revenue")

        # Missing data → impute
        if services_rev is None or total_rev is None:
            return None

        # NaN handling
        if (
            isinstance(services_rev, float) and math.isnan(services_rev)
            or isinstance(total_rev, float) and math.isnan(total_rev)
        ):
            return None

        # Economic validity
        if total_rev <= 0 or services_rev < 0:
            return None

        return (services_rev / total_rev) * 100

    def get_name(self) -> str:
        return "Services Revenue Mix (%)"

    def get_key(self) -> str:
        return "services_revenue_mix"


def get_hardware_ecosystem_metrics() -> List[Metric]:
    # Physical products + services
    return [
    GrossMarginMetric(),
    ServicesRevenueMixMetric(),
    CapExIntensityMetric()
    ]