import os
import pandas as pd

# data_names = ['BCEMAN', 'OCEMAN', 'SO2EMAN', 'SO4EMAN']
data_names = ['BCEMAN', 'OCEMAN', 'SO2EMAN', 'SO4EMAN']
for data_name in data_names:
    folder_path = f'{data_name}_files/'

    # Initialize lists to store years, months, and monthly sums
    years = []
    months = []
    monthly_sums = []

    # Loop through each file in the folder
    for file_name in os.listdir(folder_path):

        if file_name.endswith('.txt') and file_name.startswith(f'{data_name}_'):
            # Extract year and month from the file name
            year = int(file_name[-10:-6])  # [-10:-6]        
            month = int(file_name[-6:-4])  # [-6:-4]        
            if 1980 <= year <= 2023:


                # Read the file and extract data
                file_path = os.path.join(folder_path, file_name)
                with open(file_path, 'r') as file:

                    lines = file.readlines()[1:-3]
                    # Sum the values for each month
                    monthly_sum = sum(sum(map(float, line.strip().split(',')[1:])) for line in lines)

                # Append tolists
                years.append(year)
                months.append(month)
                monthly_sums.append(monthly_sum)

    # Create a df
    df = pd.DataFrame({
        'Year': years,
        'Month': months,
        f'Monthly Sum': monthly_sums
    })

    # Making sure it's all correctly formatted
    df.sort_values(by=['Year', 'Month'], inplace=True)
    df.reset_index(drop=True, inplace=True) 
    csv_file_path = f'{data_name}_ts.csv'
    df.to_csv(csv_file_path, index=False)
