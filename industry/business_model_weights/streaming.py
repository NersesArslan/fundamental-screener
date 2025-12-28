"""
STREAMING — CAPITAL-DISCIPLINED SCALE THESIS (MVP)

Core question:
Which streaming businesses can generate long-term shareholder returns by achieving
sufficient scale to stabilize content economics and transition toward sustainable
profitability and free cash flow?

Economic belief:
- Streaming is a capital-intensive subscription business where content spend is the
  primary driver of costs and competitive positioning.
- Scale alone does not create value; only scale that leads to declining content
  intensity and improving margins can support durable shareholder returns.
- Early-stage growth is not inherently valuable unless accompanied by evidence that
  incremental subscribers can be monetized without proportional increases in content
  investment.
- Balance sheet strength and capital discipline are critical, as prolonged losses
  are common and refinancing risk is real.

What this screen rewards:
- Evidence of improving or positive operating and free cash flow margins
- Declining capital intensity relative to revenue
- Reasonable valuation relative to demonstrated cash generation
- Balance sheet resilience that supports multi-year content investment cycles
- Moderate, sustainable growth rather than aggressive, loss-driven expansion

What this screen penalizes:
- Growth achieved primarily through escalating content spend
- Persistent negative margins without signs of operating leverage
- High capital intensity that suppresses long-term returns
- Excessive leverage that limits strategic flexibility
- Valuations that price in profitability without financial evidence

Explicit exclusions / limitations:
- This thesis intentionally deprioritizes subscriber growth, engagement metrics,
  and content quality narratives not reflected in financial outcomes.
- It does not attempt to predict which platforms will “win” culturally or
  dominate attention.
- Strategic optionality (bundling, advertising tiers, IP monetization) is treated
  as secondary unless it materially improves margins or cash flow.

Interpretation guidance:
- High scores indicate streaming businesses that show credible paths toward
  capital-efficient scale and sustainable economics.
- Lower scores do not imply weak brands or content, only weaker alignment with a
  discipline-first, profitability-aware investment thesis.
"""

# The Streaming business model cannot currently be evaluated against its 
# core economic thesis using yfinance alone, because ARPU growth and content 
# spend intensity are not available in consolidated financial statements.

STREAMING_WEIGHT_MAP = {
    # --- Valuation & Shareholder Reality ---
    "ev_to_fcf": 0.18,

    # --- Monetization Quality (Core Streaming Signal) ---
    "arpu_growth": 0.16,

    # --- Profitability (Evidence, not promises) ---
    "operating_margin": 0.14,
    "fcf_margin": 0.12,

    # --- Content Discipline (Primary Risk) ---
    "content_spend_intensity": 0.16,

    # --- Growth (Secondary, quality-checked) ---
    "revenue_cagr": 0.10,

    # --- Balance Sheet Survivability ---
    "net_debt_to_ebitda": 0.08,
    "interest_coverage": 0.06,
}
