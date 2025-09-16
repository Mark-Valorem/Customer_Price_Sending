import pandas as pd

# This script helps you see what columns are in your Excel file
excel_file = r"C:\Users\MarkAnderson\Valorem\Knowledge Hub - Documents\Pricing\Customer Price Lists\Price Sheet Sending_Python\Python_CustomerPricing.xlsx"

print("Reading Excel file to check column names...")
df = pd.read_excel(excel_file)

print("\nYour Excel file has the following columns:")
for i, column in enumerate(df.columns, 1):
    print(f"{i}. '{column}'")

print(f"\nTotal number of rows: {len(df)}")
print("\nFirst few rows of data:")
print(df.head())