"""
Big Tech Industry-Specific Metrics

These metrics are particularly relevant for large technology companies:
- R&D Intensity: Innovation investment
- Net Debt/FCF: Alternative leverage metric for cash-rich tech
"""

from typing import List, Optional
from metrics.core import Metric
from stock_providers import StockDataProvider


class RnDIntensityMetric(Metric):
    """
    R&D Intensity = R&D Expense / Revenue
    
    Shows commitment to innovation. Higher is typical for tech,
    especially in competitive markets.
    """
    
    def calculate(self, ticker: str, provider: StockDataProvider) -> Optional[float]:
        data = provider.get_rnd_data(ticker)
        
        rnd_expense = data.get('research_development')
        revenue = data.get('revenue')
        
        if rnd_expense and revenue and revenue > 0:
            return (rnd_expense / revenue) * 100
        
        return None
    
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


# ============================================================================
# PRESET CONFIGURATIONS
# ============================================================================

def get_tech_metrics() -> List[Metric]:
    """
    Returns big tech-specific metrics.
    Use with core metrics: get_core_metrics() + get_tech_metrics()
    """
    return [
        RnDIntensityMetric(),
        NetDebtToFCFMetric(),
    ]
