from django.db import models
import pandas as pd
from django.conf import settings



class Gappers(models.Model):
    ticker_name =models.CharField(max_length=255, blank=False, null=False)
    open = models.FloatField()
    close = models.FloatField()
    hight = models.FloatField()
    low = models.FloatField()
    vwap = models.FloatField()
    volume = models.FloatField()
    gap = models.FloatField()
    date = models.DateTimeField()

    def __str__(self):
        return self.ticker_name


class Results(models.Model):
#2023-07-12,280,404,-30.7%,358,235,52.3%,58,63,-7.9%,87,50,74.0%
    @staticmethod
    def getcsv():
        return pd.read_csv(str(settings.BASE_DIR)+"/main_part/results.csv")


class Upperblock(models.Model):
#2023-07-12,280,404,-30.7%,358,235,52.3%,58,63,-7.9%,87,50,74.0%
    @staticmethod
    def getcsv():
        return pd.read_csv(str(settings.BASE_DIR)+"/main_part/4upperblocks.csv")


class Final(models.Model):
    date=models.DateTimeField()
    dcount=models.FloatField()
    MA_5=models.FloatField()
    MA_15=models.FloatField()
    @staticmethod
    def getcsv():
        return pd.read_csv(str(settings.BASE_DIR)+"/main_part/results_final.csv")

class Script4(models.Model):
    @staticmethod
    def getcsv():
        return pd.read_csv(str(settings.BASE_DIR)+"/main_part/script4_results.csv")

class Stock_counts(models.Model):
    @staticmethod
    def getcsv():
        return pd.read_csv(str(settings.BASE_DIR)+"/main_part/stock_counts.csv")
