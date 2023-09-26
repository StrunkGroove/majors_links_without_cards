from myproject.celery import app
from base_app.info import key_best_rates, key_binance, key_bybit, base_token, exchanges
from best_change_zip.models import LinksCryptoInfo
from best_change_parsing.models import LinksExchangeInfo

from django.core.cache import cache


def unique_keys():
    unique_keys = {}

    for token in base_token:
        key = f'{token}'
        unique_keys[key] = []
    return unique_keys


def calculate_spread_with_fee(ad_price_first, best_price, ad_price_second):
    fee = 0.15
    spread_with_fee = (ad_price_first * best_price * ad_price_second - 1) * 100
    return spread_with_fee


def get_data_from_redis(key):
    data = cache.get(key)
    return data


def get_crypto_info_dict():
    crypto_info_objects = LinksCryptoInfo.objects.all()

    crypto_info_dict = {}
    for obj in crypto_info_objects:
        crypto_info_dict[obj.crypto_id] = {
            'crypto_name': obj.crypto_name,
            'abbr': obj.abbr,
        }
    return crypto_info_dict


def get_exchange_info_dict():
    exchange_info_objects = LinksExchangeInfo.objects.all()

    exchange_info_dict = {}
    for obj in exchange_info_objects:
        exchange_info_dict[obj.exchange_id] = {
            'exchange_id': obj.exchange_id,
            'exchange_name': obj.exchange_name,
            'info_reverse': obj.info_reverse,
            'info_age': obj.info_age,
            'info_star': obj.info_star,
            'info_verification': obj.info_verification,
            'info_registration': obj.info_registration,
            'addition_floating': obj.addition_floating,
            'addition_verifying': obj.addition_verifying,
            'addition_manual': obj.addition_manual,
            'addition_percent': obj.addition_percent,
            'addition_otherin': obj.addition_otherin,
            'addition_reg': obj.addition_reg,
        }
    return exchange_info_dict


def count_link_3_actions(dict, best_change_data, data, exchange):
    n = 0
    crypto_info_dict = get_crypto_info_dict()
    exchange_info_dict = get_exchange_info_dict()

    for token_first, ad_first in data.items():
        ad_give_first = ad_first['first']
        if ad_give_first not in base_token:
            continue
        ad_get_first = ad_first['second']
        ad_price_first = float(ad_first['price'])

        for best_row in best_change_data:
            best_give = best_row['crypto_name_give']
            if ad_get_first != best_give:
                continue
            best_give_number = best_row['crypto_number_give']
            best_get_number = best_row['crypto_number_get']
            best_get = best_row['crypto_name_get']
            
            best_price_give = float(best_row['rate_give'])
            best_price_get = float(best_row['rate_get'])
            best_price = best_price_get / best_price_give

            for token_second, ad_second in data.items():
                ad_give_second = ad_second['first']
                ad_get_second = ad_second['second']
                if best_get != ad_give_second or ad_get_second != ad_give_first:
                    continue
                ad_price_second = float(ad_second['price'])

                spread_with_fee = calculate_spread_with_fee(
                    ad_price_first,
                    best_price,
                    ad_price_second
                )

                spread_with_fee = round(spread_with_fee, 2)

                if spread_with_fee < 0.2:
                    continue

                record = {
                    'exchange': exchange,
                    'ad_price_first': round(ad_price_first, 5),
                    'ad_give_first': ad_give_first,
                    'ad_get_first': crypto_info_dict[best_get_number],

                    'ad_price_second': round(ad_price_second, 5),
                    'ad_give_second': crypto_info_dict[best_give_number],
                    'ad_get_second': ad_get_second,

                    'best_price': round(best_price, 5),
                    'best_full_price': round(best_price, 11),
                    'spread_with_fee': spread_with_fee,

                    'exchange_info': exchange_info_dict[best_row['exchange_id']],
                    'available': best_row['available'],
                    'negative_reviews': best_row['negative_reviews'],
                    'positive_reviews': best_row['positive_reviews'],
                    'dont_use': best_row['dont_use'],
                    'lim_min': best_row['lim_min'],
                    'lim_max': best_row['lim_max'],
                }
                dict[ad_give_first].append(record)
                n += 1
    return n


def sorted_dict(dict):
    sorted_data = sorted(
        dict,
        key=lambda x: x['spread_with_fee'],
        reverse=True
    )

    grouped_objects = {}
    
    for obj in sorted_data:
        key = (
            f"{obj['ad_give_first']}--"
            f"{obj['ad_get_first']['abbr']}--"
            f"{obj['ad_give_second']['abbr']}--"
            f"{obj['ad_get_second']}"
        )

        if key not in grouped_objects:
            grouped_objects[key] = []
        grouped_objects[key].append(obj)

    return grouped_objects


def save_db(data, exchange):
    time_cash = 60
    for key, dict in data.items():
        sort_data = sorted_dict(dict)
        key = f'{exchange}--{key}'
        cache.set(key, sort_data, time_cash)


def process_data(best_change_data, exchange, key):
    dict = unique_keys()
    data = get_data_from_redis(key)
    if not data:
        return f'No data {exchange}!'

    len_links = count_link_3_actions(dict, best_change_data, data, exchange)
    save_db(dict, exchange)
    return f'{exchange}: {len_links}'


@app.task
def main():
    best_change_data = get_data_from_redis(key_best_rates)
    if not best_change_data:
        return f'No data Best Change!'
    binance_response = process_data(best_change_data, 'binance', key_binance)
    bybit_response = process_data(best_change_data, 'bybit', key_bybit)

    # return f'bybit: {bybit_response}'
    return f'binance: {binance_response}, bybit: {bybit_response}'