"""
Core Universal Metrics - Work across all industries

These 6 metrics are carefully chosen to be universally applicable:
1. EV/FCF - Enterprise Value / Free Cash Flow
2. Revenue CAGR - 3-5 year growth trajectory
3. Operating Margin - Operating efficiency
4. FCF Margin - Cash generation efficiency
5. Net Debt/EBITDA - Leverage (handles negative book equity better)
6. Interest Coverage - Debt servicing ability
"""

from abc import ABC, abstractmethod
from typing import Optional, List, Dict
from core.stock_providers import StockDataProvider


class Metric(ABC):
    """Base class for all metrics. Each metric knows how to calculate itself."""
    
    @abstractmethod
    def calculate(self, ticker: str, provider: StockDataProvider) -> Optional[float]:
        """Calculate this metric for a given ticker."""
        pass
    
    @abstractmethod
    def get_name(self) -> str:
        """Return the display name for this metric."""
        pass
    
    @abstractmethod
    def get_key(self) -> str:
        """Return the key used in results dict."""
        pass

    def is_not_applicable(self, value, ticker_data: Dict) -> bool:
        """Default: metric is always applicable unless overridden."""
        return False

# ============================================================================
# CORE UNIVERSAL METRICS (7 metrics)
# ============================================================================

class EVToFCFMetric(Metric):
    """
    Enterprise Value / Free Cash Flow
    Lower is better - shows how expensive the company is relative to cash generation.
    
    SMART FALLBACK: If FCF is negative/zero (cash burning), return 9999 as a penalty
    value. This ensures the stock gets scored (rather than excluded) but receives
    the worst possible score for this metric.
    """
    
    def calculate(self, ticker: str, provider: StockDataProvider) -> Optional[float]:
        data = provider.get_valuation_data(ticker)
        if data['enterprise_value'] and data['free_cashflow'] is not None:
            if data['free_cashflow'] > 0:
                return data['enterprise_value'] / data['free_cashflow']
            else:
                # Negative/zero FCF = cash burning = worst possible score
                return 100
        return None
    
    def get_name(self) -> str:
        return "EV/FCF"
    
    def get_key(self) -> str:
        return "ev_to_fcf"

class RevenueCagrMetric(Metric):
    """
    Revenue Compound Annual Growth Rate (3-5 years)
    Shows consistent growth trajectory.
    """
    
    def calculate(self, ticker: str, provider: StockDataProvider) -> Optional[float]:
        # Reuse existing calculation function
        from calculation_functions import calculate_revenue_cagr_from_quarterly
        quarterly_revenue = provider.get_quarterly_revenue(ticker)
        if quarterly_revenue is not None:
            return calculate_revenue_cagr_from_quarterly(quarterly_revenue)
        return None
    
    def get_name(self) -> str:
        return "Revenue CAGR"
    
    def get_key(self) -> str:
        return "revenue_cagr"


class OperatingMarginMetric(Metric):
    """
    Operating Margin = Operating Income / Revenue
    Shows operational efficiency before financing costs.
    """
    
    def calculate(self, ticker: str, provider: StockDataProvider) -> Optional[float]:
        data = provider.get_margin_data(ticker)
        if data['operating_income'] and data['revenue']:
            if data['revenue'] > 0:
                return (data['operating_income'] / data['revenue']) * 100
        return None
    
    def get_name(self) -> str:
        return "Operating Margin"
    
    def get_key(self) -> str:
        return "operating_margin"


class FCFMarginMetric(Metric):
    """
    FCF Margin = Free Cash Flow / Revenue
    Shows how much cash the company generates per dollar of revenue.
    """
    
    def calculate(self, ticker: str, provider: StockDataProvider) -> Optional[float]:
        data = provider.get_margin_data(ticker)
        if data['free_cashflow'] and data['revenue']:
            if data['revenue'] > 0:
                return (data['free_cashflow'] / data['revenue']) * 100
        return None
    
    def get_name(self) -> str:
        return "FCF Margin"
    
    def get_key(self) -> str:
        return "fcf_margin"


class NetDebtToEBITDAMetric(Metric):
    """
    Net Debt / EBITDA
    Better leverage metric than Debt/Equity (handles negative book equity).
    Net Debt = Total Debt - Cash
    Lower is better (less levered).
    """
    
    def calculate(self, ticker: str, provider: StockDataProvider) -> Optional[float]:
        data = provider.get_leverage_data(ticker)
        
        total_debt = data.get('total_debt')
        cash = data.get('cash')
        ebitda = data.get('ebitda')
        
        if all(x is not None for x in [total_debt, cash, ebitda]):
            net_debt = total_debt - cash
            if ebitda > 0:
                return net_debt / ebitda
        
        return None
    
    def get_name(self) -> str:
        return "Net Debt/EBITDA"
    
    def get_key(self) -> str:
        return "net_debt_to_ebitda"


class InterestCoverageMetric(Metric):
    """
    Interest Coverage = EBIT / Interest Expense
    Measures ability to service debt.
    Higher is better (more cushion to pay interest).
    
    Special handling per Hal's framework:
    - Returns NaN if leverage is negligible (Debt/EBITDA < 0.5) → Case 1: N/A, redistribute weight
    - Returns None if data is missing but leverage exists → Case 2: Missing data, impute median
    """
    
    def is_not_applicable(self, value, ticker, provider):
        """
        Case 1: Interest Coverage is N/A when company has negligible leverage.
        Uses Debt/EBITDA < 0.5 threshold (Hal's suggestion).
        """
        import math
        
        # Check if value is NaN (signals N/A from calculate())
        if value is not None and math.isnan(value):
            return True
        
        return False
    
    def calculate(self, ticker: str, provider: StockDataProvider) -> Optional[float]:
        import math
        
        data = provider.get_leverage_data(ticker)
        
        ebit = data.get('ebit')
        interest_expense = data.get('interest_expense')
        total_debt = data.get('total_debt')
        ebitda = data.get('ebitda')
        
        # Case 1: Check if leverage is negligible (Debt/EBITDA < 0.5)
        # If so, Interest Coverage is not a meaningful metric → return NaN
        if total_debt is not None and ebitda is not None and ebitda > 0:
            debt_to_ebitda = total_debt / ebitda
            if debt_to_ebitda < 0.5:
                return float('nan')  # N/A - redistribute weight
        
        # Case 2: Has meaningful debt but interest expense data is missing/invalid
        if ebit is not None:
            if interest_expense is None or math.isnan(interest_expense):
                # Company has leverage but data is missing → return None for median imputation
                return None
            
            # Normal case: calculate interest coverage
            if interest_expense > 0:
                return ebit / interest_expense
            else:
                # Interest expense is zero but debt exists → check leverage again
                if total_debt is not None and ebitda is not None and ebitda > 0:
                    if (total_debt / ebitda) < 0.5:
                        return float('nan')  # Negligible leverage
                return None  # Data issue
        
        # EBIT missing - can't calculate
        return None
    
    def get_name(self) -> str:
        return "Interest Coverage"
    
    def get_key(self) -> str:
        return "interest_coverage"


# ============================================================================
# PRESET CONFIGURATIONS
# ============================================================================

def get_core_metrics() -> List[Metric]:
    """
    Returns all 6 core universal metrics.
    Use this as the foundation for any industry screening.
    """
    return [
        EVToFCFMetric(),
        RevenueCagrMetric(),
        OperatingMarginMetric(),
        FCFMarginMetric(),
        NetDebtToEBITDAMetric(),
        InterestCoverageMetric(),
    ]
