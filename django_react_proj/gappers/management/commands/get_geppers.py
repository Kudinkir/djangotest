from django.core.management.base import BaseCommand, CommandError
import requests
import pandas as pd
from datetime import datetime, timedelta
import os


class Command(BaseCommand):
    help = "Closes the specified poll for voting"

    def handle(self, *args, **options):
        dateFormat = '%Y-%m-%d'
        thisDir = os.path.realpath(__file__).replace(__file__, '')
        print(os.path.realpath(__file__))
        quit()
        targetDay = datetime.strftime(
            datetime.today() - timedelta(days=1), dateFormat)

        _from = targetDay
        _to = targetDay
        increase = 20
        try:
            theDF = self.getTickers(increase, _from)
            theDF.columns = [
                'ticker', 'open', 'close', 'high',
                'low', 'vwap', 'volume', 'gap%', 'date'
            ]
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
                otherDF = self.getTickers(increase, date)
            except Exception:
                current_day += oneDay
                fails += 1
                idx += 1
                continue
            otherDF.columns = ['ticker', 'open', 'close', 'high', 'low', 'vwap', 'volume', 'gap%', 'date']

            try:
                new_gappers = otherDF[~otherDF['ticker'].isin(theDF['ticker'])]
            except Exception:
                current_day += oneDay
                fails += 1
                idx += 1
                continue

            theDF = pd.concat([theDF, new_gappers], axis=0)

            current_day += oneDay
            idx += 1
            passes += 1

        theDF = theDF[~(theDF['ticker'].str.len() == 5)]

        csv = theDF.to_csv('results.csv', index=False)  # f - только строки с параметрами внутри (тут не надо)
        return csv

    def getTickers(self, increasePercent, date):
        api_key = "rY7jzsLlcwNmsjs1WwQftckwGrTvrCK9"
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
