import pandas as pd

# Load the datasets
median_income_df = pd.read_csv('/mnt/data/median_income.csv')
mortgage_rates_df = pd.read_csv('/mnt/data/MORTGAGE30US.csv')
home_prices_df = pd.read_csv('/mnt/data/MSPUS.csv')

# Convert the date columns to datetime
mortgage_rates_df['DATE'] = pd.to_datetime(mortgage_rates_df['DATE'])
home_prices_df['DATE'] = pd.to_datetime(home_prices_df['DATE'])
median_income_df['Date'] = pd.to_datetime(median_income_df['Date'])

# Resample the mortgage rates to annual data
annual_mortgage_rates = mortgage_rates_df.resample('Y', on='DATE').mean()

# Merge the datasets on the date column
merged_df = pd.merge_asof(median_income_df.sort_values('Date'), annual_mortgage_rates, left_on='Date', right_on='DATE')
merged_df = pd.merge_asof(merged_df, home_prices_df.sort_values('DATE'), left_on='Date', right_on='DATE')

# Monthly interest rate
merged_df['Monthly_Interest_Rate'] = merged_df['MORTGAGE30US'] / 100 / 12

# Total number of payments (360 for a 30-year mortgage)
n_payments = 30 * 12

# Monthly mortgage payment calculation
merged_df['Monthly_Mortgage_Payment'] = merged_df['MSPUS'] * (merged_df['Monthly_Interest_Rate'] * (1 + merged_df['Monthly_Interest_Rate'])**n_payments) / ((1 + merged_df['Monthly_Interest_Rate'])**n_payments - 1)

# Monthly interest payment calculation
merged_df['Monthly_Interest_Payment'] = (merged_df['MSPUS'] * (merged_df['MORTGAGE30US'] / 100)) / 12

# Total mortgage payment
merged_df['Total_Mortgage_Payment'] = merged_df['Monthly_Mortgage_Payment'] + merged_df['Monthly_Interest_Payment']

# Ratio of total mortgage payment to monthly median income
merged_df['Income_to_Total_Mortgage_Ratio'] = merged_df['Total_Mortgage_Payment'] / merged_df['Monthly_Median_Income']

# Display the final dataframe
final_df = merged_df[['Date', 'MORTGAGE30US', 'Monthly_Median_Income', 'Monthly_Interest_Payment', 'Monthly_Mortgage_Payment', 'Total_Mortgage_Payment', 'Income_to_Total_Mortgage_Ratio']]
