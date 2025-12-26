# User Metrics Data

## Overview
This directory contains curated user metrics (DAU/MAU/subscribers) for calculating ARPU Growth.

## File: `user_metrics.csv`

**Schema:**
- `ticker`: Stock symbol (e.g., META, SNAP, PINS)
- `year`: Calendar year (YYYY)
- `revenue`: Annual revenue in USD
- `active_users`: User count (units vary by company)
- `user_metric_type`: Type of user metric (DAP/DAU/MAU/Subscribers)
- `source_url`: Link to investor relations page or filing
- `notes`: Additional context

**Data Sources:**
- **Meta (META)**: Family daily active people (DAP) from quarterly earnings
  - Source: https://investor.fb.com/financials/
  - Updated quarterly
- **Snap (SNAP)**: Daily active users (DAU) from earnings letters
  - Source: https://investor.snap.com/financials/
  - Updated quarterly
- **Pinterest (PINS)**: Monthly active users (MAU) from shareholder letters
  - Source: https://investor.pinterestinc.com/financials/
  - Updated quarterly
- **Google (GOOGL)**: Not available (Google does not publicly report ad platform user counts)

## Usage

The `YFinanceProvider.get_user_metrics_data()` method automatically loads from this CSV:
1. If ticker found in CSV → returns revenues and user counts from file
2. If ticker not found → falls back to yfinance (revenues only, users = None)

## Updating Data

**Quarterly updates:**
1. Visit investor relations pages (links above)
2. Find latest quarterly earnings presentation or shareholder letter
3. Extract user count from "Key Metrics" or "Operational Highlights" section
4. Add new row to CSV with year, revenue, and user count
5. Verify revenue matches yfinance income statement

**Important notes:**
- Use each company's own metric definition (don't convert DAU to MAU or vice versa)
- ARPU Growth measures within-company improvement, not cross-company comparison
- The scorer normalizes growth rates after calculation, making different user metrics comparable

## Example: Updating for Q4 2024

```csv
META,2024,150000000000,3200000000,DAP,https://investor.fb.com/financials/,Family DAP Q4 2024
```

Extract from earnings:
- Revenue: $150B (from 10-K or yfinance)
- Family DAP: 3.2B (from earnings presentation slide 3)
