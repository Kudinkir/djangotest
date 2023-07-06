from django.db import models

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
