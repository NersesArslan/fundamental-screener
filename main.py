"""
Stock Screener - Industry-Aware Universal Metrics

ARCHITECTURE:
- Core universal metrics work across all industries
- Industry-specific overrides add specialized metrics
- Industry-aware scoring system

CORE UNIVERSAL METRICS (7):
1. EV/FCF - Valuation relative to cash generation
2. ROIC - Returns on invested capital (not distorted by buybacks)
3. Revenue CAGR - Growth trajectory
4. Operating Margin - Operational efficiency
5. FCF Margin - Cash generation efficiency
6. Net Debt/EBITDA - Leverage (handles negative book equity)
7. Interest Coverage - Debt servicing ability

INDUSTRY SUPPORT:
- 'semis': Adds CapEx Intensity, Inventory Turnover, Gross Margin
- 'tech': Adds R&D Intensity, Net Debt/FCF
- More industries coming soon!

USAGE:
    screener = StockScreener(provider, industry='semis')
    screener = StockScreener(provider, industry='tech')
"""
from stock_providers import YFinanceProvider
from stock_screener import StockScreener
from screener_output import format_screener_output
from stock_scorer import StockScorer


# ============================================================================
# SCORING WEIGHTS - Tailored per industry
# ============================================================================

# NOTE: Core metrics have different weights across industries based on what matters most.
# For example, semiconductors heavily weight margins and capital efficiency.
# We'll add more industry-specific weight profiles as we expand.

SEMIS_SCORING_WEIGHTS = {
    # Core metrics (adjusted for semiconductor industry)
    'ev_to_fcf': 0.15,           # Lower is better - valuation
    'roic': 0.20,                # Higher is better - capital efficiency (critical for semis)
    'revenue_cagr': 0.15,        # Higher is better - growth
    'operating_margin': 0.15,    # Higher is better - operational efficiency
    'fcf_margin': 0.15,          # Higher is better - cash generation
    'net_debt_to_ebitda': 0.10,  # Lower is better - leverage
    'interest_coverage': 0.10,   # Higher is better - debt safety
    
}
# Sum = 1.00 ✓

# Note: Adjust core weights proportionally when adding industry metrics


# ============================================================================
# MAIN - Wire it all together
# ============================================================================

if __name__ == "__main__":
    # ========================================================================
    # WATCHLISTS - Organize by industry
    # ========================================================================
    semis = ['NVDA', 'AMD', 'INTC', 'TSM', 'ASML', 'QCOM', 'AVGO', 'MU', 'LRCX', 'KLAC']
    big_tech = ['MSFT', 'GOOGL', 'AAPL', 'AMZN', 'META', 'ORCL', 'CRM', 'ADBE', 'IBM']
    
    # Data provider
    provider = YFinanceProvider()
    
    # ========================================================================
    # INDUSTRY-AWARE SCREENING
    # ========================================================================
    
    # Screen semiconductors with industry-specific metrics
    print("\n" + "="*70)
    print("SEMICONDUCTOR SCREENING (Core + Semis Metrics)")
    print("="*70)
    
    screener = StockScreener(provider, industry='None')
    
    print("\nFetching stock data...")
    stocks_data = screener.screen_multiple(big_tech, verbose=True)
    
    # Display raw fundamentals
    metric_names = screener.get_metric_names()
    df = format_screener_output(stocks_data, metric_names)
    print("\nStock Fundamentals:")
    print(df.to_string())
    
    # ========================================================================
    # SCORING - Calculate weighted composite scores
    # ========================================================================
    print("\n" + "="*70)
    print("COMPOSITE SCORES (0-100 scale, weighted by investment criteria)")
    print("="*70)
    
    scorer = StockScorer(SEMIS_SCORING_WEIGHTS, normalization='minmax')
    scores = scorer.calculate_scores(stocks_data)
    
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

