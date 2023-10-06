import hashlib

from myproject.celery import app
from base_app.info import (
    key_mexc, key_binance, key_bybit, key_okx, key_kucoin, key_huobi, 
    key_bitget, key_pancake, key_gateio, base_token_2
)

from django.core.cache import cache


def unique_keys(all_ex):
    unique_keys = {}

    for ex_first in all_ex:
        for ex_second in all_ex:
            key = f'{ex_first}--{ex_second}'
            unique_keys[key] = []
    return unique_keys


def calculate_spread(price_first, price_second):
    spread = ((price_first * price_second) - 1) * 100
    return spread


def custom_round_func(price):
    price = round(price, 4)
    if price == 0:
        return '0.000...'
    return price


def get_data_from_redis(all_data, all_ex, key, ex):
    data = cache.get(key)
    if not data:
        return f'Data is None {ex}'
    all_data[ex] = data
    all_ex.append(ex)


def count(ex_first, ex_second, data_first, data_second, dict, first_key, second_key):
    n = 0
    key = f'{ex_first}--{ex_second}'
    for key_first, ad_first in data_first.items():
        ad_give_first = ad_first['first']
        if ad_give_first not in base_token_2:
            continue
        ad_get_first = ad_first['second']
        bid_qty_first = ad_first['bid_qty']
        ask_qty_first = ad_first['ask_qty']
        price_first = ad_first[first_key]
        real_price_first = ad_first[f'real_{first_key}']

        for key_second, ad_second in data_second.items():
            ad_give_second = ad_second['first']
            ad_get_second = ad_second['second']
            if ad_get_first != ad_give_second or ad_get_second != ad_give_first:
                continue
            price_second = ad_second[second_key]
            bid_qty_second = ad_second['bid_qty']
            ask_qty_second = ad_second['ask_qty']
            real_price_second = ad_second[f'real_{second_key}']

            spread = calculate_spread(price_first, price_second)

            spread = round(spread, 2)

            if spread < 0.2:
                continue

            for_hash = (
                f'{ex_first}-'
                f'-{ex_second}-'
                f'-{ad_give_first}-'
                f'-{ad_get_first}'
            )
            hash_object = hashlib.sha256()
            hash_object.update(for_hash.encode())
            hashed = hash_object.hexdigest()

            record = {
                'exchange_first': ex_first,
                'price_first': custom_round_func(real_price_first),
                'full_price_first': '{:.12f}'.format(real_price_first),
                'give_first': ad_give_first,
                'get_first': ad_get_first,
                'bid_qty_first': bid_qty_first,
                'ask_qty_first': ask_qty_first,

                'exchange_second': ex_second,
                'price_second': custom_round_func(real_price_second),
                'full_price_second': '{:.12f}'.format(real_price_second),
                'give_second': ad_give_second,
                'get_second': ad_get_second,
                'bid_qty_second': bid_qty_second,
                'ask_qty_second': ask_qty_second,

                'spread': spread,
                'hash': hashed,
            }

            if ex_first == 'pancake':
                record['base_address'] = ad_first['base_address']
                record['quoto_address'] = ad_first['quoto_address']

            elif ex_second == 'pancake':
                record['base_address'] = ad_second['base_address']
                record['quoto_address'] = ad_second['quoto_address']


            dict[key].append(record)
            n += 1
    return n


def sorted_dict(dict):
    sorted_data = sorted(
        dict,
        key=lambda x: x['spread'],
        reverse=True
    )


def save_db(data, type_trade):
    time_cash = 60
    for key, dict in data.items():
        key = f'{type_trade}--{key}'
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
    # get_data_from_redis(all_data, all_exchanges, key_mexc, 'mexc')
    get_data_from_redis(all_data, all_exchanges, key_bitget, 'bitget')
    get_data_from_redis(all_data, all_exchanges, key_pancake, 'pancake')
    get_data_from_redis(all_data, all_exchanges, key_gateio, 'gateio')

    if len(all_data) == 0:
        return 'All data is None!'

    bid_key = 'bid_price'
    ask_key = 'ask_price'

    n = 0
    dict_bid_ask = unique_keys(all_exchanges)
    for ex_first, data_first in all_data.items():
        for ex_second, data_second in all_data.items():
            n += count(ex_first, ex_second, data_first, data_second, dict_bid_ask, bid_key, ask_key)

    # n = 0
    dict_bid_bid = unique_keys(all_exchanges)
    for ex_first, data_first in all_data.items():
        for ex_second, data_second in all_data.items():
            n += count(ex_first, ex_second, data_first, data_second, dict_bid_bid, bid_key, bid_key)

    # n = 0
    dict_ask_ask = unique_keys(all_exchanges)
    for ex_first, data_first in all_data.items():
        for ex_second, data_second in all_data.items():
            n += count(ex_first, ex_second, data_first, data_second, dict_ask_ask, ask_key, ask_key)

    # n = 0
    dict_ask_bid = unique_keys(all_exchanges)
    for ex_first, data_first in all_data.items():
        for ex_second, data_second in all_data.items():
            n += count(ex_first, ex_second, data_first, data_second, dict_ask_bid, ask_key, bid_key)

    save_db(dict_bid_ask, 'SELL-BUY')
    save_db(dict_bid_bid, 'SELL-SELL')
    save_db(dict_ask_ask, 'BUY-BUY')
    save_db(dict_ask_bid, 'BUY-SELL')

    return n