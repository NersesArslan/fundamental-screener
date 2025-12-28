"""
HARDWARE ECOSYSTEMS — SERVICES-LED COMPOUNDING THESIS (MVP)

Core question:
Which hardware ecosystem companies can generate durable long-term shareholder
returns by using hardware scale as a distribution and lock-in mechanism for
high-margin, recurring services revenue — without destroying value through
capital intensity?

Economic belief:
- Hardware ecosystems are not primarily hardware businesses; they are platform
  businesses where hardware serves as a means of customer acquisition, retention,
  and ecosystem lock-in.
- Long-term value creation depends on the company’s ability to layer recurring,
  high-margin services revenue on top of a large installed hardware base.
- Hardware growth alone is insufficient and often value-destructive if not paired
  with strong capital discipline and services monetization.
- Capital intensity is a critical risk factor: poorly managed CapEx can negate even
  strong brand power and ecosystem scale.

What this screen rewards:
- High or improving gross margins, indicating successful services penetration and
  pricing power
- A meaningful services revenue mix, reflecting durable, recurring monetization of
  the installed base
- Strong operating and free cash flow margins, demonstrating that ecosystem economics
  translate into shareholder returns
- Disciplined capital expenditure relative to revenue
- Reasonable valuation relative to cash generation (EV/FCF)

What this screen penalizes:
- Hardware-led growth strategies that fail to transition toward services economics
- Low-margin or highly cyclical hardware revenue without durable monetization layers
- Excessive capital intensity that suppresses returns on invested capital
- Valuations that assume ecosystem monetization without current financial evidence
- Conglomerate complexity that dilutes ecosystem-level profitability

Explicit exclusions / limitations:
- This thesis intentionally deprioritizes hardware unit growth, shipment volume,
  and market share leadership as primary investment drivers.
- It does not explicitly model brand strength, customer loyalty, or ecosystem
  switching costs beyond what is reflected in financial outcomes.
- Services revenue mix may be limited by data availability; when unavailable, the
  screen reflects consolidated economics rather than idealized segment performance.

Interpretation guidance:
- High scores indicate hardware ecosystem companies that have successfully shifted
  from product-centric economics to durable, services-led compounding.
- Lower scores do not imply weak products or brands, only weaker alignment with a
  services-driven, capital-efficient shareholder return thesis.
"""

# Services revenue mix is currently unpopulated due to data provider limitations; results reflect consolidated ecosystem economics.

HARDWARE_ECOSYSTEM_WEIGHT_MAP = {
    # --- Valuation & Shareholder Yield ---
    "ev_to_fcf": 0.20,

    # --- Ecosystem Monetization Quality ---
    "services_revenue_mix": 0.18,
    "gross_margin": 0.16,

    # --- Realized Profitability ---
    "operating_margin": 0.12,
    "fcf_margin": 0.12,

    # --- Capital Discipline ---
    "capex_intensity": 0.10,

    # --- Growth (Subordinate) ---
    "revenue_cagr": 0.06,

    # --- Balance Sheet Guardrails ---
    "net_debt_to_ebitda": 0.04,
    "interest_coverage": 0.02,
}
