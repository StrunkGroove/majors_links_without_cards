import requests
import redis

from myproject.celery import app
from base_app.info import key_bitget, crypto_list, accept_list_bitget, rc
from django.core.cache import cache


def get_data(url):
    response = requests.get(url)
    data = response.json()
    return data['data']


def del_fake(data):
    indices_to_remove = []
    
    for i in range(len(data) - 1, -1, -1):
        ad = data[i]
        symbol = ad['symbol']
        if symbol not in accept_list_bitget:
            indices_to_remove.append(i)

    for i in indices_to_remove:
        data.pop(i)


def create_all_pair():
    token_dict = {}

    for first_token in crypto_list:
        for second_token in crypto_list:
            if first_token != second_token:
                token = first_token + second_token
                token_dict[token] = {
                    'first':first_token,
                    'second':second_token,
                    'exchange':'bitget',
                }
    return token_dict


def append_info(data, token_dict):
    for token in token_dict.copy():
        for ad in data:
            symbol = ad['symbol']

            if token != symbol:
                continue

            price = ad['close']
            bid_price = ad['buyOne']
            ask_price = ad['sellOne']
            bid_qty = ad['bidSz']
            ask_qty = ad['askSz']
            
            price = float(price)
            bid_price = float(bid_price)
            ask_price = float(ask_price)
            bid_qty = float(bid_qty)
            ask_qty = float(ask_qty)

            token_dict[symbol]['price'] = price
            token_dict[symbol]['real_price'] = price
            token_dict[symbol]['bid_price'] = bid_price
            token_dict[symbol]['ask_price'] = ask_price
            token_dict[symbol]['bid_qty'] = bid_qty
            token_dict[symbol]['ask_qty'] = ask_qty
            token_dict[symbol]['real_ask_price'] = ask_price
            token_dict[symbol]['real_bid_price'] = bid_price
            break
        else:
            del token_dict[token]
    return token_dict


def duplicate(token_dict):
    for token in token_dict.copy():
        ad = token_dict[token]

        first = ad['first']
        second = ad['second']
        price = ad['price']
        bid_price = ad['bid_price']
        ask_price = ad['ask_price']
        bid_qty = ad['bid_qty']
        ask_qty = ad['ask_qty']
        exchange = ad['exchange']

        key = second + first
        token_dict[key] = {
            'first': second,
            'second': first,
            'price': 1/price,
            'real_price': price,
            'bid_price': 1/bid_price,
            'ask_price': 1/ask_price,
            'real_ask_price': ask_price,
            'real_bid_price': bid_price,
            'bid_qty': bid_qty,
            'ask_qty': ask_qty,
            'exchange': exchange,
        }


def save_db(token_dict):
    time_cash = 60
    cache.set(key_bitget, token_dict, time_cash)


@app.task
def main():
    url_bid_ask = 'https://api.bitget.com/api/spot/v1/market/tickers'

    data = get_data(url_bid_ask)

    # del_fake(data_bid_ask)

    token_dict = create_all_pair()

    append_info(data, token_dict)

    duplicate(token_dict)
    save_db(token_dict)
    return len(token_dict)