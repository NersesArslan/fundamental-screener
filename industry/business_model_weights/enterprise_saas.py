
"""
ENTERPRISE SAAS — DURABLE COMPOUND GROWTH THESIS (MVP)

Core question:
Which Enterprise SaaS companies can compound shareholder value over the long term
by converting recurring revenue into durable operating leverage at a reasonable price?

Economic belief:
- Enterprise SaaS success is not defined by maximum growth or fastest scaling,
  but by the ability to scale recurring revenue faster than organizational complexity.
- Durable compounders demonstrate high gross margins, disciplined R&D investment,
  improving organizational efficiency, and visible operating and free cash flow leverage.
- Valuation matters: even high-quality SaaS businesses can produce poor returns if
  acquired at excessive multiples.

What this screen rewards:
- High gross margins (economic scalability ceiling)
- Strong revenue per employee (organizational efficiency)
- Balanced growth and profitability (Rule of 40 discipline)
- Evidence of operating and free cash flow leverage
- Reasonable or attractive valuation relative to cash generation
- Sustainable reinvestment in product (R&D discipline)

What this screen penalizes:
- Growth achieved primarily through headcount expansion
- Persistent margin suppression justified only by future scale
- Low gross margin SaaS models resembling services businesses
- Overvaluation relative to demonstrated cash flow
- Organizational inefficiency that limits long-term operating leverage

Explicit exclusions / limitations:
- This screen intentionally deprioritizes:
  - maximum short-term revenue growth
  - TAM or platform optionality narratives
  - early-stage SaaS without demonstrated operating leverage
- It does not model churn, net revenue retention, or cohort expansion yet.
- Companies promising future leverage without current evidence are treated skeptically.

Interpretation guidance:
- High scores indicate durable SaaS compounders with proven economics.
- Lower scores do not imply poor businesses, only weaker alignment with this
  specific durability-first investment thesis.
"""


ENTERPRISE_SAAS_WEIGHT_MAP = {
    # --- Valuation & Shareholder Yield ---
    "ev_to_fcf": 0.18,

    # --- Unit Economics & Scalability Ceiling ---
    "gross_margin": 0.16,

    # --- Organizational & Product Discipline ---
    "revenue_per_employee": 0.14,
    "rnd_intensity": 0.12,

    # --- Balanced Growth vs Profitability ---
    "rule_of_40": 0.14,

    # --- Realized Profitability ---
    "operating_margin": 0.10,
    "fcf_margin": 0.08,

    # --- Balance Sheet Guardrails ---
    "net_debt_to_ebitda": 0.04,
    "interest_coverage": 0.04,
}

