from typing import Optional, List
from metrics.shared_metrics import (
 CapExIntensityMetric, GrossMarginMetric
)
from  metrics.core_metrics import Metric
from core.stock_providers import StockDataProvider
import math


def get_hardware_ecosystem_metrics() -> List[Metric]:
    # Physical products + services
    return [
    GrossMarginMetric(),
    ServicesRevenueMixMetric(),
    CapExIntensityMetric()
    ]