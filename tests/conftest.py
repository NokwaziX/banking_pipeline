"""
Shared test fixtures for the fraud detection pipeline tests.

"""

import pandas as pd
import pytest


@pytest.fixture
def sample_transactions():

    """
    Returns a small, complete transaction table with 6 rows: 3 fraud,
    3 not, spread across two months and two merchant categories.

    Used to test Clean and Transform, where the data is expected to
    be complete and well-formed.
    """

    data = {
        "transaction_id": [1, 2, 3, 4, 5, 6],
        "customer_id": [101, 102, 103, 104, 105, 106],
        "transaction_timestamp": [
            "2024-01-01", "2024-01-02", "2024-01-03",
            "2024-02-01", "2024-02-02", "2024-02-03"
        ],
        "amount": [100.0, 200.0, 50.0, 300.0, 150.0, 400.0],
        "merchant_category": [
            "groceries", "electronics", "groceries",
            "electronics", "groceries", "electronics"
        ],
        "is_fraud": [0, 1, 0, 1, 0, 1],
        "year": [2024, 2024, 2024, 2024, 2024, 2024],
        "month": [1, 1, 1, 2, 2, 2]
    }
    return pd.DataFrame(data)


@pytest.fixture
def transactions_with_missing_values(sample_transactions):

    """
    Same as sample_transactions, but with two blank values inserted:
    one in "amount", one in "merchant_category".

    Used to test that check_missing_values() finds them.
    """

    transactions = sample_transactions.copy()
    transactions.loc[0, "amount"] = None
    transactions.loc[2, "merchant_category"] = None
    return transactions


@pytest.fixture
def transactions_missing_columns(sample_transactions):

    """
    Same as sample_transactions, but with the "is_fraud" and "year"
    columns removed entirely.

    Used to test that check_missing_columns() finds them.
    """

    return sample_transactions.drop(columns=["is_fraud", "year"])