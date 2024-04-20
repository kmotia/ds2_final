import os
import pandas as pd

# data_names = ['BCEMAN', 'OCEMAN', 'SO2EMAN', 'SO4EMAN']
data_names = ['BCEMAN', 'OCEMAN', 'SO2EMAN', 'SO4EMAN']
for data_name in data_names:
    # Define the folder containing your files
    folder_path = f'{data_name}_files/'

    # Initialize lists to store years, months, and monthly sums
    years = []
    months = []
    monthly_sums = []

    # Loop through each file in the folder
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.txt') and file_name.startswith(f'{data_name}_'):
            # Extract year and month from the file name
            year = int(file_name[-10:-6])  # [-10:-6]        # **** MODIFY THIS TO ALLOW SO4EMAN to work
            month = int(file_name[-6:-4])  # [-6:-4]         # **** MODIFY THIS TO ALLOW SO4EMAN to work
            if 1980 <= year <= 2023:
                # Read the file and extract data
                file_path = os.path.join(folder_path, file_name)
                with open(file_path, 'r') as file:
                    # Skip first row and last 3 rows
                    lines = file.readlines()[1:-3]
                    # Sum the values for each month
                    monthly_sum = sum(sum(map(float, line.strip().split(',')[1:])) for line in lines)

                # Append the results to the respective lists
                years.append(year)
                months.append(month)
                monthly_sums.append(monthly_sum)

    # Create a DataFrame
    df = pd.DataFrame({
        'Year': years,
        'Month': months,
        f'{data_name} Monthly Sum': monthly_sums
    })

    # Sort the DataFrame based on year and month
    df.sort_values(by=['Year', 'Month'], inplace=True)

    # Reset the index
    df.reset_index(drop=True, inplace=True)

    # Saving the DataFrame to a CSV file
    csv_file_path = f'{data_name}_summary.csv'
    df.to_csv(csv_file_path, index=False)
