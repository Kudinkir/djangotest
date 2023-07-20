"""
what the script does:
1. gets gappers over 20% for the last 90 days
2. counts the amount of gappers for each day
3. adds the moving average for 5 days and 15 days to the result
4. returns the result as results_final.csv
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

_from = datetime.strftime(datetime.today() - timedelta(days=90), dateFormat)

_to = datetime.strftime(datetime.today() - timedelta(days=1), dateFormat)

# increase percent
increase = 20

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

# filter out stocks which have 5 letters
theDF = theDF[~(theDF['ticker'].str.len() == 5)]

final = theDF
final['date'] = pd.to_datetime(final['date'])
grouped_data = final.groupby('date').size().reset_index()
grouped_data.columns = ['date', 'count']
grouped_data['date'] = grouped_data['date'].dt.strftime(dateFormat)
grouped_data.to_csv('results_final.csv', columns=['date', 'count'], index=False)

df = pd.read_csv('results_final.csv')
df['date'] = pd.to_datetime(df['date'])
df.sort_values('date', inplace=True)
df['MA_5'] = df['count'].rolling(window=5, min_periods=1).mean().fillna(0).round(1)
df['MA_15'] = df['count'].rolling(window=15, min_periods=1).mean().fillna(0).round(1)
df.to_csv('results_final.csv', index=False)