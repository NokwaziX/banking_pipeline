import pandas as pd

RAW_FILE_PATH = r"C:\Users\DELL\Documents\ELECTIVE WORK\archive\transactions.csv"
SAMPLE_OUTPUT_PATH = "data/raw/transactions_sample.csv"
CHUNK_SIZE = 200000
NON_FRAUD_SAMPLE_RATE = 0.05

fraud_rows = []
non_fraud_rows = []

for chunk in pd.read_csv(RAW_FILE_PATH, chunksize=CHUNK_SIZE):
    fraud_chunk = chunk[chunk["is_fraud"] == 1]
    non_fraud_chunk = chunk[chunk["is_fraud"] == 0].sample(frac=NON_FRAUD_SAMPLE_RATE, random_state=42)

    fraud_rows.append(fraud_chunk)
    non_fraud_rows.append(non_fraud_chunk)

sampled_data = pd.concat(fraud_rows + non_fraud_rows, ignore_index=True)
sampled_data = sampled_data.sort_values("transaction_timestamp").reset_index(drop=True)

sampled_data.to_csv(SAMPLE_OUTPUT_PATH, index=False)

print(f"Total rows in sample: {len(sampled_data):,}")
print(f"Fraud rows kept: {sampled_data['is_fraud'].sum():,}")
print(f"Fraud rate in sample: {round(sampled_data['is_fraud'].mean() * 100, 4)}%")