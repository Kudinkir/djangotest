import requests
import pandas as pd
from datetime import datetime, timedelta
import os

dateFormat = '%Y-%m-%d'

api_key = "rY7jzsLlcwNmsjs1WwQftckwGrTvrCK9"
thisDir = os.path.realpath(__file__).replace(__file__, '')

targetDay = datetime.strftime(datetime.today() - timedelta(days=1), dateFormat)
increase = 104

def getTickers(increasePercent, date):
    url = f"https://api.polygon.io/v2/aggs/grouped/locale/us/market/stocks/{date}?unadjusted=true&apiKey={api_key}"
    response = requests.get(url)
    data = response.json()
    df = pd.DataFrame(data['results'])

    df['formula'] = (df['c']/df['o']) * 100

    df = df.loc[(df['c'] >= 1) & (df['formula'] >= increasePercent)]
    df['o'] = df['o'].round(1)
    df['c'] = df['c'].round(1)
    df['h'] = df['h'].round(1)
    df['l'] = df['l'].round(1)
    df['vw'] = df['vw'].round(1)
    df['formula'] = df['formula'].round(1)
    df['date'] = date

    return df[['T', 'o', 'c', 'h', 'l', 'vw', 'v', 'formula', 'date']]

def getTickerData(ticker, date):
    url = f"https://api.polygon.io/v2/aggs/ticker/{ticker}/range/1/day/{date}/{date}?unadjusted=true&apiKey={api_key}"
    response = requests.get(url)
    data = response.json()
    df = pd.DataFrame(data['results'])
    df['formula'] = (df['c'] / df['o']) * 100
    df['o'] = df['o'].round(1)
    df['c'] = df['c'].round(1)
    df['h'] = df['h'].round(1)
    df['l'] = df['l'].round(1)
    df['vw'] = df['vw'].round(1)
    df['formula'] = df['formula'].round()
    df['date'] = date
    df['T'] = ticker

    return df[['T', 'o', 'c', 'h', 'l', 'vw', 'v', 'formula', 'date']]

try:
    targetDay = datetime.strftime(datetime.today() - timedelta(days=1), dateFormat)
    theDF = getTickers(increase, targetDay)
except:
    try:
        targetDay = datetime.strftime(datetime.today() - timedelta(days=2), dateFormat)
        theDF = getTickers(increase, targetDay)
    except:
        try:
            targetDay = datetime.strftime(datetime.today() - timedelta(days=3), dateFormat)
            theDF = getTickers(increase, targetDay)
        except:
            try:
                targetDay = datetime.strftime(datetime.today() - timedelta(days=4), dateFormat)
                theDF = getTickers(increase, targetDay)
            except:
                targetDay = None
                quit()

_from = targetDay
_to = targetDay
try:
    theDF = getTickers(increase, _from)
    theDF.columns = ['ticker', 'open', 'close', 'high', 'low', 'vwap', 'volume', 'formula', 'date']
except Exception as e:
    print('ERROR: pick a new _from date because ' + str(e))
    quit()

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
    otherDF.columns = ['ticker', 'open', 'close', 'high', 'low', 'vwap', 'volume', 'formula', 'date']
    
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

#csv = theDF.to_csv(f'results.csv', index=False)

f1 = len(theDF.index)

import requests
import pandas as pd
from datetime import datetime, timedelta
import os

dateFormat = '%Y-%m-%d'

api_key = "rY7jzsLlcwNmsjs1WwQftckwGrTvrCK9"
thisDir = os.path.realpath(__file__).replace(__file__, '')

try:
    targetDay = datetime.strftime(datetime.today() - timedelta(days=2), dateFormat)
    theDF = getTickers(increase, targetDay)
except:
    try:
        targetDay = datetime.strftime(datetime.today() - timedelta(days=3), dateFormat)
        theDF = getTickers(increase, targetDay)
    except:
        try:
            targetDay = datetime.strftime(datetime.today() - timedelta(days=4), dateFormat)
            theDF = getTickers(increase, targetDay)
        except:
            try:
                targetDay = datetime.strftime(datetime.today() - timedelta(days=5), dateFormat)
                theDF = getTickers(increase, targetDay)
            except:
                targetDay = None
                quit()
increase = 104

def getTickers(increasePercent, date):
    url = f"https://api.polygon.io/v2/aggs/grouped/locale/us/market/stocks/{date}?unadjusted=true&apiKey={api_key}"
    response = requests.get(url)
    data = response.json()
    df = pd.DataFrame(data['results'])

    df['formula'] = (df['c']/df['o']) * 100

    df = df.loc[(df['c'] >= 1) & (df['formula'] >= increasePercent)]
    df['o'] = df['o'].round(1)
    df['c'] = df['c'].round(1)
    df['h'] = df['h'].round(1)
    df['l'] = df['l'].round(1)
    df['vw'] = df['vw'].round(1)
    df['formula'] = df['formula'].round(1)
    df['date'] = date

    return df[['T', 'o', 'c', 'h', 'l', 'vw', 'v', 'formula', 'date']]

def getTickerData(ticker, date):
    url = f"https://api.polygon.io/v2/aggs/ticker/{ticker}/range/1/day/{date}/{date}?unadjusted=true&apiKey={api_key}"
    response = requests.get(url)
    data = response.json()
    df = pd.DataFrame(data['results'])
    df['formula'] = (df['c'] / df['o']) * 100
    df['o'] = df['o'].round(1)
    df['c'] = df['c'].round(1)
    df['h'] = df['h'].round(1)
    df['l'] = df['l'].round(1)
    df['vw'] = df['vw'].round(1)
    df['formula'] = df['formula'].round()
    df['date'] = date
    df['T'] = ticker

    return df[['T', 'o', 'c', 'h', 'l', 'vw', 'v', 'formula', 'date']]


_from = targetDay
_to = targetDay

try:
    theDF = getTickers(increase, _from)
    theDF.columns = ['ticker', 'open', 'close', 'high', 'low', 'vwap', 'volume', 'formula', 'date']
except Exception as e:
    print('ERROR: pick a new _from date because ' + str(e))
    quit()

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
    otherDF.columns = ['ticker', 'open', 'close', 'high', 'low', 'vwap', 'volume', 'formula', 'date']
    
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

#csv = theDF.to_csv(f'results.csv', index=False)

f2 = len(theDF.index)

import requests
import pandas as pd
from datetime import datetime, timedelta
import os

dateFormat = '%Y-%m-%d'

api_key = "rY7jzsLlcwNmsjs1WwQftckwGrTvrCK9"
thisDir = os.path.realpath(__file__).replace(__file__, '')

try:
    targetDay = datetime.strftime(datetime.today() - timedelta(days=1), dateFormat)
    theDF = getTickers(increase, targetDay)
except:
    try:
        targetDay = datetime.strftime(datetime.today() - timedelta(days=2), dateFormat)
        theDF = getTickers(increase, targetDay)
    except:
        try:
            targetDay = datetime.strftime(datetime.today() - timedelta(days=3), dateFormat)
            theDF = getTickers(increase, targetDay)
        except:
            try:
                targetDay = datetime.strftime(datetime.today() - timedelta(days=4), dateFormat)
                theDF = getTickers(increase, targetDay)
            except:
                targetDay = None
                quit()

_from = targetDay
_to = targetDay
increase = 96

def getTickers(increasePercent, date):
    url = f"https://api.polygon.io/v2/aggs/grouped/locale/us/market/stocks/{date}?unadjusted=true&apiKey={api_key}"
    response = requests.get(url)
    data = response.json()
    df = pd.DataFrame(data['results'])

    df['formula'] = (df['c']/df['o']) * 100

    df = df.loc[(df['c'] >= 1) & (df['formula'] <= increasePercent)]
    df['o'] = df['o'].round(1)
    df['c'] = df['c'].round(1)
    df['h'] = df['h'].round(1)
    df['l'] = df['l'].round(1)
    df['vw'] = df['vw'].round(1)
    df['formula'] = df['formula'].round(1)
    df['date'] = date

    return df[['T', 'o', 'c', 'h', 'l', 'vw', 'v', 'formula', 'date']]

def getTickerData(ticker, date):
    url = f"https://api.polygon.io/v2/aggs/ticker/{ticker}/range/1/day/{date}/{date}?unadjusted=true&apiKey={api_key}"
    response = requests.get(url)
    data = response.json()
    df = pd.DataFrame(data['results'])
    df['formula'] = (df['c'] / df['o']) * 100
    df['o'] = df['o'].round(1)
    df['c'] = df['c'].round(1)
    df['h'] = df['h'].round(1)
    df['l'] = df['l'].round(1)
    df['vw'] = df['vw'].round(1)
    df['formula'] = df['formula'].round()
    df['date'] = date
    df['T'] = ticker

    return df[['T', 'o', 'c', 'h', 'l', 'vw', 'v', 'formula', 'date']]

try:
    theDF = getTickers(increase, _from)
    theDF.columns = ['ticker', 'open', 'close', 'high', 'low', 'vwap', 'volume', 'formula', 'date']
except Exception as e:
    print('ERROR: pick a new _from date because ' + str(e))
    quit()

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
    otherDF.columns = ['ticker', 'open', 'close', 'high', 'low', 'vwap', 'volume', 'formula', 'date']
    
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

#csv = theDF.to_csv(f'results.csv', index=False)

f3 = len(theDF.index)

import requests
import pandas as pd
from datetime import datetime, timedelta
import os

dateFormat = '%Y-%m-%d'

api_key = "rY7jzsLlcwNmsjs1WwQftckwGrTvrCK9"
thisDir = os.path.realpath(__file__).replace(__file__, '')

increase = 96

def getTickers(increasePercent, date):
    url = f"https://api.polygon.io/v2/aggs/grouped/locale/us/market/stocks/{date}?unadjusted=true&apiKey={api_key}"
    response = requests.get(url)
    data = response.json()
    df = pd.DataFrame(data['results'])

    df['formula'] = (df['c']/df['o']) * 100

    df = df.loc[(df['c'] >= 1) & (df['formula'] <= increasePercent)]
    df['o'] = df['o'].round(1)
    df['c'] = df['c'].round(1)
    df['h'] = df['h'].round(1)
    df['l'] = df['l'].round(1)
    df['vw'] = df['vw'].round(1)
    df['formula'] = df['formula'].round(1)
    df['date'] = date

    return df[['T', 'o', 'c', 'h', 'l', 'vw', 'v', 'formula', 'date']]

def getTickerData(ticker, date):
    url = f"https://api.polygon.io/v2/aggs/ticker/{ticker}/range/1/day/{date}/{date}?unadjusted=true&apiKey={api_key}"
    response = requests.get(url)
    data = response.json()
    df = pd.DataFrame(data['results'])
    df['formula'] = (df['c'] / df['o']) * 100
    df['o'] = df['o'].round(1)
    df['c'] = df['c'].round(1)
    df['h'] = df['h'].round(1)
    df['l'] = df['l'].round(1)
    df['vw'] = df['vw'].round(1)
    df['formula'] = df['formula'].round()
    df['date'] = date
    df['T'] = ticker

    return df[['T', 'o', 'c', 'h', 'l', 'vw', 'v', 'formula', 'date']]

try:
    targetDay = datetime.strftime(datetime.today() - timedelta(days=2), dateFormat)
    theDF = getTickers(increase, targetDay)
except:
    try:
        targetDay = datetime.strftime(datetime.today() - timedelta(days=3), dateFormat)
        theDF = getTickers(increase, targetDay)
    except:
        try:
            targetDay = datetime.strftime(datetime.today() - timedelta(days=4), dateFormat)
            theDF = getTickers(increase, targetDay)
        except:
            try:
                targetDay = datetime.strftime(datetime.today() - timedelta(days=5), dateFormat)
                theDF = getTickers(increase, targetDay)
            except:
                targetDay = None
                quit()

_from = targetDay
_to = targetDay

try:
    theDF = getTickers(increase, _from)
    theDF.columns = ['ticker', 'open', 'close', 'high', 'low', 'vwap', 'volume', 'formula', 'date']
except Exception as e:
    print('ERROR: pick a new _from date because ' + str(e))
    quit()

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
    otherDF.columns = ['ticker', 'open', 'close', 'high', 'low', 'vwap', 'volume', 'formula', 'date']
    
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

#csv = theDF.to_csv(f'results.csv', index=False)

f4 = len(theDF.index)

import requests
import pandas as pd
from datetime import datetime, timedelta
import os

dateFormat = '%Y-%m-%d'

api_key = "rY7jzsLlcwNmsjs1WwQftckwGrTvrCK9"
thisDir = os.path.realpath(__file__).replace(__file__, '')

try:
    targetDay = datetime.strftime(datetime.today() - timedelta(days=1), dateFormat)
    theDF = getTickers(increase, targetDay)
except:
    try:
        targetDay = datetime.strftime(datetime.today() - timedelta(days=2), dateFormat)
        theDF = getTickers(increase, targetDay)
    except:
        try:
            targetDay = datetime.strftime(datetime.today() - timedelta(days=3), dateFormat)
            theDF = getTickers(increase, targetDay)
        except:
            try:
                targetDay = datetime.strftime(datetime.today() - timedelta(days=4), dateFormat)
                theDF = getTickers(increase, targetDay)
            except:
                targetDay = None
                quit()

_from = targetDay
_to = targetDay
increase = 104

def getTickers(increasePercent, date):
    url = f"https://api.polygon.io/v2/aggs/grouped/locale/us/market/stocks/{date}?unadjusted=true&apiKey={api_key}"
    response = requests.get(url)
    data = response.json()
    df = pd.DataFrame(data['results'])

    df['formula'] = (df['c']/df['vw']) * 100

    df = df.loc[(df['c'] >= 1) & (df['formula'] >= increasePercent)]
    df['o'] = df['o'].round(1)
    df['c'] = df['c'].round(1)
    df['h'] = df['h'].round(1)
    df['l'] = df['l'].round(1)
    df['vw'] = df['vw'].round(1)
    df['formula'] = df['formula'].round(1)
    df['date'] = date

    return df[['T', 'o', 'c', 'h', 'l', 'vw', 'v', 'formula', 'date']]

def getTickerData(ticker, date):
    url = f"https://api.polygon.io/v2/aggs/ticker/{ticker}/range/1/day/{date}/{date}?unadjusted=true&apiKey={api_key}"
    response = requests.get(url)
    data = response.json()
    df = pd.DataFrame(data['results'])
    df['formula'] = (df['c'] / df['vw']) * 100
    df['o'] = df['o'].round(1)
    df['c'] = df['c'].round(1)
    df['h'] = df['h'].round(1)
    df['l'] = df['l'].round(1)
    df['vw'] = df['vw'].round(1)
    df['formula'] = df['formula'].round()
    df['date'] = date
    df['T'] = ticker

    return df[['T', 'o', 'c', 'h', 'l', 'vw', 'v', 'formula', 'date']]

try:
    theDF = getTickers(increase, _from)
    theDF.columns = ['ticker', 'open', 'close', 'high', 'low', 'vwap', 'volume', 'formula', 'date']
except Exception as e:
    print('ERROR: pick a new _from date because ' + str(e))
    quit()

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
    otherDF.columns = ['ticker', 'open', 'close', 'high', 'low', 'vwap', 'volume', 'formula', 'date']
    
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

#csv = theDF.to_csv(f'results.csv', index=False)

f5 = len(theDF.index)

import requests
import pandas as pd
from datetime import datetime, timedelta
import os

dateFormat = '%Y-%m-%d'

api_key = "rY7jzsLlcwNmsjs1WwQftckwGrTvrCK9"
thisDir = os.path.realpath(__file__).replace(__file__, '')

increase = 104

def getTickers(increasePercent, date):
    url = f"https://api.polygon.io/v2/aggs/grouped/locale/us/market/stocks/{date}?unadjusted=true&apiKey={api_key}"
    response = requests.get(url)
    data = response.json()
    df = pd.DataFrame(data['results'])

    df['formula'] = (df['c']/df['vw']) * 100

    df = df.loc[(df['c'] >= 1) & (df['formula'] >= increasePercent)]
    df['o'] = df['o'].round(1)
    df['c'] = df['c'].round(1)
    df['h'] = df['h'].round(1)
    df['l'] = df['l'].round(1)
    df['vw'] = df['vw'].round(1)
    df['formula'] = df['formula'].round(1)
    df['date'] = date

    return df[['T', 'o', 'c', 'h', 'l', 'vw', 'v', 'formula', 'date']]

def getTickerData(ticker, date):
    url = f"https://api.polygon.io/v2/aggs/ticker/{ticker}/range/1/day/{date}/{date}?unadjusted=true&apiKey={api_key}"
    response = requests.get(url)
    data = response.json()
    df = pd.DataFrame(data['results'])
    df['formula'] = (df['c'] / df['vw']) * 100
    df['o'] = df['o'].round(1)
    df['c'] = df['c'].round(1)
    df['h'] = df['h'].round(1)
    df['l'] = df['l'].round(1)
    df['vw'] = df['vw'].round(1)
    df['formula'] = df['formula'].round()
    df['date'] = date
    df['T'] = ticker

    return df[['T', 'o', 'c', 'h', 'l', 'vw', 'v', 'formula', 'date']]

try:
    targetDay = datetime.strftime(datetime.today() - timedelta(days=2), dateFormat)
    theDF = getTickers(increase, targetDay)
except:
    try:
        targetDay = datetime.strftime(datetime.today() - timedelta(days=3), dateFormat)
        theDF = getTickers(increase, targetDay)
    except:
        try:
            targetDay = datetime.strftime(datetime.today() - timedelta(days=4), dateFormat)
            theDF = getTickers(increase, targetDay)
        except:
            try:
                targetDay = datetime.strftime(datetime.today() - timedelta(days=5), dateFormat)
                theDF = getTickers(increase, targetDay)
            except:
                targetDay = None
                quit()

_from = targetDay
_to = targetDay

try:
    theDF = getTickers(increase, _from)
    theDF.columns = ['ticker', 'open', 'close', 'high', 'low', 'vwap', 'volume', 'formula', 'date']
except Exception as e:
    print('ERROR: pick a new _from date because ' + str(e))
    quit()

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
    otherDF.columns = ['ticker', 'open', 'close', 'high', 'low', 'vwap', 'volume', 'formula', 'date']
    
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

#csv = theDF.to_csv(f'results.csv', index=False)

f6 = len(theDF.index)

import requests
import pandas as pd
from datetime import datetime, timedelta
import os

dateFormat = '%Y-%m-%d'

api_key = "rY7jzsLlcwNmsjs1WwQftckwGrTvrCK9"
thisDir = os.path.realpath(__file__).replace(__file__, '')

try:
    targetDay = datetime.strftime(datetime.today() - timedelta(days=1), dateFormat)
    theDF = getTickers(increase, targetDay)
except:
    try:
        targetDay = datetime.strftime(datetime.today() - timedelta(days=2), dateFormat)
        theDF = getTickers(increase, targetDay)
    except:
        try:
            targetDay = datetime.strftime(datetime.today() - timedelta(days=3), dateFormat)
            theDF = getTickers(increase, targetDay)
        except:
            try:
                targetDay = datetime.strftime(datetime.today() - timedelta(days=4), dateFormat)
                theDF = getTickers(increase, targetDay)
            except:
                targetDay = None
                quit()

_from = targetDay
_to = targetDay
increase = 96

def getTickers(increasePercent, date):
    url = f"https://api.polygon.io/v2/aggs/grouped/locale/us/market/stocks/{date}?unadjusted=true&apiKey={api_key}"
    response = requests.get(url)
    data = response.json()
    df = pd.DataFrame(data['results'])

    df['formula'] = (df['c']/df['vw']) * 100

    df = df.loc[(df['c'] >= 1) & (df['formula'] <= increasePercent)]
    df['o'] = df['o'].round(1)
    df['c'] = df['c'].round(1)
    df['h'] = df['h'].round(1)
    df['l'] = df['l'].round(1)
    df['vw'] = df['vw'].round(1)
    df['formula'] = df['formula'].round(1)
    df['date'] = date

    return df[['T', 'o', 'c', 'h', 'l', 'vw', 'v', 'formula', 'date']]

def getTickerData(ticker, date):
    url = f"https://api.polygon.io/v2/aggs/ticker/{ticker}/range/1/day/{date}/{date}?unadjusted=true&apiKey={api_key}"
    response = requests.get(url)
    data = response.json()
    df = pd.DataFrame(data['results'])
    df['formula'] = (df['c'] / df['vw']) * 100
    df['o'] = df['o'].round(1)
    df['c'] = df['c'].round(1)
    df['h'] = df['h'].round(1)
    df['l'] = df['l'].round(1)
    df['vw'] = df['vw'].round(1)
    df['formula'] = df['formula'].round()
    df['date'] = date
    df['T'] = ticker

    return df[['T', 'o', 'c', 'h', 'l', 'vw', 'v', 'formula', 'date']]

try:
    theDF = getTickers(increase, _from)
    theDF.columns = ['ticker', 'open', 'close', 'high', 'low', 'vwap', 'volume', 'formula', 'date']
except Exception as e:
    print('ERROR: pick a new _from date because ' + str(e))
    quit()

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
    otherDF.columns = ['ticker', 'open', 'close', 'high', 'low', 'vwap', 'volume', 'formula', 'date']
    
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

#csv = theDF.to_csv(f'results.csv', index=False)

f7 = len(theDF.index)

import requests
import pandas as pd
from datetime import datetime, timedelta
import os

dateFormat = '%Y-%m-%d'

api_key = "rY7jzsLlcwNmsjs1WwQftckwGrTvrCK9"
thisDir = os.path.realpath(__file__).replace(__file__, '')

increase = 96

def getTickers(increasePercent, date):
    url = f"https://api.polygon.io/v2/aggs/grouped/locale/us/market/stocks/{date}?unadjusted=true&apiKey={api_key}"
    response = requests.get(url)
    data = response.json()
    df = pd.DataFrame(data['results'])

    df['formula'] = (df['c']/df['vw']) * 100

    df = df.loc[(df['c'] >= 1) & (df['formula'] <= increasePercent)]
    df['o'] = df['o'].round(1)
    df['c'] = df['c'].round(1)
    df['h'] = df['h'].round(1)
    df['l'] = df['l'].round(1)
    df['vw'] = df['vw'].round(1)
    df['formula'] = df['formula'].round(1)
    df['date'] = date

    return df[['T', 'o', 'c', 'h', 'l', 'vw', 'v', 'formula', 'date']]

def getTickerData(ticker, date):
    url = f"https://api.polygon.io/v2/aggs/ticker/{ticker}/range/1/day/{date}/{date}?unadjusted=true&apiKey={api_key}"
    response = requests.get(url)
    data = response.json()
    df = pd.DataFrame(data['results'])
    df['formula'] = (df['c'] / df['vw']) * 100
    df['o'] = df['o'].round(1)
    df['c'] = df['c'].round(1)
    df['h'] = df['h'].round(1)
    df['l'] = df['l'].round(1)
    df['vw'] = df['vw'].round(1)
    df['formula'] = df['formula'].round()
    df['date'] = date
    df['T'] = ticker

    return df[['T', 'o', 'c', 'h', 'l', 'vw', 'v', 'formula', 'date']]

try:
    targetDay = datetime.strftime(datetime.today() - timedelta(days=2), dateFormat)
    theDF = getTickers(increase, targetDay)
except:
    try:
        targetDay = datetime.strftime(datetime.today() - timedelta(days=3), dateFormat)
        theDF = getTickers(increase, targetDay)
    except:
        try:
            targetDay = datetime.strftime(datetime.today() - timedelta(days=4), dateFormat)
            theDF = getTickers(increase, targetDay)
        except:
            try:
                targetDay = datetime.strftime(datetime.today() - timedelta(days=5), dateFormat)
                theDF = getTickers(increase, targetDay)
            except:
                targetDay = None
                quit()

_from = targetDay
_to = targetDay

try:
    theDF = getTickers(increase, _from)
    theDF.columns = ['ticker', 'open', 'close', 'high', 'low', 'vwap', 'volume', 'formula', 'date']
except Exception as e:
    print('ERROR: pick a new _from date because ' + str(e))
    quit()

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
    otherDF.columns = ['ticker', 'open', 'close', 'high', 'low', 'vwap', 'volume', 'formula', 'date']
    
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

#csv = theDF.to_csv(f'results.csv', index=False)

f8 = len(theDF.index)

d12 = round((f1/f2-1)*100, 1)
d34 = round((f3/f4-1)*100, 1)
d56 = round((f5/f6-1)*100, 1)
d78 = round((f7/f8-1)*100, 1)

# d = difference
# f = formula

"""
FORMULAS
f1) number of stock today CLOSE/OPEN >= 1.04
f2) the same, but -1 day
f3) number of stock today CLOSE/OPEN <= 0.96
f4) the same, but -1 day
f5) number of stock today CLOSE/VWAP >= 1.10
f6) the same, but -1 day
f7) number of stock today CLOSE/VWAP <= 0.90
f8) the same, but -1 day
"""

print(f"""results for {datetime.strftime(datetime.today() - timedelta(days=1), dateFormat)}:
f1: {f1}
f2: {f2}
d12 (%): {d12}
f3: {f3}
f4: {f4}
d34 (%): {d34}
f5: {f5}
f6: {f6}
d56 (%): {d56}
f7: {f7}
f8: {f8}
d78 (%): {d78}""")

with open('4upperblocks.csv', 'x') as f:
    f.write(f'date,f1,f2,d12,f3,f4,d34,f5,f6,d56,f7,f8,d78\n{datetime.strftime(datetime.today() - timedelta(days=1), dateFormat)},{f1},{f2},{d12},{f3},{f4},{d34},{f5},{f6},{d56},{f7},{f8},{d78}')