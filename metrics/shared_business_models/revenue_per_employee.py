from typing import Optional
from metrics.core_metrics import Metric
from core.stock_providers import StockDataProvider
import math


class RevenuePerEmployeeMetric(Metric):
    """
    Revenue per Employee = Total Revenue / Full-Time Employees

    Measures human capital efficiency and scalability.
    Returned as $ thousands per employee (unit-normalized).
    """

    def calculate(self, ticker: str, provider: StockDataProvider) -> Optional[float]:
        data = provider.get_employee_data(ticker)

        revenue = data.get("revenue")
        employees = data.get("full_time_employees")

        # Missing → impute
        if revenue is None or employees is None:
            return None

        # NaN handling
        if (
            isinstance(revenue, float) and math.isnan(revenue)
            or isinstance(employees, float) and math.isnan(employees)
        ):
            return None

        # Economic validity
        if revenue <= 0 or employees <= 0:
            return None

        # $ thousands per employee
        return (revenue / employees) / 1_000

    def get_name(self) -> str:
        return "Revenue per Employee ($K)"

    def get_key(self) -> str:
        return "revenue_per_employee"
