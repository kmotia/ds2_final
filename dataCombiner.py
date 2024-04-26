# import pandas as pd
# import matplotlib.pyplot as plt


# # Load each CSV file into a DataFrame
# BCEMAN_df = pd.read_csv('BCEMAN_ts.csv')
# OCEMAN_df = pd.read_csv('OCEMAN_ts.csv')
# SO2EMAN_df = pd.read_csv('SO2EMAN_ts.csv')
# SO4EMAN_df = pd.read_csv('SO4EMAN_ts.csv')

# # Merge the DataFrames on 'Year' and 'Month' columns
# merged_df = BCEMAN_df.merge(OCEMAN_df, on=['Year', 'Month']).merge(SO2EMAN_df, on=['Year', 'Month']).merge(SO4EMAN_df, on=['Year', 'Month'])
# print(merged_df)

# # Save the merged DataFrame to a new CSV file
# merged_df.to_csv('all_ts.csv', index=False)

# # ----------------- Plot each pollutant as a function of time at a monthly resolution ----------------- 
# # Create a time index by combining 'Year', 'Month', and a placeholder 'day' component
# merged_df['Date'] = pd.to_datetime(merged_df[['Year', 'Month']].assign(day=1))

# # Plot each pollutant as a function of time
# plt.figure(figsize=(10, 6))

# plt.plot(merged_df['Date'], merged_df['BCEMAN Monthly Sum'], label='BCEMAN')
# plt.plot(merged_df['Date'], merged_df['OCEMAN Monthly Sum'], label='OCEMAN')
# plt.plot(merged_df['Date'], merged_df['SO2EMAN Monthly Sum'], label='SO2EMAN')
# plt.plot(merged_df['Date'], merged_df['SO4EMAN Monthly Sum'], label='SO4EMAN')

# plt.xlabel('Time')
# plt.ylabel('Pollutant Flux Density ($kg \cdot m^{-2} \cdot s^{-1}$)')
# plt.title('Pollutant Monthly Sum Over Time')
# plt.legend()
# plt.grid(True)

# plt.show()

# # ----------------- Plot each pollutant as a function of time at a quarterly resolution ----------------- 

# # Download the profit data and plot it 


'''
I don't think we need this file. 

'''