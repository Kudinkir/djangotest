import requests
import pandas as pd
from datetime import datetime, timedelta
import os

dateFormat = '%Y-%m-%d'

api_key = "rY7jzsLlcwNmsjs1WwQftckwGrTvrCK9"
thisDir = os.path.realpath(__file__).replace(__file__, '')

targetDay = datetime.strftime(datetime.today() - timedelta(days=1), dateFormat)

_from = targetDay
_to = targetDay
increase = 20

def getTickers(increasePercent, date):
    url = f"https://api.polygon.io/v2/aggs/grouped/locale/us/market/stocks/{date}?unadjusted=true&apiKey={api_key}"
    response = requests.get(url)
    data = response.json()
    df = pd.DataFrame(data['results'])

    df['gap_percent'] = ((df['c'] - df['o']) / df['o']) * 100

    df = df.loc[(df['c'] >= 1) & (df['gap_percent'] >= increasePercent)]
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

temp = True
while temp:
    try:
        theDF = getTickers(increase, _from)
        theDF.columns = ['ticker', 'open', 'close', 'high', 'low', 'vwap', 'volume', 'gap', 'date']
        temp = False
    except:
        _from = datetime.strftime(datetime.strptime(_from, dateFormat) - timedelta(days=1), dateFormat)
        _to = _from


oneDay = timedelta(days=1)
current_day = datetime.strptime(_from, dateFormat) + oneDay
end_day = datetime.strptime(_to, dateFormat) + oneDay
idx = 1
fails = 0
passes = 1
while current_day < end_day:
    date = datetime.strftime(current_day, dateFormat)
    try:
        otherDF = getTickers(increase, date)
    except:
        current_day += oneDay
        fails += 1
        idx += 1
        continue
    otherDF.columns = ['ticker', 'open', 'close', 'high', 'low', 'vwap', 'volume', 'gap', 'date']
    
    try:
        new_gappers = otherDF[~otherDF['ticker'].isin(theDF['ticker'])]
    except:
        current_day += oneDay
        fails += 1
        idx += 1
        continue
    
    theDF = pd.concat([theDF, new_gappers], axis=0)

    current_day += oneDay
    idx += 1
    passes += 1

theDF = theDF[~(theDF['ticker'].str.len() == 5)]

number = len(theDF.index)

csv = theDF.to_csv(f'results.csv', index=False)