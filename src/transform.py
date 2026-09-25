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

if __name__ == "__main__":
    transactions = load_transactions(RAW_SAMPLE_PATH)

    total_transactions = count_total_transactions(transactions)
    fraud_transactions = count_fraud_transactions(transactions)
    fraud_rate_percent = calculate_fraud_percent(total_transactions, fraud_transactions)

    print(f"Total transactions: {total_transactions}")
    print(f"Fraud transactions: {fraud_transactions}")
    print(f"Fraud rate: {fraud_rate_percent}%")


    fraud_transations_by_category = count_fraud_by_category(transactions)
    print("\nFraud transations by merhant category:")
    print(fraud_transations_by_category)

    fraud_transactions_by_month = count_fraud_by_month(transactions)
    print("\nFraud transactions by month:")
    print(fraud_transactions_by_month)

    average_fraud_amount = calculate_average_fraud_amount(transactions)
    print(f"\nAverage fraud transaction amount: {average_fraud_amount}")