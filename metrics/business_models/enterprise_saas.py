from typing import List
from metrics.shared_business_models.rnd_intensity import RnDIntensityMetric
from metrics.shared_business_models.rule_of_40 import RuleOf40Metric
from metrics.shared_business_models.revenue_per_employee import RevenuePerEmployeeMetric
from metrics.shared_metrics import GrossMarginMetric
from metrics.core_metrics import Metric

def get_saas_metrics() -> List[Metric]:
    # High gross margins, R&D intensive
    return [
        RnDIntensityMetric(),
        GrossMarginMetric(),
        RuleOf40Metric(),
        RevenuePerEmployeeMetric(),
    ]