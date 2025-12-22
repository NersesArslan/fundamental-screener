from typing import Optional
from metrics.core_metrics import Metric
from core.stock_providers import StockDataProvider
import math

class RuleOf40Metric(Metric):
    """
    Rule of 40 = Revenue Growth % + FCF Margin %

    SaaS efficiency benchmark. Healthy SaaS companies should be >= 40.
    """

    def calculate(self, ticker: str, provider: StockDataProvider) -> Optional[float]:
        # ---- Growth (assumed % per project invariant) ----
        growth_data = provider.get_growth_data(ticker) or {}
        cagr_pct = growth_data.get("revenue_cagr_3y")

        if cagr_pct is None or (
            isinstance(cagr_pct, float) and math.isnan(cagr_pct)
        ):
            return None

        # ---- Profitability ----
        data = provider.get_profitability_data(ticker) or {}
        revenue = data.get("revenue")
        fcf = data.get("free_cashflow")

        if revenue is None or fcf is None or revenue <= 0:
            return None

        if (
            isinstance(revenue, float) and math.isnan(revenue)
            or isinstance(fcf, float) and math.isnan(fcf)
        ):
            return None

        fcf_margin_pct = (fcf / revenue) * 100

        return cagr_pct + fcf_margin_pct
