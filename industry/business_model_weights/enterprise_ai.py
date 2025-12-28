"""
ENTERPRISE AI — ECONOMIC PROOF THESIS (MVP)

Core question:
Which Enterprise AI companies are demonstrating credible economic proof that AI-driven
growth can translate into durable shareholder returns, rather than remaining a perpetual
R&D and infrastructure cost center?

Economic belief:
- Enterprise AI is a high-fixed-cost software business with uncertain marginal economics.
- Long-term value creation depends not on AI capability or narrative leadership, but on
  whether incremental revenue converts into operating profit and free cash flow.
- Many Enterprise AI companies will grow revenue rapidly without ever achieving meaningful
  operating leverage due to ongoing R&D, infrastructure, and inference costs.

What this screen rewards:
- Positive and improving incremental margins (proof that AI monetizes at the margin)
- Evidence of operating and free cash flow leverage
- Reasonable valuation relative to cash generation (EV/FCF discipline)
- R&D investment that is disciplined rather than perpetually dilutive
- Balance sheet resilience sufficient to survive long AI investment cycles

What this screen penalizes:
- High growth without incremental profitability
- AI narratives unsupported by operating leverage
- Persistent margin suppression justified only by future scale
- Excessive valuation relative to demonstrated cash flow
- Business models where AI primarily increases cost rather than economic output

Explicit exclusions / limitations:
- This screen intentionally deprioritizes:
  - model quality, technical sophistication, or AI “leadership”
  - TAM or platform-optionalities without economic proof
  - early-stage AI businesses without margin signal
- It does not attempt to forecast future AI breakthroughs or step-function cost declines.
- Companies promising future AI monetization without current incremental margin evidence
  are treated skeptically.

Interpretation guidance:
- High scores indicate Enterprise AI companies already translating AI capabilities into
  real economic leverage.
- Lower scores do not imply technological inferiority, only weaker alignment with this
  proof-first investment thesis.
"""

ENTERPRISE_AI_WEIGHT_MAP = {
    # --- Valuation & Shareholder Reality ---
    "ev_to_fcf": 0.22,

    # --- Proof of AI Economics (BM Core) ---
    "incremental_margin": 0.18,

    # --- Base Profitability ---
    "operating_margin": 0.12,
    "fcf_margin": 0.10,

    # --- Growth (Heavily Discounted) ---
    "revenue_cagr": 0.08,

    # --- R&D Discipline (AI-Specific) ---
    "rnd_intensity": 0.12,

    # --- Capital & Balance Sheet Risk ---
    "net_debt_to_ebitda": 0.10,
    "interest_coverage": 0.08,
}

