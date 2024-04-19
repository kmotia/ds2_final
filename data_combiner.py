# Define the range of indices covering the spatial region around the USA
y_start, y_end = <start_index>, <end_index>
x_start, x_end = <start_index>, <end_index>

total_emissions = 0

# Iterate over each time step in the dataset
for time_step in range(num_time_steps):
    # Iterate over the spatial region around the USA
    for y_index in range(y_start, y_end + 1):
        for x_index in range(x_start, x_end + 1):
            # Accumulate emissions value
            total_emissions += BCEMAN[time_step][y_index][x_index]

# At this point, total_emissions will contain the sum of emissions for the entire month
