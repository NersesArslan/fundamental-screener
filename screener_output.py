from typing import Optional, Dict, List
import pandas as pd

# ============================================================================
# PRESENTATION LAYER - Format output prettily
# ============================================================================

def format_screener_output(results: Dict[str, Dict]) -> pd.DataFrame:
    """Transform raw metrics into a beautiful table."""
    df = pd.DataFrame(results).T
    df.index.name = 'Ticker'
    
    # Format columns for human consumption
    df['price'] = df['price'].apply(lambda x: f"${x:.2f}" if x else None)
    df['pe_ratio'] = df['pe_ratio'].apply(lambda x: f"{x:.2f}" if x else None)
    df['debt_to_equity'] = df['debt_to_equity'].apply(lambda x: f"{x:.2f}%" if x else None)
    df['5_year_cagr'] = df['5_year_cagr'].apply(lambda x: f"{x:.2f}%" if x else None)
    df['returnonequity'] = df['returnonequity'].apply(lambda x: f"{x:.2%}" if x else None)
    df['free_cashflow'] = df['free_cashflow'].apply(lambda x: f"${x:,.0f}" if x else None)
    
    # Readable column names
    df.columns = ['Price', 'P/E Ratio', 'Debt/Equity', '3Y CAGR', 'ROE', 'Free Cash Flow (TTM)']
    
    return df