"""
Test stock screener configuration WITHOUT making API calls.
Quickly verify which metrics are loaded for each industry.
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.stock_providers import YFinanceProvider
from core.stock_screener import StockScreener

def test_metrics(industry=None):
    """Display which metrics are loaded for a given industry."""
    provider = YFinanceProvider()
    screener = StockScreener(provider, industry=industry)
    
    print(f"\n{'='*70}")
    print(f"METRICS FOR INDUSTRY: {industry or 'core only'}")
    print(f"{'='*70}\n")
    
    metric_names = screener.get_metric_names()
    
    print(f"Total metrics: {len(metric_names)}\n")
    
    for i, (key, name) in enumerate(metric_names.items(), 1):
        print(f"  {i:2d}. {name:30s} (key: {key})")
    
    print(f"\n{'='*70}\n")
    
    return metric_names

if __name__ == "__main__":
    # Test different industry configurations
    print("\n🔍 Testing Metric Configurations (No API Calls)\n")
    
    # Core only
    core_metrics = test_metrics(industry=None)
    
    # Semiconductors
    semis_metrics = test_metrics(industry='semis')
    
    # Tech
    tech_metrics = test_metrics(industry='tech')
    
    # Summary
    print("📊 SUMMARY:")
    print(f"  Core only:        {len(core_metrics)} metrics")
    print(f"  Semiconductors:   {len(semis_metrics)} metrics")
    print(f"  Tech:             {len(tech_metrics)} metrics")
