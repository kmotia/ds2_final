import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.dates as mdates
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
    df['Month'] = df['Date'].dt.month                                                           # Checking for a bug...
    df['Group'] = (df['Month'] - 1) // 3                                                        # Identify the group for each month    
    df = df.groupby(['Year', 'Group'], as_index=False)['Monthly Sum'].sum()                     # Group by year and group number, then calculate the sum
    df['Month'] = df['Group'] * 3 + 1                                                           # Convert group number back to month
    df['Date'] = pd.to_datetime(df['Year'].astype(str) + '-' + df['Month'].astype(str) + '-01') # Combine year and month to create the Date column
    df = df[['Date', 'Monthly Sum']]                                                            # Reorder columns 
    df.rename(columns={'Monthly Sum': 'Emissions'}, inplace=True)
    df.set_index('Date', inplace=True)                                                          # Set Date as index
    return df

# Aggregate monthly data to quarterly data
BCE_df = aggregate_months(BCE_df)
OCE_df = aggregate_months(OCE_df)
SO2E_df = aggregate_months(SO2E_df)
SO4E_df = aggregate_months(SO4E_df)

# Output CSVs with dates and quarterly emissions
BCE_df.to_csv('clean_BCEMAN_ts.csv', index=True)
OCE_df.to_csv('clean_OCEMAN_ts.csv', index=True)
SO2E_df.to_csv('clean_SO2EMAN_ts.csv', index=True)
SO4E_df.to_csv('clean_SO4EMAN_ts.csv', index=True)

# Explicitly output SO2 as the target csv file
targets_df = SO2E_df.copy()
target_names = ['SO2']
targets_df.columns = target_names
# Explicitly state which one is the predictor
targets_df.to_csv('targets.csv', index=True)                       


#################### Plot emissions data ####################

# Plot each pollutant as a function of time
plt.figure(figsize=(10, 6))

plt.plot(BCE_df.index, BCE_df['Emissions'], label='BCEMAN')
plt.plot(OCE_df.index, OCE_df['Emissions'], label='OCEMAN')
plt.plot(SO2E_df.index, SO2E_df['Emissions'], label='SO2EMAN')
plt.plot(SO4E_df.index, SO4E_df['Emissions'], label='SO4EMAN')

plt.xlabel('Time')
plt.ylabel('Pollutant Flux Density ($kg \cdot m^{-2} \cdot s^{-1}$)')
plt.title('Pollutant Quarterly Emissions Over Time')
plt.legend()
plt.grid(True)

plt.show()


#################### Preprocess FRED data ####################
def adjust_for_inflation(df):
    # Determine the name of the feature column
    feature_column = df.columns[0]


    # Adjust values in the feature column for inflation
    for date, value in df.iterrows():
        year = date.year
        adjusted_value = cpi.inflate(value[feature_column], year, to=2023)
        df.at[date, feature_column] = adjusted_value

    return df

def adjust_index_base_year(df):
    # Filter data for the year 2023
    df_2023 = df[df.index.year == 2023]
    
    # Calculate average of "IP Index" values for the year 2023
    avg_2023 = df_2023["IP Index"].mean()
    # Calculate Conversion Factor
    conversion_factor = 100 / avg_2023



    # Multiply IP Index vals by teh Conversion Factor
    df["IP Index"] = df["IP Index"] * conversion_factor

    return df



# Rename columns. Adjust index or adjust for inflation for appropriate features
autoGas_df = pd.read_csv('raw_predictor_files/IP_autoGas.csv')
autoGas_df.columns.values[0] = 'Date'
autoGas_df.columns.values[1] = 'IP Index'
autoGas_df['Date'] = pd.to_datetime(autoGas_df['Date'])
autoGas_df.set_index('Date', inplace=True)
autoGas_df = adjust_index_base_year(autoGas_df)                 # Adjust index base year to 2023 = 100

manufacturing_df = pd.read_csv('raw_predictor_files/IP_manufacturing.csv')
manufacturing_df.columns.values[0] = 'Date'
manufacturing_df.columns.values[1] = 'IP Index'
manufacturing_df['Date'] = pd.to_datetime(manufacturing_df['Date'])
manufacturing_df.set_index('Date', inplace=True)
manufacturing_df = adjust_index_base_year(manufacturing_df)      # Adjust index base year to 2023 = 100

PC_df = pd.read_csv('raw_predictor_files/IP_petrolCoal.csv')
PC_df.columns.values[0] = 'Date'
PC_df.columns.values[1] = 'IP Index'
PC_df['Date'] = pd.to_datetime(PC_df['Date'])
PC_df.set_index('Date', inplace=True)
PC_df = adjust_index_base_year(PC_df)                            # Adjust index base year to 2023 = 100

profit_df = pd.read_csv('raw_predictor_files/profit_corp.csv')
profit_df.columns.values[0] = 'Date'
profit_df.columns.values[1] = 'Profit'
profit_df['Date'] = pd.to_datetime(profit_df['Date'])
profit_df.set_index('Date', inplace=True)
profit_df = adjust_for_inflation(profit_df)                         # Adjust for inflation

workingPop_df = pd.read_csv('raw_predictor_files/working_pop.csv')
workingPop_df.columns.values[0] = 'Date'
workingPop_df.columns.values[1] = 'Working Population'
workingPop_df['Date'] = pd.to_datetime(workingPop_df['Date'])
workingPop_df.set_index('Date', inplace=True)
                                                                    # No adjustments necessary. Units are "number of people"


# Merge the predictor dfs and output it as a CSV
predictors_df = pd.concat([autoGas_df, manufacturing_df, PC_df, profit_df, workingPop_df], axis=1)
predictor_names = ['Auto Gas', 'Manufacturing', 'Petrol Coal', 'Profit', 'Working Population']
predictors_df.columns = predictor_names
predictors_df.to_csv('predictors.csv', index=True)

print(predictors_df)


