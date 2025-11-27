"""
Cross-validation module: Compare yfinance data against alternative sources.
This helps identify when yfinance data is inaccurate or stale.
"""
import yfinance as yf
import requests
import os
from datetime import datetime


def get_alpha_vantage_data(ticker, api_key=None):
    """
    Fetch data from Alpha Vantage API as alternative source.
    Free tier: 25 calls/day
    Get API key from: https://www.alphavantage.co/support/#api-key
    """
    if not api_key:
        api_key = os.environ.get('ALPHA_VANTAGE_API_KEY')
    
    if not api_key:
        return {'error': 'No API key provided. Set ALPHA_VANTAGE_API_KEY env var or pass api_key param'}
    
    # Get overview data
    url = f'https://www.alphavantage.co/query?function=OVERVIEW&symbol={ticker}&apikey={api_key}'
    
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        
        if 'Note' in data:
            return {'error': 'API rate limit reached'}
        
        if not data or 'Symbol' not in data:
            return {'error': f'No data found for {ticker}'}
        
        # Extract comparable metrics
        return {
            'source': 'Alpha Vantage',
            'ticker': ticker,
            'market_cap': float(data.get('MarketCapitalization', 0)) if data.get('MarketCapitalization') else None,
            'pe_ratio': float(data.get('PERatio', 0)) if data.get('PERatio') else None,
            'forward_pe': float(data.get('ForwardPE', 0)) if data.get('ForwardPE') else None,
            'trailing_eps': float(data.get('EPS', 0)) if data.get('EPS') else None,
            'book_value': float(data.get('BookValue', 0)) if data.get('BookValue') else None,
            'div_yield': float(data.get('DividendYield', 0)) if data.get('DividendYield') else None,
            'profit_margin': float(data.get('ProfitMargin', 0)) if data.get('ProfitMargin') else None,
        }
    except Exception as e:
        return {'error': str(e)}


def get_yfinance_data(ticker):
    """Fetch data from yfinance for comparison."""
    try:
        t = yf.Ticker(ticker)
        info = t.info
        
        return {
            'source': 'yfinance',
            'ticker': ticker,
            'market_cap': info.get('marketCap'),
            'pe_ratio': info.get('trailingPE'),
            'forward_pe': info.get('forwardPE'),
            'trailing_eps': info.get('trailingEps'),
            'book_value': info.get('bookValue'),
            'div_yield': info.get('dividendYield'),
            'profit_margin': info.get('profitMargins'),
        }
    except Exception as e:
        return {'error': str(e)}


def compare_sources(ticker, alpha_vantage_key=None, tolerance_pct=10):
    """
    Compare yfinance data against Alpha Vantage.
    
    Args:
        ticker: Stock symbol
        alpha_vantage_key: Optional API key (or use env var)
        tolerance_pct: Percentage difference threshold to flag (default 10%)
    
    Returns:
        Dictionary with comparison results and discrepancies
    """
    print(f"\n{'='*70}")
    print(f"Cross-Validation Report: {ticker}")
    print(f"{'='*70}")
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    # Fetch from both sources
    yf_data = get_yfinance_data(ticker)
    av_data = get_alpha_vantage_data(ticker, alpha_vantage_key)
    
    # Check for errors
    if 'error' in yf_data:
        print(f"❌ yfinance error: {yf_data['error']}")
        return {'status': 'error', 'yfinance': yf_data}
    
    if 'error' in av_data:
        print(f"⚠️  Alpha Vantage error: {av_data['error']}")
        print("    Skipping cross-validation (cannot compare sources)")
        return {'status': 'partial', 'yfinance': yf_data, 'alpha_vantage': av_data}
    
    # Compare metrics
    discrepancies = []
    metrics_compared = 0
    
    comparable_fields = ['pe_ratio', 'forward_pe', 'trailing_eps', 'book_value', 'div_yield', 'profit_margin']
    
    print(f"{'Metric':<20} {'yfinance':<20} {'Alpha Vantage':<20} {'Diff %':<10} {'Status'}")
    print("-" * 80)
    
    for field in comparable_fields:
        yf_val = yf_data.get(field)
        av_val = av_data.get(field)
        
        # Skip if either is None
        if yf_val is None or av_val is None:
            status = "⚠️  Missing"
            diff_pct = "-"
            print(f"{field:<20} {str(yf_val):<20} {str(av_val):<20} {diff_pct:<10} {status}")
            continue
        
        metrics_compared += 1
        
        # Calculate percentage difference
        if av_val != 0:
            diff_pct = abs((yf_val - av_val) / av_val) * 100
        else:
            diff_pct = 0 if yf_val == 0 else 100
        
        # Flag if difference exceeds tolerance
        if diff_pct > tolerance_pct:
            status = "❌ MISMATCH"
            discrepancies.append({
                'field': field,
                'yfinance': yf_val,
                'alpha_vantage': av_val,
                'diff_pct': diff_pct
            })
        else:
            status = "✓ Match"
        
        print(f"{field:<20} {yf_val:<20.4f} {av_val:<20.4f} {diff_pct:<10.2f} {status}")
    
    # Summary
    print("\n" + "="*70)
    if discrepancies:
        print(f"❌ VALIDATION FAILED: {len(discrepancies)} discrepanc{'y' if len(discrepancies) == 1 else 'ies'} found")
        print(f"   Review these fields - data may be stale or incorrect")
    else:
        print(f"✓ VALIDATION PASSED: All {metrics_compared} comparable metrics within {tolerance_pct}% tolerance")
    print("="*70)
    
    return {
        'status': 'complete',
        'ticker': ticker,
        'timestamp': datetime.now().isoformat(),
        'metrics_compared': metrics_compared,
        'discrepancies': discrepancies,
        'yfinance': yf_data,
        'alpha_vantage': av_data,
    }


if __name__ == '__main__':
    # Example usage
    print("\n" + "="*70)
    print("CROSS-VALIDATION TOOL")
    print("="*70)
    print("\nThis tool compares yfinance data against Alpha Vantage API")
    print("to detect inaccuracies or stale data.\n")
    print("To use:")
    print("1. Get free API key: https://www.alphavantage.co/support/#api-key")
    print("2. Set environment variable: export ALPHA_VANTAGE_API_KEY='your_key'")
    print("3. Run: python cross_validate.py")
    print("\nOr pass API key directly:")
    print("  compare_sources('AAPL', alpha_vantage_key='your_key')")
    print("="*70)
    
    # Try with environment variable
    result = compare_sources('AAPL')
