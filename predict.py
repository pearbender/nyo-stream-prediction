import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import joblib
import holidays
import sys

# Check for correct number of command line arguments
if len(sys.argv) != 2:
    print("Usage: python script.py <number_of_days>")
    sys.exit(1)

# Get the number of days to predict from the command line argument
try:
    num_days = int(sys.argv[1])
except ValueError:
    print("Error: Number of days must be an integer.")
    sys.exit(1)

# Load the trained model
model = joblib.load('data/model.pkl')

# Load Japanese holidays
jp_holidays = holidays.Japan()

# Load historical data
historical_data = pd.read_csv('data/training_data.csv')

# Convert the date and time components into a datetime object in historical data
historical_data['datetime'] = pd.to_datetime(historical_data[['year', 'month', 'day', 'hour', 'minute']])

# Aggregate data by day to count unique days with streaming activity
daily_streams = historical_data[historical_data['streaming'] == True].groupby(
    historical_data['datetime'].dt.date
).size().reset_index(name='streaming_days')

# Add additional columns for year, month, and week
daily_streams['year'] = daily_streams['datetime'].apply(lambda x: x.year)
daily_streams['month'] = daily_streams['datetime'].apply(lambda x: x.month)
daily_streams['week'] = daily_streams['datetime'].apply(lambda x: x.isocalendar().week)

# Set the start time to now and generate timestamps for every minute for the specified number of days
start_time = datetime.now()
end_time = start_time + timedelta(days=num_days)  # Predict for the specified number of days
timestamps = pd.date_range(start=start_time, end=end_time, freq='min')  # Changed 'T' to 'min'

# Determine the current month and week based on the start time
current_year = start_time.year
current_month = start_time.month
current_week = start_time.isocalendar().week

# Count unique streaming days in the current month
streams_for_current_month = daily_streams[
    (daily_streams['year'] == current_year) &
    (daily_streams['month'] == current_month)
].shape[0]

# Count unique streaming days in the current week
streams_for_current_week = daily_streams[
    (daily_streams['year'] == current_year) &
    (daily_streams['week'] == current_week)
].shape[0]

# Print the counts
print(f"Number of unique streaming days in the current month ({current_month}/{current_year}): {streams_for_current_month}")
print(f"Number of unique streaming days in the current week ({current_week} of {current_year}): {streams_for_current_week}")

# Create a DataFrame with features for each timestamp
data = pd.DataFrame({
    'year': timestamps.year,
    'month': timestamps.month,
    'day': timestamps.day,
    'hour': timestamps.hour,
    'minute': timestamps.minute,
    'day_of_week': timestamps.dayofweek + 1,  # Monday=0 in datetime, but in training data Monday=1
    'day_of_month': timestamps.day,
    'week_of_year': timestamps.isocalendar().week,
    'is_japanese_holiday': [1 if date in jp_holidays else 0 for date in timestamps],
    'streams_for_current_week': streams_for_current_week,
    'streams_for_current_month': streams_for_current_month
})

# Predict streaming status for each timestamp
predictions = model.predict(data)

# Add predictions to the DataFrame
data['streaming'] = predictions

# Convert boolean columns back to boolean type
data['is_japanese_holiday'] = data['is_japanese_holiday'].astype(bool)
data['streaming'] = data['streaming'].astype(bool)

# Save the predictions to a CSV file
data.to_csv('data/predicted.csv', index=False)

print(f"Predictions saved to 'data/predicted.csv'.")
