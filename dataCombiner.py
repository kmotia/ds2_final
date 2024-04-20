import pandas as pd

# Load each CSV file into a DataFrame
BCEMAN_df = pd.read_csv('BCEMAN_ts.csv')
OCEMAN_df = pd.read_csv('OCEMAN_ts.csv')
SO2EMAN_df = pd.read_csv('SO2EMAN_ts.csv')
SO4EMAN_df = pd.read_csv('SO4EMAN_ts.csv')

# Merge the DataFrames on 'Year' and 'Month' columns
merged_df = BCEMAN_df.merge(OCEMAN_df, on=['Year', 'Month']).merge(SO2EMAN_df, on=['Year', 'Month']).merge(SO4EMAN_df, on=['Year', 'Month'])
print(merged_df)

# Save the merged DataFrame to a new CSV file
merged_df.to_csv('all_ts.csv', index=False)

# Plot each pollutant as a function of time at a monthly resolution

# Plot each pollutant as a function of time at a quarterly resolution

# Download the profit data and plot it 

