from django.db import models
from best_change_zip.models import LinksCryptoInfo
from best_change_parsing.models import LinksExchangeInfo


class AllLinksHash3(models.Model):
    hash_info = models.CharField(max_length=150)
    base_token = models.CharField(max_length=50)
    base_exchange = models.CharField(max_length=50)

    best_first_token = models.ForeignKey(
        LinksCryptoInfo,
        on_delete=models.CASCADE
    )
    best_first_token = models.ForeignKey(
        LinksCryptoInfo,
        on_delete=models.CASCADE
    )
    exchange_info = models.ForeignKey(
        LinksExchangeInfo,
        on_delete=models.CASCADE
    )

    class Meta:
        db_table = 'all_links_hash_3'