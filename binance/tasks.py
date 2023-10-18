import aiohttp
import asyncio

from myproject.celery import app
from base_app.info import key_binance, crypto_list, ban_list_binance
from django.core.cache import cache


async def fetch_data(session, url):
    async with session.get(url) as response:
        status_code = response.status

        if status_code == 200:
            return await response.json()
        else:
            print(status_code)

async def fetch_all():
    urls = [
        'https://api.binance.com/api/v3/ticker/price',
        'https://api.binance.com/api/v3/ticker/bookTicker',
    ]

    async with aiohttp.ClientSession() as session:
        data_price, data_book = await asyncio.gather(
            fetch_data(session, urls[0]), 
            fetch_data(session, urls[1])
        )
    return data_price, data_book

def del_fake(data_price, data_book):
    indices_to_remove = []
    
    for i in range(len(data_price) - 1, -1, -1):
        ad = data_price[i]
        symbol = ad['symbol']
        if symbol in ban_list_binance:
            indices_to_remove.append(i)

    for i in indices_to_remove:
        data_price.pop(i)
        data_book.pop(i)

def create_symbols():
    symbols = {}
    for i in crypto_list:
        for j in crypto_list:
            symbol = i + j
            symbols[symbol] = {
                'first': i,
                'second': j,
            }
    return symbols

def merge(data_price, data_book, key):
    symbols = create_symbols()
    merge_list = []
    for i in range(len(data_price)):
        ad_price = data_price[i]
        ad_book = data_book[i]

        symbol = ad_price['symbol']
        symbol = symbols.get(symbol)
        if not symbol: continue

        merge_list.append({
            'first': symbol['first'],
            'second': symbol['second'],
            'price': float(ad_price['price']),
            'bid_price': float(ad_book['bidPrice']),
            'ask_price': float(ad_book['askPrice']),
            'bid_qty': float(ad_book['bidQty']),
            'ask_qty': float(ad_book['askQty']),
            'ex': key,
        })
    return merge_list

def save(data):
    time_cash = 60
    cache.set(key_binance, data, time_cash)

@app.task
def main():
    data_price, data_book = asyncio.run(fetch_all())
    del_fake(data_price, data_book)
    data = merge(data_price, data_book, key_binance)
    save(data)
    return len(data)