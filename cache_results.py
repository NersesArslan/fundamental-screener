"""
Cache stock screening results to avoid repeated API calls during testing.

Usage:
    # Save results once
    python cache_results.py --save

    # Load cached results in main.py
    from cache_results import load_cached_results
    stocks_data = load_cached_results()
"""

import json
import argparse
from stock_providers import YFinanceProvider
from stock_screener import StockScreener

CACHE_FILE = "cached_screening_results.json"

def save_results(tickers, industry='semis'):
    """Fetch and save screening results."""
    provider = YFinanceProvider()
    screener = StockScreener(provider, industry=industry)
    
    print(f"Fetching data for {len(tickers)} tickers (industry={industry})...")
    stocks_data = screener.screen_multiple(tickers, parallel=True, max_workers=5)
    
    # Convert to serializable format (handle NaN, None)
    serializable_data = {}
    for ticker, metrics in stocks_data.items():
        serializable_data[ticker] = {}
        for key, value in metrics.items():
            if value is None:
                serializable_data[ticker][key] = None
            elif isinstance(value, float):
                import math
                if math.isnan(value):
                    serializable_data[ticker][key] = "NaN"
                elif math.isinf(value):
                    serializable_data[ticker][key] = "Inf"
                else:
                    serializable_data[ticker][key] = value
            else:
                serializable_data[ticker][key] = value
    
    with open(CACHE_FILE, 'w') as f:
        json.dump(serializable_data, f, indent=2)
    
    print(f"✅ Saved {len(tickers)} stocks to {CACHE_FILE}")
    return serializable_data

def load_cached_results():
    """Load cached screening results."""
    import math
    
    with open(CACHE_FILE, 'r') as f:
        data = json.load(f)
    
    # Convert special strings back to Python types
    for ticker in data:
        for key in data[ticker]:
            if data[ticker][key] == "NaN":
                data[ticker][key] = float('nan')
            elif data[ticker][key] == "Inf":
                data[ticker][key] = float('inf')
    
    return data

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--save', action='store_true', help='Fetch and save results')
    parser.add_argument('--industry', default='semis', help='Industry type (semis, tech, etc.)')
    parser.add_argument('--tickers', nargs='+', help='Ticker list (default: NVDA AMD INTC)')
    args = parser.parse_args()
    
    if args.save:
        if args.tickers:
            tickers = args.tickers
        else:
            # Default: small semis test set
            tickers = ['NVDA', 'AMD', 'INTC']
        
        save_results(tickers, industry=args.industry)
    else:
        # Load and display
        data = load_cached_results()
        print(f"Loaded {len(data)} cached stocks")
        for ticker, metrics in list(data.items())[:3]:
            print(f"\n{ticker}: {list(metrics.keys())}")
