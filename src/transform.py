"""
This file is the TRANSFORM step of the fraud detection pipeline.

It takes the loaded transaction data and calculates summary numbers
from it.

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


def calculate_fraud_percent(total_transactions, fraud_transactions):
    """
    Calculates what percentage of transactions are fraud.

    total_transactions: the total number of transactions.
    fraud_transactions: how many of those are fraud.

    Returns the fraud rate as a percentage.
    """
    fraud_rate_percent = (fraud_transactions / total_transactions) * 100
    return fraud_rate_percent


def count_fraud_by_category(transactions):
    """
    Counts fraud transactions separately for each merchant category.

    transactions: the loaded transaction table.

    Returns a count of fraud transactions per merchant category,
    sorted from the highest count to the lowest.
    """
    is_fraud_column = transactions["is_fraud"]
    fraud_rows_only = is_fraud_column == 1

    fraud_only = transactions[fraud_rows_only]
    fraud_categories = fraud_only["merchant_category"]

    fraud_by_category = fraud_categories.value_counts()

    return fraud_by_category


def count_fraud_by_month(transactions):
    """
    Counts fraud transactions separately for each month.

    transactions: the loaded transaction table.

    Returns a count of fraud transactions per month, sorted from
    the highest count to the lowest.
    """
    is_fraud_column = transactions["is_fraud"]
    fraud_rows_only = is_fraud_column == 1

    fraud_only = transactions[fraud_rows_only]
    fraud_months = fraud_only["month"]

    fraud_by_month = fraud_months.value_counts()

    return fraud_by_month


def calculate_average_fraud_amount(transactions):
    """
    Calculates the average transaction amount for fraud transactions
    only.

    transactions: the loaded transaction table.

    Returns the average fraud transaction amount.
    """
    is_fraud_column = transactions["is_fraud"]
    amount_column = transactions["amount"]

    fraud_amount_total = 0
    fraud_transaction_count = 0

    row_position = 0
    for value in is_fraud_column:
        if value == 1:
            fraud_amount_total = fraud_amount_total + amount_column[row_position]
            fraud_transaction_count = fraud_transaction_count + 1
        row_position = row_position + 1

    average_fraud_amount = fraud_amount_total / fraud_transaction_count

    return average_fraud_amount


def calculate_average_non_fraud_amount(transactions):
    """
    Calculates the average transaction amount for non-fraud
    transactions only.

    transactions: the loaded transaction table.

    Returns the average non-fraud transaction amount.
    """
    is_fraud_column = transactions["is_fraud"]
    amount_column = transactions["amount"]

    non_fraud_amount_total = 0
    non_fraud_transaction_count = 0

    row_position = 0
    for value in is_fraud_column:
        if value == 0:
            non_fraud_amount_total = non_fraud_amount_total + amount_column[row_position]
            non_fraud_transaction_count = non_fraud_transaction_count + 1
        row_position = row_position + 1

    average_non_fraud_amount = non_fraud_amount_total / non_fraud_transaction_count

    return average_non_fraud_amount


def build_summary(transactions):
    """
    Runs every Transform calculation and gathers the results into
    one single package.

    transactions: the loaded transaction table.

    Returns a dictionary containing every summary number and table
    calculated by this file.
    """
    total = count_total_transactions(transactions)
    fraud_count = count_fraud_transactions(transactions)
    fraud_rate = calculate_fraud_percent(total, fraud_count)

    by_category = count_fraud_by_category(transactions)
    by_month = count_fraud_by_month(transactions)

    average_fraud = calculate_average_fraud_amount(transactions)
    average_non_fraud = calculate_average_non_fraud_amount(transactions)

    summary = {
        "total_transactions": total,
        "fraud_transactions": fraud_count,
        "fraud_rate_percent": fraud_rate,
        "fraud_by_category": by_category,
        "fraud_by_month": by_month,
        "average_fraud_amount": average_fraud,
        "average_non_fraud_amount": average_non_fraud
    }

    return summary


if __name__ == "__main__":
    transactions = load_transactions(RAW_SAMPLE_PATH)

    summary = build_summary(transactions)

    total = summary["total_transactions"]
    fraud_count = summary["fraud_transactions"]
    fraud_rate = summary["fraud_rate_percent"]
    by_category = summary["fraud_by_category"]
    by_month = summary["fraud_by_month"]
    average_fraud = summary["average_fraud_amount"]
    average_non_fraud = summary["average_non_fraud_amount"]

    print("\nTotal transactions:", total)
    print("Fraud transactions:", fraud_count)
    print(f"Fraud rate: {fraud_rate:.2f}%")

    print("\nFraud transactions by merchant category:")
    print(by_category)

    print("\nFraud transactions by month:")
    print(by_month)

    print(f"\nAverage fraud transaction amount: R{average_fraud:.2f}")
    print(f"Average non-fraud transaction amount: R{average_non_fraud:.2f}")