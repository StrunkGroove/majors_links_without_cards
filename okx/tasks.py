import requests

from myproject.celery import app
from base_app.info import key_okx, crypto_list, ban_list_okx
from django.core.cache import cache


def get_data():
    url = "https://www.okx.com/api/v5/market/tickers?instType=SPOT"
    response = requests.get(url)
    data = response.json()
    data = data['data']
    return data


def del_fake(data):
    indices_to_remove = []
    
    for i in range(len(data) - 1, -1, -1):
        ad = data[i]
        symbol = ad['instId'].replace('-', '')
        if symbol in ban_list_okx:
            indices_to_remove.append(i)

    for i in indices_to_remove:
        data.pop(i)


def create_all_pair(token_dict):
    for first_token in crypto_list:
        for second_token in crypto_list:
            if first_token != second_token:
                token = first_token + second_token
                token_dict[token] = {'first':first_token, 'second':second_token}
    return token_dict


def append_price(data, token_dict):
    for token in token_dict.copy():
        for ad in data:
            symbol = ad['instId'].replace('-', '')

            if token != symbol:
                continue

            price = ad['last']
            token_dict[symbol]['price'] = price
            break
        else:
            del token_dict[token]
    return token_dict


def duplicate(token_dict):
    for token in token_dict.copy():
        ad = token_dict[token]

        first = ad['first']
        second = ad['second']
        price = float(ad['price'])

        key = token + '_new'
        token_dict[key] = {'first':second, 'second':first, 'price':1/price}


def save_db(token_dict):
    time_cash = 60
    cache.set(key_okx, token_dict, time_cash)


@app.task
def main():
    token_dict = {}

    data = get_data()
    del_fake(data)
    create_all_pair(token_dict)
    append_price(data, token_dict)
    duplicate(token_dict)
    save_db(token_dict)
    return len(token_dict)
