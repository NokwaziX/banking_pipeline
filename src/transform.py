"""
This file is the TRANSFORM step of the fraud detection pipeline.

It takes the loaded transaction data and calculates summary numbers
from it - things like the total fraud rate. It does not check for
problems (that's Clean's job) or save anything (that's Storage's job).
"""

"""
This file is the TRANSFORM step of the fraud detection pipeline.

It takes the loaded transaction data and calculates summary numbers
from it - things like the total fraud rate. It does not check for
problems (that's Clean's job) or save anything (that's Storage's job).
"""

from collect import load_transactions, RAW_SAMPLE_PATH


def count_total_transactions(transactions):
    """
    Counts how many transactions are in the data.

    transactions: the loaded transaction table.

    Returns the total number of transactions.
    """
    total_transactions = len(transactions)
    return total_transactions


def count_fraud_transactions(transactions):
    """
    Counts how many of the transactions are marked as fraud.

    transactions: the loaded transaction table.

    Returns the number of fraud transactions.
    """
    #fraud_transactions = transactions["is_fraud"].sum()
    fraud_column = transactions["is_fraud"]

    fraud_transactions = 0
    for value in fraud_column:
        if value == 1:
            fraud_transactions += 1
    return fraud_transactions


def calculate_fraud_rate_percent(total_transactions, fraud_transactions):
    """
    Calculates what percentage of transactions are fraud.

    total_transactions: the total number of transactions.
    fraud_transactions: how many of those are fraud.

    Returns the fraud rate as a percentage.
    """
    fraud_rate_percent = (fraud_transactions / total_transactions) * 100
    return fraud_rate_percent


if __name__ == "__main__":
    transactions = load_transactions(RAW_SAMPLE_PATH)

    total_transactions = count_total_transactions(transactions)
    fraud_transactions = count_fraud_transactions(transactions)
    fraud_rate_percent = calculate_fraud_rate_percent(total_transactions, fraud_transactions)

    print(f"Total transactions: {total_transactions}")
    print(f"Fraud transactions: {fraud_transactions}")
    print(f"Fraud rate: {fraud_rate_percent}%")