"""
This file is the CLEAN step of the fraud detection pipeline.

It checks the loaded transaction data for two kinds of problems:
missing columns, and missing (blank) values in any column. It does not
fix anything - it only reports what it finds, so a human decides what
to do about it.
"""
from collect import *

def check_missing_columns(transations):

    """
    Checks whether all expected columns are present in the data.

    transactions: the loaded transaction table.

    Returns a list of any expected columns that are missing. An empty
    list means nothing is missing.
    """
    actual_columns = list(transactions.columns)
    missing_columns = []

    for column in EXPECTED_COLUMNS:
        if column not in actual_columns:
            missing_columns.append(column)

    return missing_columns

def check_missing_values(transactions):

    """
    Checks each column for missing (blank) values.

    transactions: the loaded transaction table.

    Returns a count of missing values found in each column. A column
    showing 0 means nothing is missing there.
    """

    blank_or_not = transactions.isnull()
    missing_values_total = blank_or_not.sum()

    return missing_values_total


if __name__ == "__main__":
    transactions = load_transactions(RAW_SAMPLE_PATH)

    missing_columns = check_missing_columns(transactions)
    if len(missing_columns) > 0:
        print(f"Missing columns: {missing_columns}")
    else:
        print("No missing columns found.")

    missing_values_total = check_missing_values(transactions)
    print("Missing values per column:")
    print(missing_values_total)