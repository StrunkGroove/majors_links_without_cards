from django.db import models


class BinanceSpotData(models.Model):
    first = models.CharField(max_length=10)
    second = models.CharField(max_length=10)
    price = models.FloatField()

    class Meta:
        db_table = 'binance_spot'