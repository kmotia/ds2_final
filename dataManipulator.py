import os
data_name = 'OCEMAN'

# Define the folder containing your files
folder_path = f'{data_name}_files/'

# Initialize lists to store years, months, and monthly sums
data = []

# Loop through each file in the folder
for file_name in os.listdir(folder_path):
    if file_name.endswith('.txt') and file_name.startswith(f'{data_name}_'):
        # Extract year and month from the file name
        year = int(file_name[-10:-6])            # [-10:-6]        # **** MODIFY THIS TO ALLOW SO4EMAN to work
        month = int(file_name[-6:-4])          # [-6:-4]         # **** MODIFY THIS TO ALLOW SO4EMAN to work
        if 1980 <= year <= 2023:
            # Read the file and extract data
            file_path = os.path.join(folder_path, file_name)
            with open(file_path, 'r') as file:
                # Skip first row and last 3 rows
                lines = file.readlines()[1:-3]
                # Sum the values for each month
                monthly_sum = sum(sum(map(float, line.strip().split(',')[1:])) for line in lines)
            
            # Append the results to the list of tuples
            data.append((year, month, monthly_sum))

# Sort the data based on year and month
data.sort()

# Printing the results
for year, month, monthly_sum in data:
    print(f"Year: {year}, Month: {month}, Monthly Sum: {monthly_sum}")

