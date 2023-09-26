from myproject.celery import app
from base_app.info import key_binance, key_bybit, key_okx, key_kucoin, key_huobi, base_token_2

from django.core.cache import cache


def unique_keys(all_ex):
    unique_keys = {}

    for ex_first in all_ex:
        for ex_second in all_ex:
            key = f'{ex_first}--{ex_second}'
            unique_keys[key] = []
    return unique_keys


def calculate_spread(price_first, price_second):
    spread = (price_first * price_second - 1) * 100
    return spread


def get_data_from_redis(all_data, all_ex, key, ex):
    data = cache.get(key)
    if not data:
        return f'Data is None {ex}'
    all_data[ex] = data
    all_ex.append(ex)


def count(ex_first, ex_second, data_first, data_second, dict):
    n = 0
    key = f'{ex_first}--{ex_second}'
    for key_first, ad_first in data_first.items():
        ad_give_first = ad_first['first']
        if ad_give_first not in base_token_2:
            continue
        ad_get_first = ad_first['second']
        price_first = float(ad_first['price'])

        for key_second, ad_second in data_second.items():
            ad_give_second = ad_second['first']
            ad_get_second = ad_second['second']
            if ad_get_first != ad_give_second or ad_get_second != ad_give_first:
                continue
            price_second = float(ad_second['price'])

            spread = calculate_spread(price_first, price_second)

            spread = round(spread, 2)

            if spread < 0.2:
                continue


            record = {
                'exchange_first': ex_first,
                'price_first': round(price_first, 5),
                'give_first': ad_give_first,
                'get_first': ad_get_first,

                'exchange_second': ex_second,
                'price_second': round(price_second, 5),
                'give_second': ad_give_second,
                'get_second': ad_get_second,

                'spread': spread,
            }
            dict[key].append(record)
            n += 1
    return n


def sorted_dict(dict):
    sorted_data = sorted(
        dict,
        key=lambda x: x['spread'],
        reverse=True
    )


def save_db(data):
    time_cash = 60
    for key, dict in data.items():
        sorted_dict(dict)
        cache.set(key, dict, time_cash)


@app.task
def main():
    all_data = {}
    all_exchanges = []
    get_data_from_redis(all_data, all_exchanges, key_binance, 'binance')
    get_data_from_redis(all_data, all_exchanges, key_bybit, 'bybit')
    get_data_from_redis(all_data, all_exchanges, key_okx, 'okx')
    get_data_from_redis(all_data, all_exchanges, key_kucoin, 'kucoin')
    get_data_from_redis(all_data, all_exchanges, key_huobi, 'huobi')

    if len(all_data) == 0:
        return 'All data is None!'
        
    n = 0
    dict = unique_keys(all_exchanges)
    for ex_first, data_first in all_data.items():
        for ex_second, data_second in all_data.items():
            n += count(ex_first, ex_second, data_first, data_second, dict)

    save_db(dict)
    return n