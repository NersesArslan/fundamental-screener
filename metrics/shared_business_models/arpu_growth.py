from typing import Optional
from metrics.core_metrics import Metric
from core.stock_providers import StockDataProvider
import math

class ARPUGrowthMetric(Metric):

    def __init__(self, years: int = 3):
        self.years = years

    def calculate(self, ticker: str, provider: StockDataProvider) -> Optional[float]:
        data = provider.get_user_metrics_data(ticker) or {}

        revenues = data.get("annual_revenues")
        users = data.get("annual_active_users")

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

        # Economic validity
        if (
            rev_start <= 0
            or rev_end <= 0
            or users_start <= 0
            or users_end <= 0
        ):
            return None

        arpu_start = rev_start / users_start
        arpu_end = rev_end / users_end

        # Defensive (should already be guaranteed, but cheap)
        if arpu_start <= 0 or arpu_end <= 0:
            return None

        # CAGR (%)
        cagr = ((arpu_end / arpu_start) ** (1 / self.years) - 1) * 100
        return cagr

    def get_name(self) -> str:
        return f"ARPU CAGR ({self.years}Y)"

    def get_key(self) -> str:
        return "arpu_cagr"
