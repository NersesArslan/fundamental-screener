"""
Semiconductor Industry-Specific Metrics

These metrics are particularly important for evaluating semiconductor companies:
- CapEx Intensity: Capital-intensive manufacturing
- Inventory Turnover: Cycle management and demand signals
"""

from typing import List, Optional
from metrics.core import Metric
from stock_providers import StockDataProvider


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
        CapExIntensityMetric(),
        InventoryTurnoverMetric(),
        GrossMarginMetric(),
    ]
