"""
Shared settings for the fraud detection pipeline.

Keeping file paths and expected columns here means every stage
(collect, clean, transform, store) reads from one place, so a path
change only has to be made once.
"""

RAW_SAMPLE_PATH = "data/raw/transactions_sample.csv"
STAGING_PATH = "data/staging"
STAGING_FILE = "data/staging/transactions_staged.csv"
LOG_PATH = "data/staging/ingestion_log.json"

EXPECTED_COLUMNS = [
    "transaction_id", "customer_id", "transaction_timestamp",
    "amount", "merchant_category", "is_fraud", "year", "month"
]