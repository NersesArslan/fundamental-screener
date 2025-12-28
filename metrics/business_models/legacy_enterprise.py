from typing import Optional, List
from metrics.shared_metrics import CapExIntensityMetric

from  metrics.core_metrics import Metric
from core.stock_providers import StockDataProvider
import math
import numpy as np

class FCFYieldMetric(Metric):
    """
    FCF Yield = Free Cash Flow / Market Capitalization

    Measures cash return relative to market value.
    Returned as a percentage (e.g. 6 = 6%).
    Negative values are allowed.
    """

    def calculate(self, ticker: str, provider: StockDataProvider) -> Optional[float]:
        data = provider.get_valuation_data(ticker) or {}

        fcf = data.get("free_cashflow")
        market_cap = data.get("market_cap")

        # Missing data → impute
        if fcf is None or market_cap is None:
            return None

        # NaN handling
        if (
            isinstance(fcf, float) and math.isnan(fcf)
            or isinstance(market_cap, float) and math.isnan(market_cap)
        ):
            return None

        # Economic validity
        if market_cap <= 0:
            return None

        return (fcf / market_cap) * 100

    def get_name(self) -> str:
        return "FCF Yield (%)"

    def get_key(self) -> str:
        return "fcf_yield"

class RevenueVolatilityMetric(Metric):
    """
    Revenue Volatility = Std Dev of YoY Revenue Growth Rates

    Measures consistency of revenue growth.
    Returned as percentage-point volatility.
    """

    def calculate(self, ticker: str, provider: StockDataProvider) -> Optional[float]:
        revenues = provider.get_annual_revenue_series(ticker)

        # Require sufficient history (need at least 4 years for 3 growth rates)
        if revenues is None or len(revenues) < 4:
            return None

        # NaN handling
        if any(isinstance(r, float) and math.isnan(r) for r in revenues):
            return None

        growth_rates = []
        for i in range(1, len(revenues)):
            prev = revenues[i - 1]
            curr = revenues[i]

            # Economic validity
            if prev <= 0 or curr <= 0:
                return None

            growth = (curr - prev) / prev
            if isinstance(growth, float) and math.isnan(growth):
                return None

            growth_rates.append(growth)

        # Require enough observations for volatility
        if len(growth_rates) < 3:
            return None

        # Return as percentage-point volatility
        return float(np.std(growth_rates)) * 100

    def get_name(self) -> str:
        return "Revenue Volatility (%)"

    def get_key(self) -> str:
        return "revenue_volatility"


def get_legacy_enterprise_metrics() -> List[Metric]:
    # Mature tech, steady cash flow
    return [
    FCFYieldMetric(),
    RevenueVolatilityMetric(),
    CapExIntensityMetric()
    ]