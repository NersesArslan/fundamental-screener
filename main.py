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
import os
import sys

# ============================================================================
# SCORING WEIGHTS - Tailored per industry
# ============================================================================

def apply_subsector_weights(base: dict, modifier: dict) -> dict:
    """
    Apply subsector-specific modifiers to base semiconductor weights.
    Uses MULTIPLICATIVE modifiers (e.g., 1.25 = +25%, 0.60 = -40%).
    Automatically normalizes to sum to 1.0.
    
    Example:
        fabless_weights = apply_subsector_weights(Semiconductor_Weights, Fabless_Modifier)
        # If base["roic"] = 0.10 and modifier["roic"] = 1.25
        # → new["roic"] = 0.10 * 1.25 = 0.125 (before normalization)
    """
    new_weights = {}
    for k, v in base.items():
        multiplier = modifier.get(k, 1.0)  # Default multiplier = 1.0 (no change)
        new_weights[k] = base[k] * multiplier
    
    # Normalize to sum to 1.0
    total = sum(new_weights.values())
    if total > 0:
        new_weights = {k: v / total for k, v in new_weights.items()}
    
    return new_weights


Semiconductor_Weights = {
    # Valuation
    "ev_to_fcf":           0.12,
    "revenue_cagr":        0.12,

    # Profitability
    "operating_margin":    0.15,
    "fcf_margin":          0.12,
    "gross_margin":        0.08,

    # Balance sheet
    "net_debt_to_ebitda":  0.08,
    "interest_coverage":   0.08,

    # Capital efficiency
    "roic":                0.10,

    # Industry structure (modified per sub-sector)
    "capex_intensity":     0.08,
    "inventory_turnover":  0.07,
}
# Sum = 1.00 ✓


Fabless_Modifier = {
    "ev_to_fcf":           1.05,
    "revenue_cagr":        1.10,

    "operating_margin":    1.10,
    "fcf_margin":          1.15,
    "gross_margin":        1.10,

    "net_debt_to_ebitda":  1.00,
    "interest_coverage":   1.00,

    "roic":                1.25,   # ROIC is extremely meaningful here

    "capex_intensity":     0.60,   # Should NOT be rewarded; capex is low by design
    "inventory_turnover":  1.00,
}

Foundry_Modifier = {
    "ev_to_fcf":           0.70,  # FCF is structurally low → penalize less
    "revenue_cagr":        0.90,

    "operating_margin":    1.20,
    "fcf_margin":          0.60,  # FCF is not meaningful

    "gross_margin":        1.20,

    "net_debt_to_ebitda":  1.10,  # Very important: leverage must be low
    "interest_coverage":   1.20,

    "roic":                0.50,  # ROIC is misleading for foundries

    "capex_intensity":     1.40,  # HIGH CAPEX IS GOOD (use inverted score)
    "inventory_turnover":  0.90,
}
Equipment_Modifier = {
    "ev_to_fcf":           1.00,
    "revenue_cagr":        1.10,

    "operating_margin":    1.20,
    "fcf_margin":          1.00,
    "gross_margin":        1.15,

    "net_debt_to_ebitda":  0.90,
    "interest_coverage":   1.00,

    "roic":                1.10,   # Very meaningful here

    "capex_intensity":     0.80,   # CapEx matters but lower usually better
    "inventory_turnover":  1.15,
}
Analog_Modifier = {
    "ev_to_fcf":           1.10,
    "revenue_cagr":        0.90,   # Lower growth expectations

    "operating_margin":    1.20,
    "fcf_margin":          1.10,
    "gross_margin":        1.25,

    "net_debt_to_ebitda":  1.00,
    "interest_coverage":   1.05,

    "roic":                1.30,   # King metric for analog

    "capex_intensity":     0.50,   # Very capital-light
    "inventory_turnover":  1.10,
}
Memory_Modifier = {
    "ev_to_fcf":           0.60,   # Cyclical not structural

    "revenue_cagr":        1.15,   # Can see big cyclical swings

    "operating_margin":    1.00,
    "fcf_margin":          0.70,   # CapEx heavy
    "gross_margin":        1.00,

    "net_debt_to_ebitda":  1.10,
    "interest_coverage":   1.00,

    "roic":                0.40,   # Very cyclical, misleading

    "capex_intensity":     0.90,   # Some efficiency matters
    "inventory_turnover":  1.40,   # Critical for memory
}


# Ticker-to-subsector mapping
SUBSECTOR_MAP = {
    # Fabless Designers
    "NVDA": "fabless", "AMD": "fabless", "QCOM": "fabless", "AVGO": "fabless",
    "MRVL": "fabless", "MPWR": "fabless", "MCHP": "fabless", "QRVO": "fabless",
    "SWKS": "fabless", "XLNX": "fabless", "ARMH": "fabless", "SLAB": "fabless",
    "ALGM": "fabless", "MTSI": "fabless",
    
    # Foundries
    "TSM": "foundry", "UMC": "foundry",
    
    # Equipment
    "ASML": "equipment", "LRCX": "equipment", "KLAC": "equipment", "AMAT": "equipment",
    "ENTG": "equipment", "MKSI": "equipment", "ACLS": "equipment", "UCTT": "equipment",
    "ICHR": "equipment", "COHU": "equipment", "FORM": "equipment", "ONTO": "equipment",
    "NVMI": "equipment", "CAMT": "equipment",
    
    # IDMs (use base weights or analog modifier for mature IDMs)
    "INTC": "idm", "TXN": "analog", "NXPI": "analog", "STM": "idm",
    "ADI": "analog", "ON": "idm", "WOLF": "idm", "CRUS": "analog",
    "SIMO": "idm", "DIOD": "idm", "MXL": "idm", "SMTC": "idm", "RMBS": "idm",
    
    # Memory
    "MU": "memory", "WDC": "memory", "STX": "memory",
}

# Modifier lookup
MODIFIERS = {
    "fabless": Fabless_Modifier,
    "foundry": Foundry_Modifier,
    "equipment": Equipment_Modifier,
    "analog": Analog_Modifier,
    "memory": Memory_Modifier,
    "idm": {},  # IDMs use base weights (no modifier)
}


# Note: Adjust core weights proportionally when adding industry metrics


# ============================================================================
# MAIN - Wire it all together
# ============================================================================

if __name__ == "__main__":
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
    WATCHLIST = FABLESS  # Change to: FABLESS, FOUNDRIES, EQUIPMENT, or ALL_SEMIS
    INDUSTRY_NAME = "FABLESS DESIGNERS"  # Update this too
    
    # Screen semiconductors with industry-specific metrics
    print("\n" + "="*70)
    print(f"SEMICONDUCTOR SCREENING - {INDUSTRY_NAME}")
    print("="*70)
    
    screener = StockScreener(provider, industry='semis')
    
    # Check if cached results exist (for fast testing)
    USE_CACHE = os.path.exists('utils/cached_screening_results.json')
    
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

