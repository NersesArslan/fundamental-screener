"""
Modular metrics system - easily add/remove metrics from screening.
Each metric is self-contained and knows how to calculate itself.
"""

from abc import ABC, abstractmethod
from typing import Optional
from stock_providers import StockDataProvider
from calculation_functions import calculate_revenue_cagr_from_quarterly


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
# METRIC IMPLEMENTATIONS
# ============================================================================

class PriceMetric(Metric):
    """Current stock price."""
    
    def calculate(self, ticker: str, provider: StockDataProvider) -> Optional[float]:
        return provider.get_price(ticker)
    
    def get_name(self) -> str:
        return "Price"
    
    def get_key(self) -> str:
        return "price"


class PERatioMetric(Metric):
    """Price-to-Earnings ratio."""
    
    def calculate(self, ticker: str, provider: StockDataProvider) -> Optional[float]:
        fundamentals = provider.get_fundamentals(ticker)
        return fundamentals['pe_ratio']
    
    def get_name(self) -> str:
        return "P/E Ratio"
    
    def get_key(self) -> str:
        return "pe_ratio"


class DebtToEquityMetric(Metric):
    """Debt-to-Equity ratio."""
    
    def calculate(self, ticker: str, provider: StockDataProvider) -> Optional[float]:
        fundamentals = provider.get_fundamentals(ticker)
        return fundamentals['debt_to_equity']
    
    def get_name(self) -> str:
        return "Debt/Equity"
    
    def get_key(self) -> str:
        return "debt_to_equity"


class RevenueCagr3YearMetric(Metric):
    """3-Year Revenue CAGR (Compound Annual Growth Rate)."""
    
    def calculate(self, ticker: str, provider: StockDataProvider) -> Optional[float]:
        revenue_data = provider.get_quarterly_revenue(ticker)
        return calculate_revenue_cagr_from_quarterly(revenue_data, years=3)
    
    def get_name(self) -> str:
        return "3Y CAGR"
    
    def get_key(self) -> str:
        return "3_year_cagr"


class RevenueCagr5YearMetric(Metric):
    """5-Year Revenue CAGR (Compound Annual Growth Rate)."""
    
    def calculate(self, ticker: str, provider: StockDataProvider) -> Optional[float]:
        revenue_data = provider.get_quarterly_revenue(ticker)
        return calculate_revenue_cagr_from_quarterly(revenue_data, years=3)
    
    def get_name(self) -> str:
        return "3Y CAGR"
    
    def get_key(self) -> str:
        return "3_year_cagr"


class ROEMetric(Metric):
    """Return on Equity."""
    
    def calculate(self, ticker: str, provider: StockDataProvider) -> Optional[float]:
        fundamentals = provider.get_fundamentals(ticker)
        return fundamentals['return_on_equity']
    
    def get_name(self) -> str:
        return "ROE"
    
    def get_key(self) -> str:
        return "returnonequity"


class FreeCashFlowMetric(Metric):
    """Free Cash Flow (TTM)."""
    
    def calculate(self, ticker: str, provider: StockDataProvider) -> Optional[float]:
        fundamentals = provider.get_fundamentals(ticker)
        return fundamentals['free_cashflow']
    
    def get_name(self) -> str:
        return "Free Cash Flow"
    
    def get_key(self) -> str:
        return "free_cashflow"


# ============================================================================
# DEFAULT METRIC SETS - Pre-configured collections
# ============================================================================

def get_default_metrics():
    """Standard set of metrics for value/growth screening."""
    return [
        PriceMetric(),
        PERatioMetric(),
        DebtToEquityMetric(),
        RevenueCagr3YearMetric(),  # Using 3-year since yfinance has limited data
        ROEMetric(),
        FreeCashFlowMetric(),
    ]


def get_growth_metrics():
    """Focused on growth metrics."""
    return [
        PriceMetric(),
        RevenueCagr3YearMetric(),
        RevenueCagr5YearMetric(),
        ROEMetric(),
    ]


def get_value_metrics():
    """Focused on value metrics."""
    return [
        PriceMetric(),
        PERatioMetric(),
        DebtToEquityMetric(),
        FreeCashFlowMetric(),
    ]
