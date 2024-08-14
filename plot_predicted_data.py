import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Load the data from the predicted CSV file
df = pd.read_csv('data/predicted.csv')

# Create a datetime column for plotting
df['datetime'] = pd.to_datetime(df[['year', 'month', 'day', 'hour', 'minute']])

# Find points where streaming changes from 0 to 1
transitions_start = df[(df['streaming'] == 1) & (df['streaming'].shift(1) == 0)]
# Find points where streaming changes from 1 to 0
transitions_end = df[(df['streaming'] == 0) & (df['streaming'].shift(1) == 1)]

# Plot the streaming status over time
plt.figure(figsize=(12, 6))
plt.step(df['datetime'], df['streaming'], where='post', color='b', alpha=0.5)

# Highlight transition points
plt.scatter(transitions_start['datetime'], transitions_start['streaming'], color='g', zorder=5, label='Start of Streaming', marker='o')
plt.scatter(transitions_end['datetime'], transitions_end['streaming'], color='r', zorder=5, label='End of Streaming', marker='x')

# Annotate transition points
for _, row in pd.concat([transitions_start, transitions_end]).iterrows():
    plt.text(row['datetime'], row['streaming'], row['datetime'].strftime('%Y-%m-%d %H:%M'),
             verticalalignment='bottom', horizontalalignment='right', fontsize=8, color='black')

# Set the labels and title
plt.xlabel('Time')
plt.ylabel('Streaming (1=True, 0=False)')
plt.title('Streaming Status Over Time')

# Set y-axis limits and ticks to only show 0 and 1
plt.ylim(-0.1, 1.1)
plt.yticks([0, 1])

# Rotate and format the x-axis labels
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %a'))
plt.gcf().autofmt_xdate()  # Auto format date labels to prevent overlap

# Add legend
plt.legend()

# Display the plot
plt.grid(True)
plt.show()
