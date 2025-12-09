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