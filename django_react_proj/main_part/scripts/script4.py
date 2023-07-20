import requests
import pandas as pd
from datetime import datetime, timedelta
import os
from time import sleep

dateFormat = '%Y-%m-%d'

api_key = "rY7jzsLlcwNmsjs1WwQftckwGrTvrCK9"

x = 3
yesterday = datetime.strftime(datetime.today() - timedelta(days=x), dateFormat)

start_date = datetime.strptime(yesterday, dateFormat)
y = 93  # how many days you want to loop through
end_date = start_date - timedelta(days=y)

def get_tickers_less_than_one_dollar(date):
    url = f"https://api.polygon.io/v2/aggs/grouped/locale/us/market/stocks/{date}?unadjusted=true&apiKey={api_key}"
    response = requests.get(url)
    data = response.json()
    
    if 'results' not in data:
        previous_date = datetime.strptime(date, dateFormat) - timedelta(days=1)
        return get_tickers_less_than_one_dollar(previous_date.strftime(dateFormat))
    
    df = pd.DataFrame(data['results'])
    df = df.loc[df['c'] < 1]
    return df['T'].tolist()


def get_tickers_greater_than_or_equal_to_one_dollar(date):
    url = f"https://api.polygon.io/v2/aggs/grouped/locale/us/market/stocks/{date}?unadjusted=true&apiKey={api_key}"
    response = requests.get(url)
    data = response.json()
    try:
        df = pd.DataFrame(data['results'])
        df = df.loc[df['c'] >= 1]
        return df['T'].tolist()
    except KeyError:
        return []


def count_tickers(date):
    tickers_less_than_one_dollar = get_tickers_less_than_one_dollar(date)

    # Check if data is available for the specified date
    if not tickers_less_than_one_dollar:
        previous_date = datetime.strptime(date, dateFormat)
        while not tickers_less_than_one_dollar:
            # iterate back one day at a time until data is found, skipping weekends
            previous_date -= timedelta(days=1)
            if previous_date.weekday() < 5:  # skip saturday (5) and sunday (6)
                tickers_less_than_one_dollar = get_tickers_less_than_one_dollar(previous_date.strftime(dateFormat))

    previous_date = datetime.strptime(date, dateFormat) - timedelta(days=91)
    tickers_greater_than_or_equal_to_one_dollar = get_tickers_greater_than_or_equal_to_one_dollar(
        previous_date.strftime(dateFormat))
    count = len(set(tickers_less_than_one_dollar) & set(tickers_greater_than_or_equal_to_one_dollar))
    if count > 0:
        return date, count
    else:
        return None


def get_trading_dates(start_date, end_date):
    trading_dates = []
    current_date = start_date
    while current_date >= end_date:
        if current_date.weekday() < 5: # grrr 0 and 1 are days too!
            trading_dates.append(current_date.strftime(dateFormat))
        current_date -= timedelta(days=1)
        if current_date.weekday() >= 5:  # skip saturday (5) and sunday (6)
            current_date -= timedelta(days=1)
    return trading_dates


trading_dates = get_trading_dates(start_date, end_date)

results = []
for date in trading_dates:
    result = count_tickers(date)
    if result is not None:
        print(result)
        results.append(result)
    sleep(0.5)  # rate limits suck

df = pd.DataFrame(results, columns=['date', 'count'])
df.to_csv('script4_results.csv', index=False)

print('part 1/2 done...')

df = pd.read_csv('script4_results.csv')
df['date'] = pd.to_datetime(df['date'])
df.sort_values('date', inplace=True)
df['MA_5'] = df['count'].rolling(window=5, min_periods=1).mean().fillna(0).round(1)
df['MA_15'] = df['count'].rolling(window=15, min_periods=1).mean().fillna(0).round(1)
df.to_csv('script4_results.csv', index=False)

print('part 2/2 done')