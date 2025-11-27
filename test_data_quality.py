"""
Automated test suite for stock screener data accuracy.
Run this regularly to catch data quality issues.
"""
import yfinance as yf
from validate_data import validate_single_stock, validate_batch


def test_data_completeness():
    """Test that all expected fields are populated."""
    print("\n" + "="*70)
    print("TEST: Data Completeness")
    print("="*70)
    
    test_tickers = ['AAPL', 'MSFT', 'GOOGL']
    required_fields = ['price', 'pe_ratio', 'market_cap', 'trailing_eps']
    
    failures = []
    for ticker in test_tickers:
        validation = validate_single_stock(ticker)
        raw = validation['raw_data']
        
        missing = [f for f in required_fields if raw.get(f) is None]
        if missing:
            failures.append(f"{ticker}: missing {missing}")
            print(f"  ❌ {ticker}: Missing fields: {missing}")
        else:
            print(f"  ✓ {ticker}: All required fields present")
    
    if failures:
        print(f"\n❌ FAILED: {len(failures)} ticker(s) have missing data")
        return False
    else:
        print(f"\n✓ PASSED: All tickers have complete data")
        return True


def test_pe_ratio_consistency():
    """Test that P/E ratios are consistent with price/EPS."""
    print("\n" + "="*70)
    print("TEST: P/E Ratio Consistency")
    print("="*70)
    
    test_tickers = ['AAPL', 'MSFT', 'GOOGL', 'NVDA']
    
    failures = []
    for ticker in test_tickers:
        validation = validate_single_stock(ticker)
        raw = validation['raw_data']
        
        if raw['price'] and raw['trailing_eps'] and raw['pe_ratio']:
            calculated = raw['price'] / raw['trailing_eps']
            reported = raw['pe_ratio']
            diff = abs(calculated - reported)
            
            if diff > 0.5:
                failures.append(f"{ticker}: calc={calculated:.2f}, reported={reported:.2f}")
                print(f"  ❌ {ticker}: P/E mismatch (calc={calculated:.2f}, reported={reported:.2f})")
            else:
                print(f"  ✓ {ticker}: P/E consistent (calc={calculated:.2f}, reported={reported:.2f})")
        else:
            print(f"  ⚠ {ticker}: Skipped (missing data)")
    
    if failures:
        print(f"\n❌ FAILED: {len(failures)} ticker(s) have P/E inconsistencies")
        return False
    else:
        print(f"\n✓ PASSED: All P/E ratios are consistent")
        return True


def test_price_sanity():
    """Test that prices are reasonable (positive, not extreme)."""
    print("\n" + "="*70)
    print("TEST: Price Sanity Checks")
    print("="*70)
    
    test_tickers = ['AAPL', 'MSFT', 'GOOGL', 'BRK-A']  # Include Berkshire to test high prices
    
    failures = []
    for ticker in test_tickers:
        validation = validate_single_stock(ticker)
        price = validation['raw_data']['price']
        
        if price is None:
            failures.append(f"{ticker}: No price data")
            print(f"  ❌ {ticker}: No price data")
        elif price <= 0:
            failures.append(f"{ticker}: Negative or zero price")
            print(f"  ❌ {ticker}: Invalid price: ${price:.2f}")
        elif price > 1000000:  # Sanity check (even BRK-A is < $1M)
            failures.append(f"{ticker}: Suspiciously high price")
            print(f"  ❌ {ticker}: Suspiciously high price: ${price:,.2f}")
        else:
            print(f"  ✓ {ticker}: Price looks reasonable: ${price:.2f}")
    
    if failures:
        print(f"\n❌ FAILED: {len(failures)} ticker(s) have price issues")
        return False
    else:
        print(f"\n✓ PASSED: All prices are reasonable")
        return True


def test_cagr_calculation():
    """Test that CAGR calculations are working."""
    print("\n" + "="*70)
    print("TEST: CAGR Calculation")
    print("="*70)
    
    from stock import calculate_cagr
    
    test_tickers = ['AAPL', 'MSFT', 'GOOGL']
    
    failures = []
    for ticker in test_tickers:
        cagr = calculate_cagr(ticker, years=5)
        
        if cagr is None:
            failures.append(f"{ticker}: CAGR returned None")
            print(f"  ❌ {ticker}: CAGR calculation failed (returned None)")
        elif cagr < -50 or cagr > 200:  # Sanity check: between -50% and 200% per year
            failures.append(f"{ticker}: CAGR out of reasonable range")
            print(f"  ❌ {ticker}: CAGR seems unreasonable: {cagr:.2f}%")
        else:
            print(f"  ✓ {ticker}: CAGR calculated successfully: {cagr:.2f}%")
    
    if failures:
        print(f"\n❌ FAILED: {len(failures)} ticker(s) have CAGR issues")
        return False
    else:
        print(f"\n✓ PASSED: All CAGR calculations successful")
        return True


def run_all_tests():
    """Run all validation tests."""
    print("\n" + "="*70)
    print("STOCK SCREENER DATA VALIDATION TEST SUITE")
    print("="*70)
    
    tests = [
        test_data_completeness,
        test_pe_ratio_consistency,
        test_price_sanity,
        test_cagr_calculation,
    ]
    
    results = []
    for test in tests:
        try:
            passed = test()
            results.append((test.__name__, passed))
        except Exception as e:
            print(f"\n❌ ERROR in {test.__name__}: {e}")
            results.append((test.__name__, False))
    
    # Summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    
    passed_count = sum(1 for _, passed in results if passed)
    total_count = len(results)
    
    for test_name, passed in results:
        status = "✓ PASSED" if passed else "❌ FAILED"
        print(f"  {status}: {test_name}")
    
    print(f"\n{passed_count}/{total_count} tests passed")
    
    if passed_count == total_count:
        print("\n✓ ALL TESTS PASSED - Data quality looks good!")
    else:
        print(f"\n❌ {total_count - passed_count} test(s) failed - Review data quality issues")
    
    return passed_count == total_count


if __name__ == "__main__":
    run_all_tests()
