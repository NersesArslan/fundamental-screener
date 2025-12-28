"""
LEGACY ENTERPRISE — DURABLE CASH HARVESTING THESIS (MVP)

Core question:
Which legacy enterprise companies can deliver reliable long-term shareholder
returns by harvesting stable cash flows with disciplined reinvestment, while
avoiding value destruction from volatility, decay, or capital misallocation?

Economic belief:
- Legacy enterprise businesses are mature, mission-critical providers whose value
  creation is driven primarily by durability and cash generation rather than growth.
- Long-term shareholder returns depend on the consistency, yield, and sustainability
  of free cash flow, not on reinvention narratives or accelerated scaling.
- Stability is an asset: predictable revenue, entrenched customer relationships,
  and low volatility are core economic strengths in this business model.
- Capital discipline is essential; excessive capital expenditure or aggressive
  reinvestment often erodes returns in mature enterprise businesses.

What this screen rewards:
- High free cash flow yield, reflecting meaningful cash return relative to valuation
- Strong free cash flow and operating margins, indicating real cash generation
- Low revenue volatility, signaling durable demand and customer entrenchment
- Disciplined capital expenditure relative to revenue
- Balance sheet safety that supports long-term cash harvesting
- Modest, non-destructive growth that offsets decay without requiring heavy investment

What this screen penalizes:
- Volatile or unstable revenue streams inconsistent with legacy enterprise economics
- Capital-intensive reinvestment justified by turnaround or transformation narratives
- Declining or low-quality cash flows masked by accounting adjustments
- Excessive leverage that threatens long-term durability
- Valuations that fail to compensate investors for low growth and limited optionality

Explicit exclusions / limitations:
- This thesis intentionally deprioritizes high growth, platform optionality,
  and technology leadership narratives.
- It does not attempt to identify turnaround stories or companies in active
  reinvention phases.
- Strategic relevance and future positioning are considered only insofar as they
  manifest in stable cash generation and disciplined capital use.

Interpretation guidance:
- High scores indicate legacy enterprise companies capable of reliably harvesting
  cash with low volatility and strong shareholder return potential.
- Lower scores do not imply failing businesses, only weaker alignment with a
  durability-first, cash-yield–oriented investment thesis.
"""


LEGACY_ENTERPRISE_WEIGHT_MAP = {
    # --- Cash Yield & Valuation (Primary) ---
    "fcf_yield": 0.22,
    "ev_to_fcf": 0.12,

    # --- Cash Generation Quality ---
    "fcf_margin": 0.14,
    "operating_margin": 0.12,

    # --- Revenue Durability ---
    "revenue_volatility": 0.10,

    # --- Capital Discipline ---
    "capex_intensity": 0.10,

    # --- Balance Sheet Safety ---
    "net_debt_to_ebitda": 0.08,
    "interest_coverage": 0.06,

    # --- Decay Control (Secondary) ---
    "revenue_cagr": 0.04,
    "rnd_intensity": 0.02,
}
