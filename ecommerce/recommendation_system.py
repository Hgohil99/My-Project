# importing pandas library to manipulate and transform the data in python
import pandas as pd

# loading dataset
data = pd.read_csv("ecommerce_data.csv")

# diaplaying the few rows of dataset
print("Dataset Preview:")

# data.head shows quickly shows the first 5 row and data.tails show us last row so we can quickly varify it
print(data.head())

# View the column names
print("Column Names:", data.columns)

# checking data types
print("Data Types:", data.dtypes)
