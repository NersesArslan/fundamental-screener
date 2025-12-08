# Stockify - Value & Growth Stock Screener

Industry-aware stock screener with modular metrics and configurable weights.

## 📁 Project Structure

```
stockify/
├── core/                          # Core business logic
│   ├── stock_providers.py         # Data fetching (yfinance)
│   ├── stock_screener.py          # Screening orchestration
│   ├── stock_scorer.py            # Normalization & scoring
│   └── screener_output.py         # Output formatting
│
├── metrics/                       # Metric definitions
│   ├── core.py                    # 6 universal metrics
│   ├── semis_overrides.py         # Semiconductor addons
│   └── tech_overrides.py          # Tech addons
│
├── data/                          # Watchlists & industries
│   └── industries.py              # Sub-industry tickers
│
├── utils/                         # Testing & development
│   ├── cache_results.py           # Cache API results
│   ├── test_metrics.py            # Quick metric checks
│   └── cached_screening_results.json
│
├── main.py                        # Main entry point
└── run_cmd.sh                     # Convenience script
```

## 🚀 Quick Start

### Run Full Screener
```bash
./run_cmd.sh
```

### Fast Testing (Cache Mode)
```bash
# 1. Cache results once (takes ~15 sec)
./tractatus/bin/python3 -m utils.cache_results --save --industry semis --tickers NVDA AMD INTC

# 2. Test instantly (< 1 sec)
./run_cmd.sh
```

### Check Metrics Without API Calls
```bash
./tractatus/bin/python3 -m utils.test_metrics
```

## 🎯 Screening Sub-Industries

Edit `main.py` line 75-76:

```python
WATCHLIST = FABLESS        # Options: FABLESS, FOUNDRIES, EQUIPMENT, ALL_SEMIS
INDUSTRY_NAME = "FABLESS DESIGNERS"
```

## ⚖️ Configure Weights

Edit `SEMIS_SCORING_WEIGHTS` in `main.py`:

```python
SEMIS_SCORING_WEIGHTS = {
    'ev_to_fcf': 0.15,
    'revenue_cagr': 0.15,
    'operating_margin': 0.15,
    'fcf_margin': 0.15,
    'net_debt_to_ebitda': 0.10,
    'interest_coverage': 0.10,
    'roic': 0.10,             # Semis addon
    'gross_margin': 0.05,     # Semis addon
    'capex_intensity': 0.03,  # Semis addon
    'inventory_turnover': 0.02,  # Semis addon
}
```

## 📊 Available Watchlists

- `FABLESS`: 14 fabless designers (NVDA, AMD, QCOM, AVGO, MRVL, MPWR, etc.)
- `FOUNDRIES`: 2 foundries (TSM, UMC)
- `EQUIPMENT`: 14 equipment makers (ASML, LRCX, KLAC, AMAT, etc.)
- `IDMS`: 18 integrated manufacturers (INTC, TXN, NXPI, STM, etc.)
- `ALL_SEMIS`: ~50 semiconductor stocks
- `BIG_TECH`: 11 big tech stocks

## 🔧 Development Workflow

1. **Test metrics**: `./tractatus/bin/python3 -m utils.test_metrics`
2. **Cache data**: `./tractatus/bin/python3 -m utils.cache_results --save --tickers NVDA AMD`
3. **Test scoring**: Edit weights, run `./run_cmd.sh` (instant with cache)
4. **Refresh data**: `rm utils/cached_screening_results.json && ./run_cmd.sh`

## 📝 Core Metrics (6)

1. **EV/FCF** - Valuation (lower is better)
2. **Revenue CAGR** - Growth (higher is better)
3. **Operating Margin** - Efficiency (higher is better)
4. **FCF Margin** - Cash generation (higher is better)
5. **Net Debt/EBITDA** - Leverage (lower is better)
6. **Interest Coverage** - Debt safety (higher is better)

## 🔬 Semis Addon Metrics (4)

1. **ROIC** - Capital efficiency (higher is better)
2. **Gross Margin** - Pricing power (higher is better)
3. **CapEx Intensity** - Capital efficiency (lower is better)
4. **Inventory Turnover** - Cycle management (higher is better)
