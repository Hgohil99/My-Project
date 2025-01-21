# importing pandas library
import pandas as pd

# loading dataset
data = pd.read_csv("ecommerce_data.csv")

# diaplaying the few rows of dataset
print("Dataset Preview:")

# head shows quickly shows the first 5 row and data.tails show us last row so we can quickly varify it
print(data.head())