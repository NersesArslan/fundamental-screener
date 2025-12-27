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
        # ---- Growth ----
        # Calculate revenue CAGR using the same method as RevenueCagrMetric
        from calculation_functions import calculate_revenue_cagr_from_quarterly
        quarterly_revenue = provider.get_quarterly_revenue(ticker)
        
        if quarterly_revenue is None:
            return None
        
        cagr_pct = calculate_revenue_cagr_from_quarterly(quarterly_revenue)
        
        if cagr_pct is None or (isinstance(cagr_pct, float) and math.isnan(cagr_pct)):
            return None

        # ---- Profitability ----
        # Use get_margin_data which provides both revenue and FCF
        data = provider.get_margin_data(ticker)
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

    def get_name(self) -> str:
        return "Rule of 40"

    def get_key(self) -> str:
        return "rule_of_40"
