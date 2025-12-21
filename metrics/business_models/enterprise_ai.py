from typing import List
from metrics.shared_business_models.incremental_margin import IncrementalMarginMetric
from metrics.shared_business_models.rnd_intensity import RnDIntensityMetric
from metrics.core_metrics import Metric




def get_enterprise_ai_metrics() -> List[Metric]:
    # Data platforms, AI/ML infrastructure
    return [
    IncrementalMarginMetric(),
    RnDIntensityMetric()
    ]