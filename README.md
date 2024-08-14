# NYO Stream Prediction

## Usage

Get data like the following

```
Stream	Duration	Avg Viewers
 13/Aug/2024 20:32	4.2 hrs
11
 12/Aug/2024 21:01	3.7 hrs
13
 11/Aug/2024 20:22	4.7 hrs
 ```

from https://twitchtracker.com and save it to `data/raw.txt`.

Run

```
python parse_raw.py > data/formatted.txt
```


## Possible features
- Year
- Month
- Day
- Hour
- Minute
- Day of the week
- Day of the month
- Week of the year
- Minutes since last stream -- Doesn't work because 0 = streaming and > 0 = not streaming
- Is Japanese holiday?
- Streams for current week
- Streams for current month

1440 minutes in a day.
365 days in a year.
525,600 (1440 * 365) data points per year.