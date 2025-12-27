
# This weight screens for long term durable ad platform stocks. 

AD_PLATFORM_WEIGHT_MAP = {
    # --- Valuation & Shareholder Yield ---
    "ev_to_fcf": 0.22,

    # --- Profitability & Operating Leverage ---
    "operating_margin": 0.16,
    "fcf_margin": 0.16,
    "incremental_margin": 0.14,

    # --- Growth (Durability-adjusted) ---
    "revenue_cagr": 0.04,
    "arpu_cagr": 0.06,
    "revenue_volatility": 0.08,

    # --- Capital Discipline & Moat Maintenance ---
    "capex_intensity": 0.07,
    "rnd_intensity": 0.07,

    # --- Balance Sheet Safety ---
    "net_debt_to_ebitda": 0.00,
    "interest_coverage": 0.00,
}

# This weight screens for higher cash yield and capital-efficient ad platforms,
# assuming durability rather than explicitly testing for it

# AD_PLATFORM_WEIGHT_MAP = {
#     # --- Valuation & Shareholder Yield ---
#     "ev_to_fcf": 0.22,

#     # --- Profitability & Operating Leverage ---
#     "operating_margin": 0.16,
#     "fcf_margin": 0.16,
#     "incremental_margin": 0.14,

#     # --- Growth (Durability-adjusted) ---
#     "revenue_cagr": 0.08,
#     "arpu_cagr": 0.06,

#     # --- Capital Discipline & Moat Maintenance ---
#     "capex_intensity": 0.08,
#     "rnd_intensity": 0.08,

#     # --- Balance Sheet Safety ---
#     "net_debt_to_ebitda": 0.01,
#     "interest_coverage": 0.01,
# }