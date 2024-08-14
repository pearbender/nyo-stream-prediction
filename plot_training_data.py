import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import sys

# Check if the number of days is provided as an argument
if len(sys.argv) != 2:
    print("Usage: python script.py <number_of_days>")
    sys.exit(1)

# Get the number of days from the first argument
n = int(sys.argv[1])

# Load the data from the CSV file
df = pd.read_csv('data/training_data.csv')

# Create a datetime column for plotting
df['datetime'] = pd.to_datetime(df[['year', 'month', 'day', 'hour', 'minute']])

# Calculate the cutoff date
cutoff_date = df['datetime'].max() - timedelta(days=n)

# Filter the DataFrame for the last n days
df_filtered = df[df['datetime'] >= cutoff_date]

# Plot the streaming status over time for the last n days
plt.figure(figsize=(12, 6))
plt.plot(df_filtered['datetime'], df_filtered['streaming'], drawstyle='steps-post')

# Set the labels and title
plt.xlabel('Time')
plt.ylabel('Streaming (1=True, 0=False)')
plt.title(f'Streaming Status Over the Last {n} Days')

# Display the plot
plt.show()
