"""
Stock Screener - Industry-Aware Universal Metrics

ARCHITECTURE:
- Core universal metrics work across all industries
- Industry-specific overrides add specialized metrics
- Industry-aware scoring system

CORE UNIVERSAL METRICS (6):
1. EV/FCF - Valuation relative to cash generation
2. Revenue CAGR - Growth trajectory
3. Operating Margin - Operational efficiency
4. FCF Margin - Cash generation efficiency
5. Net Debt/EBITDA - Leverage (handles negative book equity)
6. Interest Coverage - Debt servicing ability

INDUSTRY SUPPORT:
- 'semis': Adds CapEx Intensity, Inventory Turnover, Gross Margin
- 'tech': Adds R&D Intensity, Net Debt/FCF
- More industries coming soon!

USAGE:
    screener = StockScreener(provider, industry='semis')
    screener = StockScreener(provider, industry='tech')
"""
from core.stock_providers import YFinanceProvider
from core.stock_screener import StockScreener
from core.screener_output import format_screener_output
from core.stock_scorer import StockScorer
from data.industries import ALL_SEMIS, FABLESS, FOUNDRIES, EQUIPMENT
from data.score_weights import SUBSECTOR_MAP, MODIFIERS, apply_subsector_weights, Semiconductor_Weights
import os
import sys




# Note: Adjust core weights proportionally when adding industry metrics


# ============================================================================
# MAIN - Wire it all together
# ============================================================================

if __name__ == "__main__":
    # ========================================================================
    # CONFIGURATION
    # ========================================================================
    USE_CACHE = False  # Toggle: True = fast cached data, False = live API calls
    
    # ========================================================================
    # WATCHLISTS - Organize by industry
    # ========================================================================
    semis = ['NVDA', 'AMD', 'INTC', 'TSM', 'ASML', 'QCOM', 'AVGO', 'MU', 'LRCX', 'KLAC']
    big_tech = ['MSFT', 'GOOGL', 'AAPL', 'AMZN', 'META', 'ORCL', 'CRM', 'ADBE', 'IBM', 'PLTR']
    
    # Data provider
    provider = YFinanceProvider()
    
    # ========================================================================
    # INDUSTRY-AWARE SCREENING
    # ========================================================================
    
    # Choose which sub-industry to screen
    WATCHLIST = ALL_SEMIS  # Change to: FABLESS, FOUNDRIES, EQUIPMENT, or ALL_SEMIS
    INDUSTRY_NAME = "ALL Semiconductors"  # Update this too
    
    # Screen semiconductors with industry-specific metrics
    print("\n" + "="*70)
    print(f"SEMICONDUCTOR SCREENING - {INDUSTRY_NAME}")
    print("="*70)
    
    screener = StockScreener(provider, industry='semis')
    
    # Check if cached results exist and user wants to use them
    cache_exists = os.path.exists('utils/cached_screening_results.json')
    USE_CACHE = USE_CACHE and cache_exists
    
    if USE_CACHE:
        print("\n📦 Using cached results (fast mode)")
        print("💡 Delete utils/cached_screening_results.json to fetch fresh data\n")
        from utils.cache_results import load_cached_results
        stocks_data = load_cached_results()
    else:
        print(f"\nFetching stock data for {len(WATCHLIST)} {INDUSTRY_NAME} stocks...")
        stocks_data = screener.screen_multiple(WATCHLIST, verbose=True)
    
    # Display raw fundamentals
    metric_names = screener.get_metric_names()
    df = format_screener_output(stocks_data, metric_names)
    print("\nStock Fundamentals:")
    print(df.to_string())
    
    # ========================================================================
    # SCORING - Calculate weighted composite scores PER TICKER
    # ========================================================================
    print("\n" + "="*70)
    print("COMPOSITE SCORES (0-100 scale, weighted by investment criteria)")
    print("="*70)
    
    # Apply ticker-specific subsector weights
    print("Applying subsector-specific weights per ticker:\n")
    
    # Create a weight configuration for each ticker
    ticker_weights = {}
    subsector_counts = {}
    
    for ticker in stocks_data.keys():
        subsector = SUBSECTOR_MAP.get(ticker, "idm")  # Default to IDM if not mapped
        modifier = MODIFIERS.get(subsector, {})
        ticker_weights[ticker] = apply_subsector_weights(Semiconductor_Weights, modifier)
        
        # Count subsectors for summary
        subsector_counts[subsector] = subsector_counts.get(subsector, 0) + 1
    
    # Print subsector distribution
    for subsector, count in sorted(subsector_counts.items()):
        print(f"  {subsector.capitalize()}: {count} stocks")
    print()
    
    # Score each ticker with its specific weights
    scores = {}
    for ticker, data in stocks_data.items():
        weights = ticker_weights[ticker]
        scorer = StockScorer(weights, normalization='minmax')
        # Calculate score for just this ticker (need to pass all data for normalization)
        ticker_scores = scorer.calculate_scores(stocks_data)
        scores[ticker] = ticker_scores[ticker]
    
    # Sort by score (highest first)
    sorted_scores = sorted(scores.items(), key=lambda x: x[1] if x[1] is not None else -1, reverse=True)
    
    print("\nRanking:")
    for rank, (ticker, score) in enumerate(sorted_scores, 1):
        if score is not None:
            print(f"  {rank}. {ticker:6} - Score: {score:.1f}/100")
        else:
            print(f"  {rank}. {ticker:6} - Score: N/A (missing data)")
    
    print("\n💡 Tip: Edit SEMIS_SCORING_WEIGHTS in main.py to adjust your scoring criteria!")
    print(f"💡 Tip: Change industry='semis' to industry='tech' for big tech screening.")
    print(f"💡 Available industries: 'semis', 'tech'")

