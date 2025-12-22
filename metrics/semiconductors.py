"""
Semiconductor Industry-Specific Metrics

These metrics are particularly important for evaluating semiconductor companies:
- CapEx Intensity: Capital-intensive manufacturing
- Inventory Turnover: Cycle management and demand signals
"""

from typing import List, Optional
from core_metrics import Metric
from core.stock_providers import StockDataProvider
from shared_metrics import (
    ROICMetric,
    CapExIntensityMetric,
    GrossMarginMetric
)
class InventoryTurnoverMetric(Metric):
    """
    Inventory Turnover = Cost of Revenue / Average Inventory
    
    Higher is better - shows how quickl
    y inventory moves.
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
