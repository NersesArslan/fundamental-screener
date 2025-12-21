from typing import List
from metrics.shared_metrics import GrossMarginMetric

from  metrics.core_metrics import Metric
from core.stock_providers import StockDataProvider

class SalesMarketingIntensityMetric(Metric):
    def calculate(self, ticker: str, provider: StockDataProvider) -> float | None:
        data = provider.get_operating_expense_data(ticker) or {}

        sales_marketing = data.get("sales_marketing_expense")
        revenue = data.get("revenue")

        if sales_marketing is None or revenue is None:
            return None
        if revenue <= 0:
            return None

        return sales_marketing / revenue

    def get_name(self) -> str:
        return "Sales & Marketing Intensity"

    def get_key(self) -> str:
        return "sales_marketing_intensity"

def get_cybersecurity_metrics() -> List[Metric]:
    # Security platforms, high R&D
    return [
    GrossMarginMetric(),
    SalesMarketingIntensityMetric()
    ]