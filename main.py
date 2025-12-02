"""
Stock Screener - Value investing focused
Elegantly decoupled for future data source flexibility.

MODULAR METRICS SYSTEM:
- Easily add/remove metrics by customizing the metrics list
- Pre-configured sets: get_default_metrics(), get_growth_metrics(), get_value_metrics()
- Or create your own custom list!

SCORING SYSTEM:
- Normalize metrics and calculate weighted composite scores
- Adjust weights in the SCORING_WEIGHTS dictionary below
- Weights should sum to 1.0
"""
from stock_providers import YFinanceProvider
from stock_screener import StockScreener
from screener_output import format_screener_output
from stock_scorer import StockScorer
from metrics import (
    get_default_metrics, 
    get_growth_metrics, 
    get_value_metrics,
    PriceMetric,
    PERatioMetric,
    RevenueCagr3YearMetric,
    ROEMetric,
    FreeCashFlowMetric,
)


# ============================================================================
# SCORING WEIGHTS - Adjust these to match your investment strategy
# ============================================================================

SCORING_WEIGHTS = {
    'pe_ratio': 0.10,           # Lower P/E = better value
    'debt_to_equity': 0.15,     # Lower debt = better
    '3_year_cagr': 0.15,        # Higher growth = better
    'returnonequity': 0.20,     # Higher ROE = better profitability
    'free_cashflow': 0.10,      # Higher FCF = better
    'fcf_yield': 0.30,          # Higher yield = better
}

# Note: Weights should sum to 1.0 (current sum: {sum(SCORING_WEIGHTS.values())})


# ============================================================================
# MAIN - Wire it all together
# ============================================================================

if __name__ == "__main__":
    # Your watchlist
    semis = ['NVDA', 'AMD', 'INTC', 'TSM', 'ASML', 'QCOM', 'AVGO', 'MU', 'LRCX', 'KLAC']
    
    # Data provider
    provider = YFinanceProvider()
    
    # ========================================================================
    # CHOOSE YOUR METRICS - Uncomment the one you want!
    # ========================================================================
    

    screener = StockScreener(provider, metrics=get_default_metrics())
 
    print("\nFetching stock data...")
    stocks_data = screener.screen_multiple(semis)
    
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
    
    scorer = StockScorer(SCORING_WEIGHTS, normalization='minmax')
    scores = scorer.calculate_scores(stocks_data)
    
    # Sort by score (highest first)
    sorted_scores = sorted(scores.items(), key=lambda x: x[1] if x[1] is not None else -1, reverse=True)
    
    print("\nRanking:")
    for rank, (ticker, score) in enumerate(sorted_scores, 1):
        if score is not None:
            print(f"  {rank}. {ticker:6} - Score: {score:.1f}/100")
        else:
            print(f"  {rank}. {ticker:6} - Score: N/A (missing data)")
    
    print("\n💡 Tip: Edit SCORING_WEIGHTS in main.py to adjust your scoring criteria!")
    print("💡 Tip: Set a weight to 0 to exclude that metric from scoring.")
