# main.py

from core.stock_providers import YFinanceProvider
from experiments.run_business_model import run_business_model_test

from universes.cloud_infrastructure import CLOUD_INFRASTRUCTURE
from metrics.core_metrics import get_core_metrics
from metrics.business_models.cloud_infrastructure import (
    get_cloud_infrastructure_metrics,
)
from industry.business_model_weights.cloud_infrastructure import (
    CLOUD_INFRASTRUCTURE_WEIGHT_MAP,
)

def main():
    provider = YFinanceProvider()

    run_business_model_test(
        name="Cloud Infrastructure",
        tickers=CLOUD_INFRASTRUCTURE,
        provider=provider,
        core_metrics=get_core_metrics(),
        bm_metrics=get_cloud_infrastructure_metrics(),
        weight_map=CLOUD_INFRASTRUCTURE_WEIGHT_MAP,
        normalization="minmax",
        verbose=True,
    )

if __name__ == "__main__":
    main()
