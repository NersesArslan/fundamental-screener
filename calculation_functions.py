from typing import Optional, Dict, List
import pandas as pd
# ============================================================================
# CALCULATION LAYER - Pure functions, source-agnostic
# ============================================================================

def calculate_revenue_cagr_from_quarterly(quarterly_revenue: pd.Series, years: int = 5) -> Optional[float]:
    """
    Calculate revenue CAGR from quarterly OR annual data.
    Handles both quarterly and annual revenue series.
    
    Args:
        quarterly_revenue: Series of revenues (most recent first) - can be quarterly or annual
        years: Target years for CAGR calculation (will use all available data if less than target)
    
    Returns:
        CAGR as percentage, or None if insufficient data
    
    Note: Automatically falls back to whatever data is available (typically 3-4 years for most stocks)
    """
    if quarterly_revenue is None or len(quarterly_revenue) < 2:
        return None
    
    # Detect if this is annual or quarterly data by checking time gaps
    if len(quarterly_revenue) >= 2:
        avg_gap_days = (quarterly_revenue.index[0] - quarterly_revenue.index[-1]).days / (len(quarterly_revenue) - 1)
        is_annual = avg_gap_days > 200  # If average gap > 200 days, treat as annual
    else:
        is_annual = False
    
    if is_annual:
        # Annual data - simpler calculation
        if len(quarterly_revenue) < 2:
            return None
        
        # Use all available data
        ending_revenue = quarterly_revenue.iloc[0]
        beginning_revenue = quarterly_revenue.iloc[-1]
        actual_years = (quarterly_revenue.index[0] - quarterly_revenue.index[-1]).days / 365.25
        
        if beginning_revenue <= 0 or actual_years <= 0:
            return None
        
        cagr = (ending_revenue / beginning_revenue) ** (1 / actual_years) - 1
        return float(cagr * 100)
    else:
        # Quarterly data - need to group into years
        quarters_needed = (years * 4) + 1
        
        if len(quarterly_revenue) < quarters_needed:
            if len(quarterly_revenue) < 2:
                return None
            quarters_needed = len(quarterly_revenue)
        
        # Sum first 4 quarters (most recent year) and last 4 quarters (oldest year)
        ending_revenue = quarterly_revenue.iloc[:4].sum()
        beginning_revenue = quarterly_revenue.iloc[quarters_needed-4:quarters_needed].sum()
        
        # Calculate actual time span
        actual_years = (quarterly_revenue.index[0] - quarterly_revenue.index[quarters_needed-1]).days / 365.25
        
        if beginning_revenue <= 0 or actual_years <= 0:
            return None
        
        cagr = (ending_revenue / beginning_revenue) ** (1 / actual_years) - 1
        return float(cagr * 100)


def calculate_cagr_generic(values: pd.Series, years: int = 5) -> Optional[float]:
    """
    Generic CAGR calculator. Works for any time series.
    Supply price history, revenue, earnings, whatever.
    """
    if values is None or len(values) < 2:
        return None
    
    beginning = values.iloc[-1]  # Oldest
    ending = values.iloc[0]  # Most recent
    
    if beginning <= 0:
        return None
    
    # Time span from the data itself
    time_diff = (values.index[0] - values.index[-1]).days / 365.25
    actual_years = time_diff if time_diff > 0 else years
    
    cagr = (ending / beginning) ** (1 / actual_years) - 1
    return float(cagr * 100)