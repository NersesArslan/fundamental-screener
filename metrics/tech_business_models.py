"""
Big Tech Industry-Specific Metrics

These metrics are particularly relevant for large technology companies:
- R&D Intensity: Innovation investment
- Net Debt/FCF: Alternative leverage metric for cash-rich tech
"""

from typing import List, Optional
import math
from metrics.core import Metric
from stock_providers import StockDataProvider
from semis_overrides import ROICMetric, CapExIntensityMetric, GrossMarginMetric
import numpy as np

class RnDIntensityMetric(Metric):
    """
    R&D Intensity = R&D Expense / Revenue (%)
    
    Indicates investment in innovation.
    Particularly meaningful for:
    - SaaS
    - Enterprise software
    - Semiconductor designers
    """
    
    def calculate(self, ticker: str, provider: StockDataProvider) -> Optional[float]:
        data = provider.get_rnd_data(ticker) or {}
        
        rnd_expense = data.get("research_development")
        revenue = data.get("revenue")
        
        # Missing data → impute
        if rnd_expense is None or revenue is None:
            return None
        
        # Invalid revenue → not meaningful
        if revenue <= 0:
            return None
        
        # Handle NaN explicitly
        if (
            isinstance(rnd_expense, float) and math.isnan(rnd_expense)
            or isinstance(revenue, float) and math.isnan(revenue)
        ):
            return None
        
        return (rnd_expense / revenue) * 100
    
    def get_name(self) -> str:
        return "R&D Intensity"
    
    def get_key(self) -> str:
        return "rnd_intensity"


class NetDebtToFCFMetric(Metric):
    """
    Net Debt / Free Cash Flow
    
    Alternative to Net Debt/EBITDA for cash-generating tech companies.
    Shows how many years of FCF needed to pay off net debt.
    """
    
    def calculate(self, ticker: str, provider: StockDataProvider) -> Optional[float]:
        data = provider.get_leverage_data(ticker)
        
        total_debt = data.get('total_debt')
        cash = data.get('cash')
        free_cashflow = data.get('free_cashflow')
        
        if all(x is not None for x in [total_debt, cash, free_cashflow]):
            net_debt = total_debt - cash
            if free_cashflow > 0:
                return net_debt / free_cashflow
        
        return None
    
    def get_name(self) -> str:
        return "Net Debt/FCF"
    
    def get_key(self) -> str:
        return "net_debt_to_fcf"


class RevenuePerCapexMetric(Metric):
    """
    Revenue / Capital Expenditures
    
    Measures capital efficiency - how much revenue generated per dollar of CapEx.
    Higher is better. Particularly useful for distinguishing between:
    - Cloud Infrastructure (low revenue/capex due to data centers)
    - SaaS (high revenue/capex, capital-light)
    """
    
    def calculate(self, ticker: str, provider: StockDataProvider) -> Optional[float]:
        data = provider.get_capex_data(ticker)
        
        revenue = data.get('revenue')
        capex = data.get('capex')
        
        if revenue and capex and capex > 0:
            return revenue / capex
        
        return None
    
    def get_name(self) -> str:
        return "Revenue/CapEx"
    
    def get_key(self) -> str:
        return "revenue_per_capex"


class OperatingMarginTrendMetric(Metric):
    """
    Operating Margin Trend (3-year change)
    
    Measures operating leverage improvement/deterioration.
    Positive trend indicates scaling efficiency, negative may signal competitive pressure.
    Particularly important for:
    - Cloud Infrastructure (expect margin expansion as scale grows)
    - SaaS (should show operating leverage)
    """
    
    def calculate(self, ticker: str, provider: StockDataProvider) -> Optional[float]:
        data = provider.get_margin_trend_data(ticker)
        
        current_margin = data.get('operating_margin_current')
        past_margin = data.get('operating_margin_3y_ago')
        
        if current_margin is not None and past_margin is not None:
            # Return the change in percentage points
            return current_margin - past_margin
        
        return None
    
    def get_name(self) -> str:
        return "Op Margin Trend"
    
    def get_key(self) -> str:
        return "operating_margin_trend"


class RuleOf40Metric(Metric):
    """
    Rule of 40 = Revenue Growth % + FCF Margin %
    
    SaaS efficiency benchmark. Healthy SaaS companies should be >= 40.
    - High-growth, low-margin: 50% growth + (-10%) margin = 40
    - Mature, high-margin: 10% growth + 30% margin = 40
    
    For public markets, using 3Y Revenue CAGR is a robust proxy for growth.
    Allows negative FCF (important for high-growth SaaS burning cash).
    """
    
    def calculate(self, ticker: str, provider: StockDataProvider) -> Optional[float]:
        # ---- Growth (3Y CAGR for consistency) ----
        growth_data = provider.get_growth_data(ticker) or {}
        cagr = growth_data.get("revenue_cagr_3y")
        
        # ---- FCF margin ----
        data = provider.get_profitability_data(ticker) or {}
        revenue = data.get("revenue")
        fcf = data.get("free_cashflow")
        
        # Validate revenue + fcf presence (allow fcf negative/zero)
        if revenue is None or fcf is None or revenue <= 0:
            return None
        
        # Validate CAGR (check for None or NaN)
        if cagr is None or (isinstance(cagr, float) and math.isnan(cagr)):
            return None
        
        # Convert CAGR to percent if it looks like a decimal (e.g. 0.12 -> 12)
        cagr_pct = cagr * 100 if abs(cagr) <= 1 else cagr
        
        fcf_margin_pct = (fcf / revenue) * 100
        
        return cagr_pct + fcf_margin_pct
    
    def get_name(self) -> str:
        return "Rule of 40"
    
    def get_key(self) -> str:
        return "rule_of_40"


class RevenuePerEmployeeMetric(Metric):
    """
    Revenue per Employee = Total Revenue / Full-Time Employees

    Measures human capital efficiency and scalability.
    Most meaningful for:
    - Enterprise SaaS
    - Software platforms
    - Digital-first businesses

    Returned as $ thousands per employee.
    """

    def calculate(self, ticker: str, provider: StockDataProvider) -> Optional[float]:
        data = provider.get_employee_data(ticker) or {}

        revenue = data.get("revenue")
        employees = data.get("full_time_employees")

        # Missing → impute
        if revenue is None or employees is None:
            return None

        # Invalid → drop
        if revenue <= 0 or employees <= 0:
            return None

        # NaN handling
        if (
            isinstance(revenue, float) and math.isnan(revenue)
            or isinstance(employees, (int, float)) and math.isnan(employees)
        ):
            return None

        # Return in $ thousands per employee
        return (revenue / employees) / 1_000

    def get_name(self) -> str:
        return "Revenue per Employee ($K)"

    def get_key(self) -> str:
        return "revenue_per_employee"



class ARPUGrowthMetric(Metric):

    def __init__(self, years: int = 3):
        self.years = years

    def calculate(self, ticker: str, provider: StockDataProvider) -> Optional[float]:
        # Get time series data for revenue and user counts
        data = provider.get_user_metrics_data(ticker) or {}
        
        revenues = data.get("annual_revenues")  # List of annual revenues
        users = data.get("annual_active_users")  # List of annual user counts

        # Missing data → impute
        if revenues is None or users is None:
            return None

        # Insufficient time series data
        if len(revenues) < self.years + 1 or len(users) < self.years + 1:
            return None

        rev_start, rev_end = revenues[-(self.years + 1)], revenues[-1]
        users_start, users_end = users[-(self.years + 1)], users[-1]

        # Invalid → drop
        if (
            rev_start <= 0
            or rev_end <= 0
            or users_start <= 0
            or users_end <= 0
        ):
            return None

        # NaN handling
        if any(
            isinstance(x, float) and math.isnan(x)
            for x in [rev_start, rev_end, users_start, users_end]
        ):
            return None

        arpu_start = rev_start / users_start
        arpu_end = rev_end / users_end

        if arpu_start <= 0 or arpu_end <= 0:
            return None

        # Calculate CAGR and return as percentage
        cagr = ((arpu_end / arpu_start) ** (1 / self.years) - 1) 
        return cagr

    def get_name(self) -> str:
        return f"ARPU CAGR ({self.years}Y)"

    def get_key(self) -> str:
        return "arpu_cagr"


class IncrementalMarginMetric(Metric):

    def calculate(self, ticker: str, provider: StockDataProvider) -> Optional[float]:
        # Get time series data for revenue and operating income
        data = provider.get_incremental_margin_data(ticker) or {}
        
        revenue_current = data.get("revenue_current")
        revenue_prior = data.get("revenue_prior")
        op_income_current = data.get("operating_income_current")
        op_income_prior = data.get("operating_income_prior")
        
        # Missing data → impute
        if any(x is None for x in [revenue_current, revenue_prior, op_income_current, op_income_prior]):
            return None
        
        # NaN handling
        if any(
            isinstance(x, float) and math.isnan(x)
            for x in [revenue_current, revenue_prior, op_income_current, op_income_prior]
        ):
            return None
        
        # Calculate changes
        revenue_change = revenue_current - revenue_prior
        op_income_change = op_income_current - op_income_prior
        
        # Invalid → drop (need positive revenue growth to be meaningful)
        if revenue_change <= 0:
            return None
        
        # Calculate incremental margin
        incremental_margin = (op_income_change / revenue_change) 
        
        return incremental_margin
    
    def get_name(self) -> str:
        return "Incremental Margin"
    
    def get_key(self) -> str:
        return "incremental_margin"


# ============================================================================
# PRESET CONFIGURATIONS
# ============================================================================


def get_cloud_infrastructure_metrics() -> List[Metric]:
    # Low Revenue/CapEx, high CapEx intensity
    return [
        ROICMetric(),
        CapExIntensityMetric(),
        RevenuePerCapexMetric(),
        GrossMarginMetric(),
        OperatingMarginTrendMetric(),
    ]

def get_saas_metrics() -> List[Metric]:
    # High gross margins, R&D intensive
    return [
        RnDIntensityMetric(),
        GrossMarginMetric(),
        RuleOf40Metric(),
        RevenuePerEmployeeMetric(),
    ]

def get_ad_platform_metrics() -> List[Metric]:
    # User engagement, monetization efficiency
    return [
        ARPUGrowthMetric(),
        IncrementalMarginMetric(),
        RnDIntensityMetric(),
        CapExIntensityMetric()
    ]