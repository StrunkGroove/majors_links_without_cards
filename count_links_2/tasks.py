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
    if price_first == 0: return 0
    fee = 0.15
    spread = (((price_second - price_first) / price_first) - 1) * 100
    spread = spread - fee
    return spread
    return round(spread, 2)


def custom_round_func(price):
    price = round(price, 4)
    if price == 0:
        return '0.000...'
    return price


# def count(ex_first, ex_second, data_first, data_second, dict, first_key, second_key):
#     def create_hash():
#         for_hash = (
#             f'{ex_first}-'
#             f'-{ex_second}-'
#             f'-{give_first}-'
#             f'-{get_first}'
#         )
#         hash_object = hashlib.sha256()
#         hash_object.update(for_hash.encode())
#         hashed = hash_object.hexdigest()
#         return hashed

#     def create_record():
#         return {
#             'exchange_first': ex_first,
#             'exchange_second': ex_second,

#             'price_first': custom_round_func(price_first),
#             'price_second': custom_round_func(price_second),

#             'full_price_first': '{:10f}'.format(price_first),
#             'full_price_second': '{:10f}'.format(price_second),

#             'base': base_first,
#             'quote': quote_first,
            
#             'bid_qty_first': bid_qty_first,
#             'ask_qty_first': ask_qty_first,
#             'bid_qty_second': bid_qty_second,
#             'ask_qty_second': ask_qty_second,

#             # 'give_second': base_second,
#             # 'get_second': quote_second,

#             'spread': spread,
#             'hash': create_hash(),
#         }

#     n = 0
#     key = f'{ex_first}--{ex_second}'
    
#     for ad_first in data_first:
#         give_first = ad_first['first']
#         get_first = ad_first['second']

#         base_first = None
#         if give_first in base_token_2: 
#             base_first = give_first
#             quote_first = get_first
#         elif get_first in base_token_2: 
#             base_first = get_first
#             quote_first = give_first
#         elif base_first is None:
#             continue

#         for ad_second in data_second:
#             give_second = ad_second['first']
#             get_second = ad_second['second']

#             base_second = None
#             if base_first == give_second:
#                 base_second = give_second
#                 quote_second = get_second
#                 same = True
#             elif base_first == get_second:
#                 base_second = get_second
#                 quote_second = give_second
#                 same = False
#             elif base_second is None:
#                 continue

#             if quote_first != quote_second:
#                 continue

#             price_first = ad_first[first_key]
#             bid_qty_first = ad_first['bid_qty']
#             ask_qty_first = ad_first['ask_qty']

#             price_second = ad_second[second_key]
#             bid_qty_second = ad_second['bid_qty']
#             ask_qty_second = ad_second['ask_qty']

#             if same == True:
#                 spread = calculate_spread(price_first, price_second)
#                 record = create_record()
#                 if spread < 0.2: continue
#             elif same == False:
#                 if price_second == 0:
#                     continue

#                 spread = calculate_spread(price_first, 1/price_second)
#                 record = create_record()
#                 if spread < 0.2: continue
#             dict[key].append(record)
#             n += 1
#     return n

def count(ex_first, ex_second, data_first, data_second, dict, first_key, second_key):
    def create_hash():
        for_hash = (
            f'{ex_first}-'
            f'-{ex_second}-'
            f'-{base_first}-'
            f'-{quote_first}'
        )
        hash_object = hashlib.sha256()
        hash_object.update(for_hash.encode())
        hashed = hash_object.hexdigest()
        return hashed

    def create_record():
        return {
            'exchange_first': ex_first,
            'exchange_second': ex_second,

            'price_first': custom_round_func(price_first),
            'price_second': custom_round_func(price_second),

            'full_price_first': '{:10f}'.format(price_first),
            'full_price_second': '{:10f}'.format(price_second),

            # 'base': base_first,
            # 'quote': quote_first,
            
            'bid_qty_first': bid_qty_first,
            'ask_qty_first': ask_qty_first,
            'bid_qty_second': bid_qty_second,
            'ask_qty_second': ask_qty_second,

            'give_first': base_first,
            'get_first': quote_first,
            'give_second': base_second,
            'get_second': quote_second,

            'spread': spread,
            'hash': create_hash(),
        }

    n = 0
    key = f'{ex_first}--{ex_second}'
    
    for ad_first in data_first:
        base_first = ad_first['first']
        quote_first = ad_first['second']

        for ad_second in data_second:
            base_second = ad_second['first']
            quote_second = ad_second['second']

            if base_first != base_second \
            or quote_first != quote_second:
                continue

            price_first = ad_first[first_key]
            bid_qty_first = ad_first['bid_qty']
            ask_qty_first = ad_first['ask_qty']

            price_second = ad_second[second_key]
            bid_qty_second = ad_second['bid_qty']
            ask_qty_second = ad_second['ask_qty']

            spread = calculate_spread(price_first, price_second)
            if spread < 0.2: continue
            dict[key].append(create_record())
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
    def count_links(type, key_first, key_second):
        dict = unique_keys(exchanges)
        n = 0
        for ex_first, data_first in data.items():
            for ex_second, data_second in data.items():
                n += count(ex_first, ex_second, data_first, data_second, dict, key_first, key_second)
        save_db(dict, type)
        return n

    def get_data(all_data, exchanges, key):
        data = cache.get(key)
        if not data:
            return f'Data is None {key}'
        all_data[key] = data
        exchanges.append(key)

    data = {}
    exchanges = []
    get_data(data, exchanges, key_binance)
    get_data(data, exchanges, key_bybit)
    get_data(data, exchanges, key_okx)
    get_data(data, exchanges, key_kucoin)
    get_data(data, exchanges, key_huobi)
    get_data(data, exchanges, key_bitget)
    get_data(data, exchanges, key_pancake)
    get_data(data, exchanges, key_gateio)

    if len(data) == 0:
        return 'All data is None!'

    bid = 'bid_price'
    ask = 'ask_price'
    
    n = 0
    n += count_links('SELL-BUY', bid, ask)
    n += count_links('SELL-SELL', bid, bid)
    n += count_links('BUY-BUY', ask, ask)
    n += count_links('BUY-SELL', ask, bid)
    return n