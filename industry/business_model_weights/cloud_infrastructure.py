"""
CLOUD INFRASTRUCTURE — CAPITAL-EFFICIENT COMPOUNDING THESIS (MVP)

Core question:
Which cloud infrastructure providers can generate superior long-term shareholder
returns by converting scale and capital investment into durable, high-quality cash flows?

Economic belief:
- Cloud infrastructure is a capital-intensive, scale-driven business where market
  share alone does not guarantee attractive shareholder returns.
- Long-term value creation depends on how efficiently a provider converts heavy
  capital investment (CapEx) into sustained profitability, free cash flow, and
  acceptable returns on invested capital.
- Scale is necessary but not sufficient; disciplined capital allocation and margin
  structure determine whether cloud growth compounds or dilutes shareholder value.

What this screen rewards:
- Strong returns on invested capital (ROIC) or proxies thereof
- Efficient capital deployment (low CapEx intensity relative to revenue)
- High revenue generated per unit of capital invested (Revenue / CapEx)
- Healthy gross margins that indicate pricing power and cost discipline
- Evidence that cloud economics translate into consolidated shareholder returns,
  not just segment-level growth

What this screen penalizes:
- Capital-heavy growth that fails to earn adequate returns
- Cloud businesses whose economics are diluted at the parent-company level
- Persistent reinvestment without improving margin or cash flow outcomes
- Scale achieved primarily through infrastructure spending rather than efficiency gains

Explicit exclusions / limitations:
- This thesis intentionally deprioritizes pure market share leadership and absolute
  cloud revenue size.
- It does not attempt to isolate or idealize cloud segment economics when those
  economics are not directly reflected in consolidated financials.
- Platform optionality, ecosystem effects, and strategic importance are treated as
  secondary to demonstrated capital efficiency.

Interpretation guidance:
- High scores indicate cloud providers that have learned to grow without destroying
  returns on capital.
- Lower scores do not imply weak cloud offerings, only weaker alignment with a
  shareholder-return–focused, capital-efficiency investment thesis.
"""


CLOUD_INFRASTRUCTURE_WEIGHT_MAP = {
    # Core metrics (65%)
    "ev_to_fcf": 0.15,
    "revenue_cagr": 0.15,
    "operating_margin": 0.10,
    "fcf_margin": 0.10,
    "net_debt_to_ebitda": 0.075,
    "interest_coverage": 0.075,

    # Cloud-specific (35%)
    "roic": 0.10,
    "capex_intensity": 0.05,
    "revenue_per_capex": 0.08,

    "gross_margin": 0.05,
    "operating_margin_trend": 0.07,
}