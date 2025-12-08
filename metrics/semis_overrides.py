"""
Semiconductor Industry-Specific Metrics

These metrics are particularly important for evaluating semiconductor companies:
- CapEx Intensity: Capital-intensive manufacturing
- Inventory Turnover: Cycle management and demand signals
"""

from typing import List, Optional
from metrics.core import Metric
from core.stock_providers import StockDataProvider

class ROICMetric(Metric):
    """
    Return on Invested Capital = NOPAT / Invested Capital
    Superior to ROE because it's not distorted by buybacks.
    Formula: (Operating Income * (1 - Tax Rate)) / (Total Debt + Total Equity - Cash)
    
    Special handling:
    - Returns None if data is missing (will be imputed with peer median)
    - Returns float('nan') if invested capital <= 0 (metric not applicable, excluded from scoring)
    """
    
    def calculate(self, ticker: str, provider: StockDataProvider) -> Optional[float]:
        data = provider.get_roic_components(ticker)
        
        operating_income = data.get('operating_income')
        tax_rate = data.get('tax_rate')
        total_debt = data.get('total_debt')
        total_equity = data.get('total_equity')
        cash = data.get('cash')

        if not all(x is not None for x in [operating_income, tax_rate, total_debt, total_equity, cash]):
            return None

        nopat = operating_income * (1 - tax_rate)
        invested_capital = total_debt + total_equity - cash

        # Store helper values into the object
        self.last_invested_capital = invested_capital

        if invested_capital > 0:
            return (nopat / invested_capital) * 100
        else:
            # negative invested capital → NA, not “missing”
            return float('nan')

    
    def get_name(self) -> str:
        return "ROIC"
    
    def get_key(self) -> str:
        return "roic"
    

    def is_not_applicable(self, value, ticker_data):
        invested = ticker_data.get("invested_capital")
        return invested is not None and invested <= 0
    
class CapExIntensityMetric(Metric):
    """
    CapEx Intensity = Capital Expenditures / Revenue
    
    Semiconductors are capital-intensive. This shows how much revenue 
    reinvestment is required. Lower can be better (more efficient),
    but too low may indicate underinvestment.
    """
    
    def calculate(self, ticker: str, provider: StockDataProvider) -> Optional[float]:
        data = provider.get_capex_data(ticker)
        
        capex = data.get('capital_expenditure')
        revenue = data.get('revenue')
        
        if capex and revenue and revenue > 0:
            # Return as percentage (make positive for display)
            return abs(capex / revenue) * 100
        
        return None
    
    def get_name(self) -> str:
        return "CapEx Intensity"
    
    def get_key(self) -> str:
        return "capex_intensity"


class InventoryTurnoverMetric(Metric):
    """
    Inventory Turnover = Cost of Revenue / Average Inventory
    
    Higher is better - shows how quickly inventory moves.
    Important for semis: low turnover can signal demand weakness.
    """
    
    def calculate(self, ticker: str, provider: StockDataProvider) -> Optional[float]:
        data = provider.get_inventory_data(ticker)
        
        cost_of_revenue = data.get('cost_of_revenue')
        inventory = data.get('inventory')
        
        if cost_of_revenue and inventory and inventory > 0:
            return cost_of_revenue / inventory
        
        return None
    
    def get_name(self) -> str:
        return "Inventory Turnover"
    
    def get_key(self) -> str:
        return "inventory_turnover"


class GrossMarginMetric(Metric):
    """
    Gross Margin = (Revenue - Cost of Revenue) / Revenue
    
    Critical for semis - shows pricing power and manufacturing efficiency.
    High margins indicate technological moats.
    """
    
    def calculate(self, ticker: str, provider: StockDataProvider) -> Optional[float]:
        data = provider.get_margin_data(ticker)
        
        revenue = data.get('revenue')
        cost_of_revenue = data.get('cost_of_revenue')
        
        if revenue and cost_of_revenue and revenue > 0:
            gross_profit = revenue - cost_of_revenue
            return (gross_profit / revenue) * 100
        
        return None
    
    def get_name(self) -> str:
        return "Gross Margin"
    
    def get_key(self) -> str:
        return "gross_margin"


# ============================================================================
# PRESET CONFIGURATIONS
# ============================================================================

def get_semis_metrics() -> List[Metric]:
    """
    Returns semiconductor-specific metrics.
    Use with core metrics: get_core_metrics() + get_semis_metrics()
    """
    return [
        ROICMetric(),
        CapExIntensityMetric(),
        InventoryTurnoverMetric(),
        GrossMarginMetric(),
    ]
