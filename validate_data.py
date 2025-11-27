"""
Data validation module for stock screener.
Compares fetched data against known reference values and manual checks.
"""
import yfinance as yf
import pandas as pd
from datetime import datetime


def validate_single_stock(ticker_symbol, reference_data=None):
    """
    Validate data for a single stock against reference values.
    
    Args:
        ticker_symbol: Stock ticker (e.g., 'AAPL')
        reference_data: Optional dict with reference values to compare against
                       e.g., {'price': 275.50, 'pe_ratio': 37.0, ...}
    
    Returns:
        Dictionary with validation results and discrepancies
    """
    ticker = yf.Ticker(ticker_symbol)
    info = ticker.info
    
    # Fetch raw data
    raw_data = {
        'ticker': ticker_symbol,
        'price': info.get('currentPrice'),
        'pe_ratio': info.get('trailingPE'),
        'forward_pe': info.get('forwardPE'),
        'debt_to_equity': info.get('debtToEquity'),
        'return_on_equity': info.get('returnOnEquity'),
        'free_cashflow': info.get('freeCashflow'),
        'market_cap': info.get('marketCap'),
        'trailing_eps': info.get('trailingEps'),
        'forward_eps': info.get('forwardEps'),
    }
    
    # Data quality checks
    issues = []
    
    # Check for None values
    none_fields = [k for k, v in raw_data.items() if v is None and k != 'ticker']
    if none_fields:
        issues.append(f"Missing data: {', '.join(none_fields)}")
    
    # Check PE ratio consistency
    if raw_data['price'] and raw_data['trailing_eps']:
        calculated_pe = raw_data['price'] / raw_data['trailing_eps']
        reported_pe = raw_data['pe_ratio']
        if reported_pe and abs(calculated_pe - reported_pe) > 0.5:
            issues.append(f"P/E mismatch: calculated={calculated_pe:.2f}, reported={reported_pe:.2f}")
    
    # Check negative values where they shouldn't be
    if raw_data['price'] and raw_data['price'] < 0:
        issues.append("Price is negative")
    if raw_data['free_cashflow'] and raw_data['free_cashflow'] < -1e12:  # Allow some negative FCF
        issues.append(f"Free cash flow unusually negative: {raw_data['free_cashflow']:,.0f}")
    
    # Compare with reference data if provided
    discrepancies = []
    if reference_data:
        for key, ref_value in reference_data.items():
            actual_value = raw_data.get(key)
            if actual_value is not None and ref_value is not None:
                # Calculate percentage difference
                if ref_value != 0:
                    pct_diff = abs((actual_value - ref_value) / ref_value) * 100
                    if pct_diff > 5:  # Flag if >5% different
                        discrepancies.append({
                            'field': key,
                            'reference': ref_value,
                            'actual': actual_value,
                            'diff_pct': pct_diff
                        })
    
    return {
        'ticker': ticker_symbol,
        'timestamp': datetime.now().isoformat(),
        'raw_data': raw_data,
        'issues': issues,
        'discrepancies': discrepancies,
        'data_source': 'yfinance',
    }


def validate_batch(tickers, reference_data_dict=None):
    """
    Validate multiple stocks and generate a report.
    
    Args:
        tickers: List of ticker symbols
        reference_data_dict: Optional dict mapping ticker -> reference data
                            e.g., {'AAPL': {'price': 275.50, ...}, ...}
    
    Returns:
        DataFrame with validation summary
    """
    results = []
    
    for ticker in tickers:
        ref_data = reference_data_dict.get(ticker) if reference_data_dict else None
        validation = validate_single_stock(ticker, ref_data)
        
        results.append({
            'Ticker': ticker,
            'Has Issues': len(validation['issues']) > 0,
            'Issue Count': len(validation['issues']),
            'Issues': '; '.join(validation['issues']) if validation['issues'] else 'None',
            'Discrepancy Count': len(validation['discrepancies']),
            'Price': validation['raw_data']['price'],
            'P/E': validation['raw_data']['pe_ratio'],
        })
    
    return pd.DataFrame(results)


def print_detailed_validation(ticker_symbol, reference_data=None):
    """Print detailed validation report for a single stock."""
    result = validate_single_stock(ticker_symbol, reference_data)
    
    print(f"\n{'='*70}")
    print(f"VALIDATION REPORT: {ticker_symbol}")
    print(f"Timestamp: {result['timestamp']}")
    print(f"Data Source: {result['data_source']}")
    print(f"{'='*70}\n")
    
    print("RAW DATA:")
    for key, value in result['raw_data'].items():
        if key != 'ticker':
            if isinstance(value, float) and value > 1000:
                print(f"  {key:20s}: {value:,.2f}")
            elif isinstance(value, float):
                print(f"  {key:20s}: {value:.4f}")
            else:
                print(f"  {key:20s}: {value}")
    
    print(f"\nISSUES FOUND: {len(result['issues'])}")
    for issue in result['issues']:
        print(f"  ⚠ {issue}")
    
    if result['discrepancies']:
        print(f"\nDISCREPANCIES (vs reference): {len(result['discrepancies'])}")
        for disc in result['discrepancies']:
            print(f"  • {disc['field']}: ref={disc['reference']:.2f}, actual={disc['actual']:.2f} ({disc['diff_pct']:.1f}% diff)")
    
    print(f"\n{'='*70}\n")


if __name__ == "__main__":
    # Example: Validate AAPL with manual reference data
    # (Get reference values from Yahoo Finance, Google Finance, or Bloomberg)
    reference = {
        'price': 275.92,  # Check against current market price
        'pe_ratio': 37.04,
        'market_cap': 4.2e12,  # $4.2 trillion
    }
    
    print("Single Stock Detailed Validation:")
    print_detailed_validation('AAPL', reference)
    
    # Batch validation
    print("\nBatch Validation (Semiconductor stocks):")
    semis = ['NVDA', 'AMD', 'INTC', 'TSM', 'ASML']
    summary = validate_batch(semis)
    print(summary.to_string(index=False))
