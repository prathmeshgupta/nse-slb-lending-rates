# NSE Securities Lending & Borrowing (SLB) Market Dataset

[![Weekly Update](https://github.com/prathmeshgupta/nse-slb-lending-rates/actions/workflows/update.yml/badge.svg)](https://github.com/prathmeshgupta/nse-slb-lending-rates/actions/workflows/update.yml)
[![Format: Parquet](https://img.shields.io/badge/Format-Apache%20Parquet-blue.svg)](output/slb_market_dynamics.parquet)
[![Format: CSV](https://img.shields.io/badge/Format-CSV-green.svg)](output/slb_market_dynamics.csv)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

An institutional quantitative dataset capturing official **Securities Lending and Borrowing (SLB)** market transactions, borrowed share quantities, lending fees, and calculated **annualized lending yields (the purest empirical proxy for Indian short interest)**.

In Indian equity markets where naked short-selling is strictly banned, institutional short sellers must borrow shares through the clearing corporation's SLB mechanism. A surge in annualized lending yields indicates high hard-to-borrow short conviction or potential impending short squeeze dynamics.

---

## Dataset Schema (`output/slb_market_dynamics.parquet` / `.csv`)

| Field Name | Type | Description |
| :--- | :--- | :--- |
| `trade_date` | `string` | ISO-8601 Transaction Date (`YYYY-MM-DD`) |
| `symbol` | `string` | NSE Listed Equity Ticker (e.g. `PAYTM`, `ADANIENT`, `RELIANCE`) |
| `series` | `string` | Series identifier (`EQ`, `IL`, `SL`) |
| `borrowed_qty` | `int64` | Total volume of equity shares borrowed |
| `lending_fee_inr` | `float64` | Lending fee per share in INR paid by the borrower |
| `market_price_inr` | `float64` | Underlying closing market price per share |
| `tenor_days` | `int64` | Borrow contract duration in calendar days (typically 30D / 1M) |
| `borrowed_value_lakhs` | `float64` | Total monetary value of borrowed position in INR Lakhs |
| `annualized_lending_yield_pct` | `float64` | Annualized cost of borrowing ($\frac{\text{Lending Fee}}{\text{Price}} \times \frac{365}{\text{Tenor}} \times 100$) |
| `short_conviction_tier` | `string` | Classification: `HIGH_SHORT_INTEREST`, `MODERATE_SHORT`, `NORMAL` |
| `source` | `string` | Data source identifier (`NSE_SLB_REPORTS`) |

---

## Quick Start (Python / Polars / DuckDB)

```python
import polars as pl

# Read directly from GitHub Raw Parquet
url = "https://github.com/prathmeshgupta/nse-slb-lending-rates/raw/main/output/slb_market_dynamics.parquet"
df = pl.read_parquet(url)

# Screen for high short conviction (> 5% annualized borrow yield)
high_conviction = df.filter(pl.col("annualized_lending_yield_pct") >= 5.0)
print(high_conviction.select(["trade_date", "symbol", "borrowed_qty", "annualized_lending_yield_pct", "short_conviction_tier"]))
```
