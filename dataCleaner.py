import pandas as pd

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

# Output CSVs with dates
BCE_df.to_csv('clean_BCEMAN_ts.csv', index=False)
OCE_df.to_csv('clean_OCEMAN_ts.csv', index=False)
SO2E_df.to_csv('clean_SO2EMAN_ts.csv', index=False)
SO4E_df.to_csv('clean_SO4EMAN_ts.csv', index=False)


# # Load the cleaned CSV files for each pollutant
# BCE_df = pd.read_csv('clean_BCEMAN_ts.csv')
# OCE_df = pd.read_csv('clean_OCEMAN_ts.csv')
# SO2E_df = pd.read_csv('clean_SO2EMAN_ts.csv')
# SO4E_df = pd.read_csv('clean_SO4EMAN_ts.csv')


# Function to aggregate monthly data to quarterly data
def aggregate_months(df):
    # Group by year and calculate the sum for every 3 consecutive months
    df['Year'] = df['Date'].dt.year
    df['Month'] = df['Date'].dt.month
    df['Group'] = (df['Month'] - 1) // 3  # Identify the group for each month
    
    # Group by year and group number, then calculate the sum
    df = df.groupby(['Year', 'Group'], as_index=False)['Monthly Sum'].sum()
    
    # Convert group number back to month
    df['Month'] = df['Group'] * 3 + 1
    
    # Combine year and month to create the Date column
    df['Date'] = pd.to_datetime(df['Year'].astype(str) + '-' + df['Month'].astype(str) + '-01')
    
    # Reorder columns
    df = df[['Date', 'Monthly Sum']]

    return df

# Aggregate monthly data to quarterly data
BCE_df = aggregate_months(BCE_df)
OCE_df = aggregate_months(OCE_df)
SO2E_df = aggregate_months(SO2E_df)
SO4E_df = aggregate_months(SO4E_df)

