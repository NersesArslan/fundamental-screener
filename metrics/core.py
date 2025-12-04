"""
Core Universal Metrics - Work across all industries

These 7 metrics are carefully chosen to be universally applicable:
1. EV/FCF - Enterprise Value / Free Cash Flow
2. ROIC - Return on Invested Capital (bypasses buyback distortions)
3. Revenue CAGR - 3-5 year growth rate
4. Operating Margin - Operating efficiency
5. FCF Margin - Cash generation efficiency
6. Net Debt/EBITDA - Leverage (handles negative book equity better)
7. Interest Coverage - Debt servicing ability
"""

from abc import ABC, abstractmethod
from typing import Optional, List
from stock_providers import StockDataProvider


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


# ============================================================================
# CORE UNIVERSAL METRICS (7 metrics)
# ============================================================================

class EVToFCFMetric(Metric):
    """
    Enterprise Value / Free Cash Flow
    Lower is better - shows how expensive the company is relative to cash generation.
    """
    
    def calculate(self, ticker: str, provider: StockDataProvider) -> Optional[float]:
        data = provider.get_valuation_data(ticker)
        if data['enterprise_value'] and data['free_cashflow']:
            if data['free_cashflow'] > 0:
                return data['enterprise_value'] / data['free_cashflow']
        return None
    
    def get_name(self) -> str:
        return "EV/FCF"
    
    def get_key(self) -> str:
        return "ev_to_fcf"


class ROICMetric(Metric):
    """
    Return on Invested Capital = NOPAT / Invested Capital
    Superior to ROE because it's not distorted by buybacks.
    Formula: (Operating Income * (1 - Tax Rate)) / (Total Debt + Total Equity - Cash)
    """
    
    def calculate(self, ticker: str, provider: StockDataProvider) -> Optional[float]:
        data = provider.get_roic_components(ticker)
        
        operating_income = data.get('operating_income')
        tax_rate = data.get('tax_rate')
        total_debt = data.get('total_debt')
        total_equity = data.get('total_equity')
        cash = data.get('cash')
        
        if all(x is not None for x in [operating_income, tax_rate, total_debt, total_equity, cash]):
            # NOPAT = Operating Income * (1 - Tax Rate)
            nopat = operating_income * (1 - tax_rate)
            
            # Invested Capital = Total Debt + Total Equity - Cash
            invested_capital = total_debt + total_equity - cash
            
            if invested_capital > 0:
                return (nopat / invested_capital) * 100  # Return as percentage
        
        return None
    
    def get_name(self) -> str:
        return "ROIC"
    
    def get_key(self) -> str:
        return "roic"


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
    """
    
    def calculate(self, ticker: str, provider: StockDataProvider) -> Optional[float]:
        data = provider.get_leverage_data(ticker)
        
        ebit = data.get('ebit')
        interest_expense = data.get('interest_expense')
        
        if ebit and interest_expense:
            if interest_expense > 0:
                return ebit / interest_expense
        
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
    Returns all 7 core universal metrics.
    Use this as the foundation for any industry screening.
    """
    return [
        EVToFCFMetric(),
        ROICMetric(),
        RevenueCagrMetric(),
        OperatingMarginMetric(),
        FCFMarginMetric(),
        NetDebtToEBITDAMetric(),
        InterestCoverageMetric(),
    ]
