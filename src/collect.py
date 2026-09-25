"""
This file is the COLLECT step of the fraud detection pipeline.

Its only job is to open the transaction data file and confirm it loaded
correctly.

"""

import pandas as pd
from config import RAW_SAMPLE_PATH, EXPECTED_COLUMNS

def load_transactions(path):

    """
    Opens a transaction CSV file and returns its contents as a table.

    path: the location of the CSV file to open.

    Returns the loaded data, and also prints how many rows and columns
    were found, so a human can quickly confirm the file loaded properly.
    """


    print(f" ===================================== Reading transaction sample from: {path}. ===================================== ")

    transactions = pd.read_csv(path)
    number_of_rows = len(transactions)
    number_of_columns = len(transactions.columns)
  
    print(f"Loaded {number_of_rows} rows and {number_of_columns} columns.")

    return transactions

if __name__ == "__main__":
    transactions = load_transactions(RAW_SAMPLE_PATH)  
    print(transactions.tail(20))
