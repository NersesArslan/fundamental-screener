
"""
AD PLATFORMS — DURABLE COMPOUNDING THESIS (MVP)

Core question:
Which ad platform companies can compound shareholder value over the long term by
converting demand aggregation and scale into durable, capital-efficient cash flows
at reasonable valuations?

Economic belief:
- Ad platforms are monetization engines built on demand aggregation, pricing power,
  and operating leverage rather than pure growth.
- Long-term returns are driven by the consistency with which incremental revenue
  converts into profit and free cash flow, not by market share or revenue growth alone.
- Durable ad platforms exhibit stable demand, strong margins, disciplined reinvestment,
  and resilience through advertising cycles.

What this screen rewards:
- Strong operating and free cash flow margins
- High incremental margins (with diminishing returns recognized at extreme levels)
- Reasonable valuation relative to cash generation (EV/FCF discipline)
- Capital-light economics (low reinvestment intensity)
- Stable revenue growth indicative of durable advertiser demand

What this screen penalizes:
- Volatile or cyclical revenue patterns that undermine long-term compounding
- Monetization models where growth fails to translate into profit
- Excessive reinvestment that dilutes shareholder returns
- Valuations that assume perpetual growth without margin durability

Explicit exclusions / limitations:
- This thesis intentionally deprioritizes pure scale dominance and TAM expansion narratives.
- It does not explicitly model user growth, engagement metrics, or ad load expansion.
- Conglomerate structures may dilute ad economics at the consolidated level; this screen
  reflects shareholder reality rather than segment-level idealization.

Interpretation guidance:
- High scores indicate ad platforms capable of durable cash flow compounding through cycles.
- Lower scores do not imply weak businesses, only weaker alignment with a durability-first,
  shareholder-return–oriented investment lens.
"""


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
