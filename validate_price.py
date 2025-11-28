#!/usr/bin/env python3
"""
Simple price validator - compares yfinance prices with alternative sources.
Start here to verify data accuracy one metric at a time.
"""

import yfinance as yf
import requests
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def get_yfinance_price(ticker):
    """Get current price from yfinance (what your screener uses)."""
    try:
        stock = yf.Ticker(ticker)
        price = stock.info.get('currentPrice')
        return price
    except Exception as e:
        print(f"  ❌ yfinance error: {e}")
        return None


def get_alphavantage_price(ticker, api_key=None):
    """Get current price from Alpha Vantage (alternative source)."""
    if not api_key:
        return None, "No API key provided"
    
    try:
        url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={ticker}&apikey={api_key}"
        response = requests.get(url, timeout=5)
        data = response.json()
        
        if "Global Quote" in data and "05. price" in data["Global Quote"]:
            return float(data["Global Quote"]["05. price"]), None
        else:
            return None, f"API response: {data.get('Note', data.get('Error Message', 'Unknown error'))}"
    except Exception as e:
        return None, str(e)


def get_polygon_price(ticker, api_key=None):
    """Get current price from Polygon.io/Massive.com (alternative source)."""
    if not api_key:
        return None, "No API key provided"
    
    try:
        # Use the previous close endpoint (free tier with 5 calls/min limit)
        url = f"https://api.polygon.io/v2/aggs/ticker/{ticker}/prev?adjusted=true&apiKey={api_key}"
        response = requests.get(url, timeout=5)
        data = response.json()
        
        # Check for errors
        if data.get('status') == 'ERROR':
            return None, f"API Error: {data.get('error', 'Unknown error')}"
        
        if data.get('status') != 'OK':
            return None, f"API returned status: {data.get('status')}"
        
        # Extract close price from results
        results = data.get('results')
        if results and len(results) > 0 and 'c' in results[0]:
            return float(results[0]['c']), None
        else:
            return None, f"No price data in response"
    except Exception as e:
        return None, str(e)


def validate_price(ticker, alpha_vantage_key=None, fmp_key=None):
    """Compare price from yfinance against alternative sources."""
    print(f"\n{'='*60}")
    print(f"Validating price for {ticker}")
    print(f"{'='*60}")
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    # Get yfinance price (your screener's source)
    yf_price = get_yfinance_price(ticker)
    print(f"📊 Your screener (yfinance): ${yf_price:.2f}" if yf_price else f"📊 Your screener (yfinance): Failed to fetch")
    
    if not yf_price:
        print("⚠️  Cannot validate - yfinance price unavailable")
        return
    
    prices = [yf_price]
    sources = ["yfinance"]
    
    # Try Alpha Vantage
    if alpha_vantage_key:
        av_price, av_error = get_alphavantage_price(ticker, alpha_vantage_key)
        if av_price:
            print(f"📈 Alpha Vantage:          ${av_price:.2f}")
            prices.append(av_price)
            sources.append("Alpha Vantage")
        else:
            print(f"📈 Alpha Vantage:          ❌ {av_error}")
    
    # Try Polygon.io
    if fmp_key:
        polygon_price, polygon_error = get_polygon_price(ticker, fmp_key)
        if polygon_price:
            print(f"💰 Polygon.io (Massive):    ${polygon_price:.2f}")
            prices.append(polygon_price)
            sources.append("Polygon")
        else:
            print(f"💰 Polygon.io (Massive):    ❌ {polygon_error}")
    
    # Analysis
    if len(prices) == 1:
        print(f"\n⚠️  Only one source available - cannot cross-validate")
        print(f"💡 Get free API keys:")
        print(f"   - Alpha Vantage: https://www.alphavantage.co/support/#api-key")
        print(f"   - Polygon.io: https://polygon.io/ (now Massive.com)")
    else:
        print(f"\n📊 Analysis:")
        avg_price = sum(prices) / len(prices)
        max_diff = max(prices) - min(prices)
        max_diff_pct = (max_diff / avg_price) * 100
        
        print(f"   Average price: ${avg_price:.2f}")
        print(f"   Price range: ${min(prices):.2f} - ${max(prices):.2f}")
        print(f"   Max difference: ${max_diff:.2f} ({max_diff_pct:.2f}%)")
        
        # Verdict
        if max_diff_pct < 0.5:
            print(f"\n✅ GOOD: Prices agree within 0.5% - your data looks accurate")
        elif max_diff_pct < 2.0:
            print(f"\n⚠️  ACCEPTABLE: Prices differ by {max_diff_pct:.2f}% - likely timing differences")
        else:
            print(f"\n❌ ISSUE: Prices differ by {max_diff_pct:.2f}% - investigate discrepancy")
        
        # Show individual differences
        print(f"\n   Difference from yfinance:")
        for i, (price, source) in enumerate(zip(prices[1:], sources[1:]), 1):
            diff = price - yf_price
            diff_pct = (diff / yf_price) * 100
            symbol = "📈" if diff > 0 else "📉" if diff < 0 else "➡️ "
            print(f"   {symbol} {source}: ${diff:+.2f} ({diff_pct:+.2f}%)")


if __name__ == "__main__":
    # Test with a few stocks
    tickers = ["AAPL", "MSFT", "GOOGL"]
    
    # Load API keys from environment variables
    ALPHA_VANTAGE_KEY = os.getenv('ALPHA_VANTAGE_KEY')
    POLYGON_KEY = os.getenv('POLYGON_KEY')
    
    print("\n" + "="*60)
    print("PRICE VALIDATION TEST")
    print("="*60)
    print("\n💡 For better validation, add API keys to this script:")
    print("   - Alpha Vantage (free, 25 calls/day)")
    print("   - Polygon.io/Massive (free, 5 calls/min)")
    
    for ticker in tickers:
        validate_price(ticker, ALPHA_VANTAGE_KEY, POLYGON_KEY)
    
    print(f"\n{'='*60}")
    print("MANUAL VERIFICATION")
    print(f"{'='*60}")
    print("\nCompare these prices manually with:")
    print("  • Google Finance: https://www.google.com/finance")
    print("  • Yahoo Finance: https://finance.yahoo.com")
    print("  • TradingView: https://www.tradingview.com")
    print("\nNote: Small differences (<2%) are normal due to:")
    print("  - Real-time vs delayed quotes")
    print("  - Pre/post-market trading")
    print("  - Different data providers")
