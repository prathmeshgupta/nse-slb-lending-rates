import re
import pandas as pd
from pathlib import Path

ISO_REGEX = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def audit_quality():
    print("=" * 65)
    print(" NSE SECURITIES LENDING & BORROWING (SLB) - DATA QUALITY AUDIT")
    print("=" * 65)

    root = Path(__file__).parent
    pq_path = root / "output" / "slb_market_dynamics.parquet"
    csv_path = root / "output" / "slb_market_dynamics.csv"

    assert pq_path.exists(), "slb_market_dynamics.parquet missing"
    assert csv_path.exists(), "slb_market_dynamics.csv missing"

    df_pq = pd.read_parquet(pq_path)
    df_csv = pd.read_csv(csv_path)

    # 1. Parity Check
    assert len(df_pq) == len(df_csv), f"Parity mismatch: Parquet ({len(df_pq)}) != CSV ({len(df_csv)})"
    print(f"Total SLB Transactions Indexed: {len(df_pq)} [PASS - 100% Parity]")

    # 2. Null Checks
    null_count = df_pq.isnull().sum().sum()
    assert null_count == 0, f"Found {null_count} nulls across table"
    print("Null Values: 0 across all columns [100% COMPLETE]")

    # 3. ISO-8601 Format
    s = df_pq["trade_date"].astype(str)
    invalid = s[~s.str.match(ISO_REGEX)]
    assert len(invalid) == 0, f"Non-ISO dates detected: {len(invalid)}"
    print("ISO-8601 Compliance (trade_date): 100% PASS")

    # 4. Domain Invariants
    assert (df_pq["borrowed_qty"] > 0).all(), "Non-positive borrowed quantity"
    assert (df_pq["lending_fee_inr"] >= 0).all(), "Negative lending fee"
    assert (df_pq["market_price_inr"] > 0).all(), "Non-positive market price"
    assert (df_pq["annualized_lending_yield_pct"] >= 0).all(), "Negative lending yield"
    print("Domain Bounds (Positive quantities, prices, and yields): [PASS]")

    # 5. Math Identity
    calc_val = ((df_pq["borrowed_qty"] * df_pq["market_price_inr"]) / 100000).round(2)
    assert (df_pq["borrowed_value_lakhs"] == calc_val).all(), "Borrowed value math mismatch"
    print("Transaction Value Math Identity: [PASS]")

    # 6. High Short Interest Securities
    high_short = df_pq[df_pq["short_conviction_tier"] == "HIGH_SHORT_INTEREST"]
    print("\nSecurities with Highest Annualized Lending Yield (Short Conviction):")
    for _, row in high_short.drop_duplicates(subset=["symbol"]).iterrows():
        print(f"  • {row['symbol']:<12}: Borrow Yield = {row['annualized_lending_yield_pct']}% | Borrowed = {row['borrowed_qty']:,} shares")

    print("=" * 65)
    print("ALL AUDIT CHECKS PASSED.")
    print("=" * 65)


if __name__ == "__main__":
    audit_quality()
