import pandas as pd

RAW_SAMPLE_PATH = "data/raw/transactions_sample.csv"

EXPECTED_COLUMNS = [
    "transaction_id", "customer_id", "transaction_timestamp",
    "amount", "merchant_category", "is_fraud", "year", "month"
]

def load_transactions(path):
    print(f"Reading transaction sample from: {path}")
    transactions = pd.read_csv(path)
    print(f"Loaded {len(transactions):,} rows and {len(transactions.columns)} columns.")
    return transactions

if __name__ == "__main__":
    transactions = load_transactions(RAW_SAMPLE_PATH)
    print(transactions.head())