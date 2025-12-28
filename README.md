# Fundamentals-Driven Stock Screener

A modular, fundamentals-first stock screening system designed to evaluate companies
through **explicit economic theses**, rather than generic factor models or price prediction.

This project asks a simple but demanding question:

> *How well does a business convert its core advantage (scale, growth, demand aggregation,
> or capital investment) into durable shareholder returns?*

The system is intentionally:
- **Comparative, not predictive**
- **Business-model aware**
- **Explicit about assumptions**
- **Resistant to silent overfitting**

---

## Core Principles

- **Separation of concerns**
  - Metrics compute economic concepts only
  - Scoring applies explicit weights
  - Experiments express investment theses
- **Price ≠ Quality**
  - Valuation is contextual, not absolute
- **Durability over narrative**
  - Preference for demonstrated operating leverage over promised future scale
- **Interpretability first**
  - Every ranking should be explainable in economic terms

---

## Architecture Overview


fundamental-screener/

├── .gitignore

├── README.md

├── main.py                          # Entry point - toggle between business models

├── calculation_functions.py         # Shared calculation utilities

├── run_cmd.sh                       # Shell script runner

│
├── config/                          # Configuration files

│
├── core/                            # Core screening & scoring engine


│   ├── screener_output.py           # Output formatting


│   ├── stock_providers.py           # Data provider abstraction (YFinance)


│   ├── stock_scorer.py              # Normalization & weighted scoring


│   └── stock_screener.py            # Metric calculation orchestration

│

├── data/                            # External data files

│   ├── README.md

│   └── user_metrics.csv             # Manual user/revenue data
│
├── experiments/

│   └── run_business_model.py        # Business model test runner

│

├── industry/                        # Industry-specific configurations

│   ├── semiconductor_base_weights.py

│   ├── semiconductor_modifiers.py

│   └── business_model_weights/      # Weight maps per business model

│       ├── ad_platform.py

│       ├── cloud_infrastructure.py

│       ├── cybersecurity.py

│       ├── enterprise_ai.py

│       └── enterprise_saas.py

│

├── metrics/                         # Metric definitions

│   ├── core_metrics.py              # Universal metrics (EV/FCF, CAGR, margins)

│   ├── semiconductors.py            # Semiconductor-specific metrics

│   ├── shared_metrics.py            # Shared industry metrics (ROIC, CapEx)

│   ├── business_models/             # Business model-specific metrics

│   │   ├── ad_platform.py

│   │   ├── cloud_infrastructure.py

│   │   ├── cybersecurity.py

│   │   ├── enterprise_ai.py

│   │   ├── enterprise_saas.py

│   │   ├── hardware_ecosystem.py

│   │   ├── legacy_enterprise.py

│   │   └── streaming.py

│   └── shared_business_models/      # Reusable business model metrics

│       ├── arpu_growth.py

│       ├── incremental_margin.py

│       ├── revenue_per_employee.py

│       ├── rnd_intensity.py

│       └── rule_of_40.py

│
├── universes/                       # Stock ticker lists per business model

│   ├── ad_platform.py

│   ├── cloud_infrastructure.py

│   ├── cybersecurity.py

│   ├── enterprise_ai.py

│   ├── enterprise_saas.py

│   ├── hardware_ecosystem.py

│   ├── legacy_enterprise.py

│   ├── semiconductors.py

│   └── streaming.py

│
└── utils/                           # Utility scripts
    ├── cache_results.py
    └── test_metrics.py
