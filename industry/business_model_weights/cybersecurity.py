"""
CYBERSECURITY — DURABLE OPERATING ECONOMICS THESIS (MVP)

Core question:
Which cybersecurity companies can generate long-term shareholder returns by
converting high gross margins into sustainable operating leverage without
permanently elevated go-to-market costs?

Economic belief:
- Cybersecurity is fundamentally a trust- and switching-cost–driven software business,
  not a winner-take-all network or pure growth market.
- Long-term value creation depends less on headline growth and more on the ability
  to translate strong gross margins into operating and free cash flow leverage.
- Sales & marketing efficiency is the primary constraint in cybersecurity; companies
  that cannot reduce S&M intensity over time face structural limits to profitability.

What this screen rewards:
- High gross margins (software purity and pricing power)
- Evidence of operating and free cash flow leverage
- Declining or efficient sales & marketing intensity
- Reasonable valuation relative to demonstrated cash generation
- Balance sheet survivability through long enterprise sales cycles

What this screen penalizes:
- Growth achieved primarily through sustained high sales & marketing spend
- Persistent operating losses justified only by future scale
- Low gross-margin models resembling services or implementation-heavy businesses
- Valuations that price in margin expansion without current evidence
- Fragile capital structures in cash-burning companies

Explicit exclusions / limitations:
- This thesis intentionally deprioritizes platform breadth, product optionality,
  and long-dated ecosystem narratives.
- It does not attempt to model future cross-sell efficiency, module expansion,
  or category consolidation benefits.
- Companies promising future operating leverage without current proof are treated
  skeptically, not dismissed outright.

Interpretation guidance:
- High scores indicate cybersecurity companies that already exhibit durable,
  capital-efficient economics.
- Lower scores do not imply inferior technology, only weaker alignment with a
  discipline-first, evidence-based investment thesis.
"""

CYBERSECURITY_WEIGHT_MAP = {
    # --- Valuation & Shareholder Yield ---
    "ev_to_fcf": 0.18,

    # --- Profitability & Unit Economics ---
    "gross_margin": 0.16,
    "operating_margin": 0.12,
    "fcf_margin": 0.12,

    # --- Growth (Secondary, not dominant) ---
    "revenue_cagr": 0.10,

    # --- Go-To-Market Efficiency (Critical in Cyber) ---
    "sales_marketing_intensity": 0.14,

    # --- Capital Discipline ---
    "rnd_intensity": 0.08,
    "capex_intensity": 0.04,

    # --- Balance Sheet Survivability ---
    "net_debt_to_ebitda": 0.04,
    "interest_coverage": 0.02,
}
