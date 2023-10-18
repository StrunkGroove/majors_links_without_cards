import aiohttp
import asyncio

from myproject.celery import app
from base_app.info import key_kucoin, crypto_list, ban_list_kucoin
from django.core.cache import cache


async def fetch_data(session, url):
    async with session.get(url) as response:
        status_code = response.status

        if status_code == 200:
            res = await response.json()
            return res['data']['ticker']

        else:
            print(status_code)

async def fetch_all():
    urls = [
        'https://api.kucoin.com/api/v1/market/allTickers',
    ]

    async with aiohttp.ClientSession() as session:
        data = await asyncio.gather(
            fetch_data(session, urls[0])
        )
    return data[0]

def del_fake(data):
    indices_to_remove = []
    
    for i in range(len(data) - 1, -1, -1):
        ad = data[i]
        symbol = ad['symbol'].replace('-', '')
        if symbol in ban_list_kucoin:
            indices_to_remove.append(i)

    for i in indices_to_remove:
        data.pop(i)

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

def merge(data, key):
    symbols = create_symbols()
    merge_list = []
    for i in range(len(data)):
        ad = data[i]
        symbol = ad['symbol'].replace('-', '')
        symbol = symbols.get(symbol)
        if not symbol: continue

        price = float(ad['last'])
        bid_price = float(ad['buy'])
        ask_price = float(ad['sell'])
        if price == 0 or bid_price == 0 or ask_price == 0: continue

        merge_list.append({
            'first': symbol['first'],
            'second': symbol['second'],
            'price': price,
            'bid_price': bid_price,
            'ask_price': ask_price,
            'bid_qty': float(ad['volValue']) / 24,
            'ask_qty': float(ad['volValue']) / 24,
            'ex': key,
        })
    return merge_list

def save(data, key):
    time_cash = 60
    cache.set(key, data, time_cash)

@app.task
def main():
    data = asyncio.run(fetch_all())
    del_fake(data)
    data = merge(data, key_kucoin)
    save(data, key_kucoin)
    return len(data)