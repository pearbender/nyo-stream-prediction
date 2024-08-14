from datetime import datetime, timedelta
import re
import pytz

# File path to the raw data and output file
input_file_path = 'data/raw.txt'
output_file_path = 'data/formatted.txt'

# Read the data from the file
with open(input_file_path, 'r') as file:
    lines = file.readlines()

# Regex to match date, time, and duration
date_duration_pattern = re.compile(r'(\d{2}/\w{3}/\d{4} \d{2}:\d{2})\t([\d.]+) hrs')

# Define JST timezone
jst = pytz.timezone('Asia/Tokyo')

# Process each line in reverse order and write the results to the output file
with open(output_file_path, 'w') as output_file:
    for line in reversed(lines[1::2]):  # Skip the header and the lines with avg viewers, then reverse
        line = line.strip()
        match = date_duration_pattern.match(line)
        
        if match:
            # Extract date and duration
            date_str = match.group(1)
            duration_hrs = float(match.group(2))

            # Parse the date string into a datetime object with JST timezone
            dt_jst = jst.localize(datetime.strptime(date_str, '%d/%b/%Y %H:%M'))

            # Calculate the duration in seconds
            duration = timedelta(hours=duration_hrs)

            # Format the ISO datetime and duration in seconds
            iso_datetime_jst = dt_jst.strftime('%Y-%m-%dT%H:%M')
            duration_secs = duration.total_seconds()
            
            # Write the result to the output file
            output_file.write(f"{iso_datetime_jst} {duration_secs}\n")
