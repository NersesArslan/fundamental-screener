from typing import Optional, Dict, List
import pandas as pd

# ============================================================================
# PRESENTATION LAYER - Format output prettily
# ============================================================================

def format_screener_output(results: Dict[str, Dict], metric_names: Dict[str, str] = None) -> pd.DataFrame:
    """
    Transform raw metrics into a beautiful table.
    
    Args:
        results: Dict of {ticker: {metric_key: value}}
        metric_names: Optional dict of {metric_key: display_name}
    """
    df = pd.DataFrame(results).T
    df.index.name = 'Ticker'
    
    # Format columns based on type
    for col in df.columns:
        if col == 'price':
            df[col] = df[col].apply(lambda x: f"${x:.2f}" if pd.notna(x) else None)
        elif col == 'pe_ratio':
            df[col] = df[col].apply(lambda x: f"{x:.2f}" if pd.notna(x) else None)
        elif col == 'debt_to_equity':
            df[col] = df[col].apply(lambda x: f"{x:.2f}" if pd.notna(x) else None)
        elif 'cagr' in col:
            df[col] = df[col].apply(lambda x: f"{x:.2f}%" if pd.notna(x) else None)
        elif col == 'returnonequity':
            df[col] = df[col].apply(lambda x: f"{x:.2%}" if pd.notna(x) else None)
        elif col == 'free_cashflow':
            df[col] = df[col].apply(lambda x: f"${x:,.0f}" if pd.notna(x) else None)
    
    # Rename columns to display names if provided
    if metric_names:
        df.columns = [metric_names.get(col, col) for col in df.columns]
    
    return df