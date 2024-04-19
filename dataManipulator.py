import os

# Define the folder containing your files
folder_path = 'BCEMAN_files/'

# Initialize lists to store years, months, and monthly sums
BCEMAN_data = []

# Loop through each file in the folder
for file_name in os.listdir(folder_path):
    if file_name.endswith('.txt') and file_name.startswith('BCEMAN_'):
        # Extract year and month from the file name
        year = int(file_name[7:11])
        month = int(file_name[11:13])
        if 1980 <= year <= 2023:
            # Read the file and extract data
            file_path = os.path.join(folder_path, file_name)
            with open(file_path, 'r') as file:
                # Skip first row and last 3 rows
                lines = file.readlines()[1:-3]
                # Sum the values for each month
                monthly_sum = sum(sum(map(float, line.strip().split(',')[1:])) for line in lines)
            
            # Append the results to the list of tuples
            BCEMAN_data.append((year, month, monthly_sum))

# Sort the data based on year and month
BCEMAN_data.sort()

# Printing the results
for year, month, monthly_sum in BCEMAN_data:
    print(f"Year: {year}, Month: {month}, Monthly Sum: {monthly_sum}")

