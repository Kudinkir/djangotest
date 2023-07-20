""" script 5
what the script does:
1. gets gappers over 25% for the last 90 days
2. counts the amount of gappers for each day
3. counts the number of stocks: for yesterday, last 7 days, and last 31 days
4. returns the result as stock_counts.csv
"""


# rY7jzsLlcwNmsjs1WwQftckwGrTvrCK9 <-- api key
import requests
import pandas as pd
from datetime import datetime, timedelta
import os
from time import sleep

dateFormat = '%Y-%m-%d'

api_key = "rY7jzsLlcwNmsjs1WwQftckwGrTvrCK9"
thisDir = os.path.realpath(__file__).replace(__file__, '')

_from = datetime.strftime(datetime.today() - timedelta(days=40), dateFormat)

_to = datetime.strftime(datetime.today() - timedelta(days=1), dateFormat)

# increase percent
increase = 25

##########################################################################################################################

def getTickers(increasePercent, date):
    # get data for current date
    url = f"https://api.polygon.io/v2/aggs/grouped/locale/us/market/stocks/{date}?unadjusted=true&apiKey={api_key}"
    response = requests.get(url)
    data = response.json()
    df = pd.DataFrame(data['results'])

    # formulas
    df['gap_percent'] = ((df['c'] - df['o']) / df['o']) * 100   # (c-o)/o -> gap percent

    df = df.loc[(df['c'] >= 1) & (df['gap_percent'] >= increasePercent)]

    # round values for readability
    df['o'] = df['o'].round(1)
    df['c'] = df['c'].round(1)
    df['h'] = df['h'].round(1)
    df['l'] = df['l'].round(1)
    df['vw'] = df['vw'].round(1)
    df['gap_percent'] = df['gap_percent'].round(1)
    df['date'] = date

    return df[['T', 'o', 'c', 'h', 'l', 'vw', 'v', 'gap_percent', 'date']]

def getTickerData(ticker, date):
    url = f"https://api.polygon.io/v2/aggs/ticker/{ticker}/range/1/day/{date}/{date}?unadjusted=true&apiKey={api_key}"
    response = requests.get(url)
    data = response.json()
    df = pd.DataFrame(data['results'])
    df['gap_percent'] = ((df['c'] - df['o']) / df['o']) * 100
    df['o'] = df['o'].round(1)
    df['c'] = df['c'].round(1)
    df['h'] = df['h'].round(1)
    df['l'] = df['l'].round(1)
    df['vw'] = df['vw'].round(1)
    df['gap_percent'] = df['gap_percent'].round()
    df['date'] = date
    df['T'] = ticker

    return df[['T', 'o', 'c', 'h', 'l', 'vw', 'v', 'gap_percent', 'date']]

##########################################################################################################################
oneDay = timedelta(days=1)

# try to get the tickers for the current day
try:
    theDF = getTickers(increase, _from)
    theDF.columns = ['ticker', 'open', 'close', 'high', 'low', 'vwap', 'volume', 'gap%', 'date']
except Exception as e:
    _from = datetime.strftime(datetime.strptime(_from, dateFormat) + timedelta(days=1), dateFormat)
    try:
        theDF = getTickers(increase, _from)
        theDF.columns = ['ticker', 'open', 'close', 'high', 'low', 'vwap', 'volume', 'gap%', 'date']
    except Exception as e:
        _from = datetime.strftime(datetime.strptime(_from, dateFormat) + timedelta(days=1), dateFormat)
        try:
            theDF = getTickers(increase, _from)
            theDF.columns = ['ticker', 'open', 'close', 'high', 'low', 'vwap', 'volume', 'gap%', 'date']
        except Exception as e:
            _from = datetime.strftime(datetime.strptime(_from, dateFormat) + timedelta(days=1), dateFormat)
            try:
                theDF = getTickers(increase, _from)
                theDF.columns = ['ticker', 'open', 'close', 'high', 'low', 'vwap', 'volume', 'gap%', 'date']
            except Exception as e:
                _from = datetime.strftime(datetime.strptime(_from, dateFormat) + timedelta(days=1), dateFormat)
                try:
                    theDF = getTickers(increase, _from)
                    theDF.columns = ['ticker', 'open', 'close', 'high', 'low', 'vwap', 'volume', 'gap%', 'date']
                except Exception as e:
                    print(f'nope: {e}')

# loop through every day from _from to _to and add gappers
current_day = datetime.strptime(_from, dateFormat) + oneDay
end_day = datetime.strptime(_to, dateFormat) + oneDay
idx = 1
fails = 0
passes = 1
while current_day < end_day:
    date = datetime.strftime(current_day, dateFormat)
    # look for new stocks that gapped on current day
    try:
        otherDF = getTickers(increase, date)
    except:
        current_day += oneDay
        fails += 1
        idx += 1
        continue
    otherDF.columns = ['ticker', 'open', 'close', 'high', 'low', 'vwap', 'volume', 'gap%', 'date']
    
    # add the new gappers to the dataframe
    theDF = pd.concat([theDF, otherDF], axis=0)

    current_day += oneDay
    idx += 1
    passes += 1

# Filter out stocks that have 5 letters
theDF = theDF[~(theDF['ticker'].str.len() == 5)]

# Convert date column to datetime
theDF['date'] = pd.to_datetime(theDF['date'])

# Calculate the number of stocks up 25% in a day, a week, and a month
stocks_up_25_day = theDF[theDF['date'] >= (current_day - timedelta(days=1))]
stocks_up_25_week = theDF[theDF['date'] >= (current_day - timedelta(weeks=1))]
stocks_up_25_month = theDF[theDF['date'] >= (current_day - timedelta(days=31))]

# Group by date and count the number of stocks
stocks_up_25_day_grouped = stocks_up_25_day.groupby('date').size().reset_index()
stocks_up_25_day_grouped.columns = ['date', 'day']
stocks_up_25_day_grouped['date'] = stocks_up_25_day_grouped['date'].dt.strftime(dateFormat)

stocks_up_25_week_grouped = stocks_up_25_week.groupby(pd.Grouper(key='date', freq='W')).size().reset_index()
stocks_up_25_week_grouped.columns = ['date', 'week']
stocks_up_25_week_grouped['date'] = stocks_up_25_week_grouped['date'].dt.strftime('%Y-%m-%d')
merged_stocks_up_25_week = stocks_up_25_week_grouped.groupby('date')['week'].sum().reset_index()

stocks_up_25_month_grouped = stocks_up_25_month.groupby(pd.Grouper(key='date', freq='M')).size().reset_index()
stocks_up_25_month_grouped.columns = ['date', 'month']
stocks_up_25_month_grouped['date'] = stocks_up_25_month_grouped['date'].dt.strftime('%Y-%m')

# Combine rows
combined_stocks_up_25_day = pd.DataFrame({
    'date': ['day'],
    'count': [stocks_up_25_day_grouped['day'].sum()]
})
combined_stocks_up_25_week = pd.DataFrame({
    'date': ['Week'],
    'count': [merged_stocks_up_25_week['week'].sum()]
})
combined_stocks_up_25_month = pd.DataFrame({
    'date': ['month'],
    'count': [stocks_up_25_month_grouped['month'].sum()]
})

# Concatenate the combined row
merged_stocks_up_25_day = pd.concat([stocks_up_25_day_grouped, combined_stocks_up_25_day])
merged_stocks_up_25_week = pd.concat([merged_stocks_up_25_week, combined_stocks_up_25_week])
merged_stocks_up_25_month = pd.concat([stocks_up_25_month_grouped, combined_stocks_up_25_month])

# Create the final DataFrame with day, week, and month counts
final_df = pd.DataFrame({
    'day': [int(round(merged_stocks_up_25_day['count'].sum(), 0))],
    'week': [int(round(merged_stocks_up_25_week['count'].sum(), 0))],
    'month': [int(round(merged_stocks_up_25_month['count'].sum(), 0))]
})

# Save the final DataFrame to a CSV file
final_df.to_csv('stock_counts.csv', index=False)