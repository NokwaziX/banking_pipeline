"""
Tests for the COLLECT step (src/collect.py).

These check that load_transactions() correctly reads a CSV file from
disk and returns it as a usable table, using a small temporary CSV
file instead of the real (large) dataset.
"""

import pandas as pd

from collect import load_transactions


def test_load_transactions_reads_all_rows(tmp_path):

    """
    Writes a small 3-row CSV to a temporary file, loads it with
    load_transactions(), and checks all 3 rows came back.
    """

    csv_path = tmp_path / "sample.csv"
    pd.DataFrame({
        "transaction_id": [1, 2, 3],
        "amount": [10.0, 20.0, 30.0]
    }).to_csv(csv_path, index=False)

    transactions = load_transactions(str(csv_path))

    assert len(transactions) == 3


def test_load_transactions_keeps_all_columns(tmp_path):

    """
    Checks that no columns get dropped or renamed while loading.
    """

    csv_path = tmp_path / "sample.csv"
    pd.DataFrame({
        "transaction_id": [1],
        "amount": [10.0],
        "merchant_category": ["groceries"]
    }).to_csv(csv_path, index=False)

    transactions = load_transactions(str(csv_path))

    assert list(transactions.columns) == [
        "transaction_id", "amount", "merchant_category"
    ]


def test_load_transactions_returns_a_dataframe(tmp_path):

    """
    Checks that the return type is a pandas DataFrame, since every
    later stage (Clean, Transform, Store) assumes it can call
    DataFrame methods on what load_transactions() gives back.
    """

    csv_path = tmp_path / "sample.csv"
    pd.DataFrame({"transaction_id": [1]}).to_csv(csv_path, index=False)

    transactions = load_transactions(str(csv_path))

    assert isinstance(transactions, pd.DataFrame)