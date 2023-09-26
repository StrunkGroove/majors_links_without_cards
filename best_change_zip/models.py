from django.db import models
from best_change_parsing.models import LinksExchangeInfo

class LinksCryptoInfo(models.Model):
    id = models.AutoField(primary_key=True)
    crypto_id = models.IntegerField(unique=True) 
    crypto_name = models.CharField(max_length=40)
    abbr = models.CharField(max_length=10)

    class Meta:
        db_table = 'links_crypto_info'
        indexes = [
            models.Index(fields=['id']),
        ]