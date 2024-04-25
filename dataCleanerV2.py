import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.dates as mdates
from statsmodels.tsa.stattools import grangercausalitytests
import cpi

#################### Preprocess emissions data ####################

# Read in raw year-month CSVs
BCE_df = pd.read_csv('BCEMAN_ts.csv')
OCE_df = pd.read_csv('OCEMAN_ts.csv')
SO2E_df = pd.read_csv('SO2EMAN_ts.csv')
SO4E_df = pd.read_csv('SO4EMAN_ts.csv')

# Function to turn year-month into a date
def get_pollutants_dates(df):
    df['Date'] = pd.to_datetime(df[['Year', 'Month']].assign(day=1))
    df = df.drop(columns=['Year', 'Month'])
    df = df[['Date'] + [col for col in df.columns if col != 'Date']]
    return df

# Turn year-month into dates
BCE_df = get_pollutants_dates(BCE_df)
OCE_df = get_pollutants_dates(OCE_df)
SO2E_df = get_pollutants_dates(SO2E_df)
SO4E_df = get_pollutants_dates(SO4E_df)

# Function to aggregate monthly data to quarterly data
def aggregate_months(df):
    # Group by year and calculate the sum for every 3 consecutive months
    df['Year'] = df['Date'].dt.year
    df['Month'] = df['Date'].dt.month
    df['Group'] = (df['Month'] - 1) // 3                                                        # Identify the group for each month    
    df = df.groupby(['Year', 'Group'], as_index=False)['Monthly Sum'].sum()                     # Group by year and group number, then calculate the sum
    df['Month'] = df['Group'] * 3 + 1                                                           # Convert group number back to month
    df['Date'] = pd.to_datetime(df['Year'].astype(str) + '-' + df['Month'].astype(str) + '-01') # Combine year and month to create the Date column
    df = df[['Date', 'Monthly Sum']]                                                            # Reorder columns 
    df.rename(columns={'Monthly Sum': 'Emissions'}, inplace=True)
    return df

# Aggregate monthly data to quarterly data
BCE_df = aggregate_months(BCE_df)
OCE_df = aggregate_months(OCE_df)
SO2E_df = aggregate_months(SO2E_df)
SO4E_df = aggregate_months(SO4E_df)

# Output CSVs with dates and quarterly emissions
BCE_df.to_csv('clean_BCEMAN_ts.csv', index=False)
OCE_df.to_csv('clean_OCEMAN_ts.csv', index=False)
SO2E_df.to_csv('clean_SO2EMAN_ts.csv', index=False)
SO4E_df.to_csv('clean_SO4EMAN_ts.csv', index=False)

#################### Plot emissions data ####################

# Plot each pollutant as a function of time
plt.figure(figsize=(10, 6))

# plt.plot(BCE_df['Date'], BCE_df['Emissions'], label='BCEMAN')
# plt.plot(OCE_df['Date'], OCE_df['Emissions'], label='OCEMAN')
plt.plot(SO2E_df['Date'], SO2E_df['Emissions'], label='SO2EMAN')
# plt.plot(SO4E_df['Date'], SO4E_df['Emissions'], label='SO4EMAN')

plt.xlabel('Time')
plt.ylabel('Pollutant Flux Density ($kg \cdot m^{-2} \cdot s^{-1}$)')
plt.title('Pollutant Quarterly Emissions Over Time')
plt.legend()
plt.grid(True)

plt.show()


#################### Preprocess FRED data ####################
def adjust_for_inflation(df):
    # Ensure 'Date' column is set as datetime
    df['Date'] = pd.to_datetime(df['Date'])

    # Determine the name of the second column
    second_column = df.columns[1]

    # Adjust values in the second column for inflation
    for i, row in df.iterrows():
        year = row['Date'].year
        adjusted_value = cpi.inflate(row[second_column], year)      # Adjusts for inflation using a benchmark year --> (Most recent completed year for this project is 2023)
        df.at[i, second_column] = adjusted_value
    return df

profit_df = pd.read_csv('raw_profit_ts.csv')
profit_df.rename(columns={'DATE': 'Date'}, inplace=True)
profit_df.rename(columns={'A053RC1Q027SBEA': 'Profit'}, inplace=True)
# profit_df['Date'] = pd.to_datetime(profit_df['Date'])                     # Convert to datetime format
profit_df = adjust_for_inflation(profit_df)



# Repeat for every FRED CSV file









#################### Plot FRED data ####################
# Plot each pollutant as a function of time
plt.figure(figsize=(10, 6))

plt.plot(profit_df['Date'], profit_df['Profit'], label='National Corporate Profit')

plt.xlabel('Time')
plt.ylabel('Billions of Dollars')
plt.title('Profit Over Time')
plt.legend()
plt.grid(True)

# Set locator and formatter for the x-axis ticks
plt.gca().xaxis.set_major_locator(mdates.YearLocator(base=5))
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y'))

plt.show()


