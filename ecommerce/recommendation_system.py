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

# Verifying the dataset
print("Dataset Dimensions:", data.shape)
print("Column Names:", data.columns)
print("Data Types:")
print(data.dtypes)

# Checking for missing values
print("Missing Values:")
print(data.isnull().sum())

# Handling duplicates
print("Duplicate Rows:", data.duplicated().sum())
data = data.drop_duplicates()

# Saving the cleaned dataset
data.to_csv("cleaned_ecommerce_data.csv", index=False)
print("Cleaned dataset saved as cleaned_ecommerce_data.csv")