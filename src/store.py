"""
This file is the STORE step of the fraud detection pipeline.

It runs Collect, Clean, and Transform in order, then saves the result:
the transaction data goes to a staging CSV, and a summary of the run
(row counts, missing data, fraud stats) goes to a JSON log file.
"""

import os
import json
from datetime import datetime

from collect import load_transactions
from clean import check_missing_columns, check_missing_values
from transform import build_summary
from config import RAW_SAMPLE_PATH, STAGING_PATH, STAGING_FILE, LOG_PATH


def save_staged_data(transactions):

    """
    Saves the transaction table to the staging folder as a CSV file.

    transactions: the loaded transaction table.

    Returns the path the file was saved to.
    """

    os.makedirs(STAGING_PATH, exist_ok=True)
    transactions.to_csv(STAGING_FILE, index=False)
    return STAGING_FILE


def build_log(transactions, missing_columns, missing_values_total, summary):

    """
    Builds a summary of the pipeline run to save as a log.

    transactions: the loaded transaction table.
    missing_columns: list of expected columns that were missing.
    missing_values_total: count of missing values per column.
    summary: the dictionary of fraud stats from the Transform step.

    Returns a dictionary describing what happened during this run.
    """

    log = {
        "run_timestamp": datetime.now().isoformat(),
        "source_file": RAW_SAMPLE_PATH,
        "total_rows": len(transactions),
        "missing_columns": missing_columns,
        "missing_values_per_column": missing_values_total.to_dict(),
        "fraud_rate_percent": summary["fraud_rate_percent"],
        "average_fraud_amount": summary["average_fraud_amount"],
        "average_non_fraud_amount": summary["average_non_fraud_amount"],
        "status": "WARNING" if missing_columns else "SUCCESS"
    }
    return log


def save_log(log):

    """
    Saves the run log to the staging folder as a JSON file.

    log: the dictionary built by build_log().

    Returns the path the log was saved to.
    """

    os.makedirs(STAGING_PATH, exist_ok=True)
    with open(LOG_PATH, "w") as f:
        json.dump(log, f, indent=2)
    return LOG_PATH


if __name__ == "__main__":
    transactions = load_transactions(RAW_SAMPLE_PATH)

    missing_columns = check_missing_columns(transactions)
    missing_values_total = check_missing_values(transactions)
    summary = build_summary(transactions)

    staged_path = save_staged_data(transactions)
    log = build_log(transactions, missing_columns, missing_values_total, summary)
    log_path = save_log(log)

    print(f"Staged data saved to: {staged_path}")
    print(f"Run log saved to: {log_path}")