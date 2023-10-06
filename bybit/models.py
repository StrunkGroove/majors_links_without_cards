from django.db import models


class BybitSpotData(models.Model):
    first = models.CharField(max_length=10)
    second = models.CharField(max_length=10)
    price = models.FloatField()

    class Meta:
        db_table = 'bybit_spot'
