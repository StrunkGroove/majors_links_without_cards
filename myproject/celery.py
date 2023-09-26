import os
from datetime import timedelta
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')

app = Celery('myproject')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


app.conf.beat_schedule = {

    'spot-binance-task': {
        'task': 'binance.tasks.main',
        'schedule': 10.0,
    },

    'spot-huobi-task': {
        'task': 'huobi.tasks.main',
        'schedule': 10.0,
    },

    'spot-kucoin-task': {
        'task': 'kucoin.tasks.main',
        'schedule': 10.0,
    },

    'spot-okx-task': {
        'task': 'okx.tasks.main',
        'schedule': 10.0,
    },

    'spot-bybit-task': {
        'task': 'bybit.tasks.main',
        'schedule': 10.0,
    },

    'count-links-3-task': {
        'task': 'count_links_3.tasks.main',
        'schedule': 60.0,
    },

    'count-links-2-task': {
        'task': 'count_links_2.tasks.main',
        'schedule': 30.0,
    },

    'pars-best-zip-task': {
        'task': 'best_change_zip.tasks.main',
        'schedule': 30.0,
    },

    'update-best-exchange-info-task': {
        'task': 'best_change_parsing.tasks.main',
        'schedule': 300.0,
    },
}