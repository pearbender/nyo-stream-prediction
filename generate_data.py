import csv
from datetime import datetime, timedelta
import calendar
import holidays

# Load Japanese holidays
jp_holidays = holidays.Japan()

# File paths
input_file = "data/formatted.txt"
output_file = "data/training_data.csv"

# Function to determine if a date is a Japanese holiday
def is_japanese_holiday(date):
    return date in jp_holidays

# Read the input file and parse the data
streams = []
with open(input_file, "r") as file:
    for line in file:
        timestamp_str, duration_str = line.strip().split()
        timestamp = datetime.strptime(timestamp_str, "%Y-%m-%dT%H:%M")
        duration = float(duration_str)
        end_time = timestamp + timedelta(seconds=duration)
        streams.append((timestamp, end_time))

# Sort streams by start time
streams.sort()

# Determine the first and last minute to process
first_minute = streams[0][0]
current_time = datetime.now()

# Prepare CSV output
header = [
    "year", "month", "day", "hour", "minute", "day_of_week", "day_of_month", "week_of_year",
    #"minutes_since_last_stream",
    "is_japanese_holiday",
    "streams_for_current_week", "streams_for_current_month", "streaming"
]

with open(output_file, "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(header)
    
    last_stream_time = None
    streams_for_current_week = 0
    streams_for_current_month = 0
    
    current_stream_index = 0
    
    current_minute = first_minute
    previous_month = first_minute.month  # Keep track of the previous month
    
    while current_minute <= current_time:
        # Reset stream counts if new week or month
        if current_minute.isocalendar()[1] != (current_minute - timedelta(minutes=1)).isocalendar()[1]:
            streams_for_current_week = 0
        if current_minute.month != previous_month:
            streams_for_current_month = 0
            previous_month = current_minute.month
        
        # Check if current minute is within the stream period
        streaming = False
        if current_stream_index < len(streams):
            current_stream = streams[current_stream_index]
            if current_minute == current_stream[0]:  # New stream starts
                streams_for_current_week += 1
                streams_for_current_month += 1
            if current_stream[0] <= current_minute < current_stream[1]:
                streaming = True
                last_stream_time = current_minute
            elif current_minute >= current_stream[1] and current_stream_index + 1 < len(streams):
                current_stream_index += 1
        
        # Calculate minutes since last stream
        if last_stream_time is None:
            minutes_since_last_stream = 0
        else:
            minutes_since_last_stream = int((current_minute - last_stream_time).total_seconds() / 60)
        
        # Determine the week and month of the current minute
        week_of_year = current_minute.isocalendar()[1]
        
        # Write the row
        row = [
            current_minute.year,
            current_minute.month,
            current_minute.day,
            current_minute.hour,
            current_minute.minute,
            current_minute.strftime("%w"),
            current_minute.day,
            week_of_year,
            #minutes_since_last_stream,
            is_japanese_holiday(current_minute.date()),
            streams_for_current_week,
            streams_for_current_month,
            streaming
        ]
        writer.writerow(row)
        
        # Increment the current minute
        current_minute += timedelta(minutes=1)
