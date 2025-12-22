FABLESS_MODIFIER = {
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

FOUNDRY_MODIFIER = {
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
EQUIPMENT_MODIFIER = {
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
ANALOG_MODIFIER = {
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
MEMORY_MODIFIER = {
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