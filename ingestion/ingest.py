import pandas as pd
import os
import json
from datetime import datetime

RAW_PATH = "data/raw/transactions.csv"
STAGING_PATH = "data/staging"
LOG_PATH = "data/staging/ingestion_log.json"

EXPECTED_COLUMNS = [
    "step", "type", "amount", "nameOrig", "oldbalanceOrg",
    "newbalanceOrig", "nameDest", "oldbalanceDest",
    "newbalanceDest", "isFraud", "isFlaggedFraud"
]

def load_raw(path):
    print(f"[1/4] Reading raw file: {path}")
    df = pd.read_csv(path)
    print(f"      Loaded {len(df):,} rows and {len(df.columns)} columns.")
    return df

def validate(df):
    print("[2/4] Validating data...")
    issues = []

    missing_cols = [c for c in EXPECTED_COLUMNS if c not in df.columns]
    if missing_cols:
        issues.append(f"Missing columns: {missing_cols}")

    null_counts = df[EXPECTED_COLUMNS].isnull().sum()
    nulls = null_counts[null_counts > 0]
    if not nulls.empty:
        issues.append(f"Null values found: {nulls.to_dict()}")

    neg_amounts = (df["amount"] < 0).sum()
    if neg_amounts > 0:
        issues.append(f"Negative amounts: {neg_amounts} rows")

    if issues:
        for issue in issues:
            print(f"      WARNING: {issue}")
    else:
        print("      All checks passed.")

    return issues

def summarise(df):
    print("[3/4] Generating summary...")
    summary = {
        "ingestion_timestamp": datetime.now().isoformat(),
        "source_file": RAW_PATH,
        "total_rows": len(df),
        "total_columns": len(df.columns),
        "columns": list(df.columns),
        "transaction_types": df["type"].value_counts().to_dict(),
        "fraud_transactions": int(df["isFraud"].sum()),
        "fraud_rate_pct": round(df["isFraud"].mean() * 100, 4),
        "total_amount_transferred": round(df["amount"].sum(), 2),
        "date_steps_range": {
            "min_step": int(df["step"].min()),
            "max_step": int(df["step"].max())
        }
    }
    return summary

def save_staging(df, summary, issues):
    print("[4/4] Saving to staging...")
    os.makedirs(STAGING_PATH, exist_ok=True)

    staging_file = os.path.join(STAGING_PATH, "transactions_staged.csv")
    df.to_csv(staging_file, index=False)
    print(f"      Staged data saved to: {staging_file}")

    summary["validation_issues"] = issues
    summary["status"] = "WARNING" if issues else "SUCCESS"

    with open(LOG_PATH, "w") as f:
        json.dump(summary, f, indent=2)
    print(f"      Ingestion log saved to: {LOG_PATH}")

    return summary

def run():
    print("=" * 50)
    print("  SA Bank Pipeline — Phase 1: Ingestion")
    print("=" * 50)

    if not os.path.exists(RAW_PATH):
        print(f"\nERROR: File not found at '{RAW_PATH}'")
        print("Make sure transactions.csv is in data/raw/")
        return

    df = load_raw(RAW_PATH)
    issues = validate(df)
    summary = summarise(df)
    result = save_staging(df, summary, issues)

    print()
    print("--- Ingestion Summary ---")
    print(f"  Status            : {result['status']}")
    print(f"  Total rows        : {result['total_rows']:,}")
    print(f"  Fraud transactions: {result['fraud_transactions']:,} ({result['fraud_rate_pct']}%)")
    print(f"  Total amount (R)  : {result['total_amount_transferred']:,.2f}")
    print(f"  Transaction types : {result['transaction_types']}")
    print()
    print("Phase 1 complete. Ready for Phase 2 (load into PostgreSQL).")
    print("=" * 50)

if __name__ == "__main__":
    run()