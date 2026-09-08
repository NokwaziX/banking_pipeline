import pandas as pd

FILE_PATH = "C:/Users/DELL/Documents/ELECTIVE WORK/archive/transactions.csv"
ROWS_TO_PREVIEW = 5000

preview = pd.read_csv(FILE_PATH, nrows=ROWS_TO_PREVIEW)

print("Columns found:")
print(list(preview.columns))
print()
print("Data types:")
print(preview.dtypes)
print()
print("First 5 rows:")
print(preview.head())
print()
print("Any missing values in the preview:")
print(preview.isnull().sum())