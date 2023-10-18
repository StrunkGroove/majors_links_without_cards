import aiohttp
import asyncio

from myproject.celery import app
from base_app.info import key_huobi, crypto_list, ban_list_huobi
from django.core.cache import cache


async def fetch_data(session, url):
    async with session.get(url) as response:
        status_code = response.status

        if status_code == 200:
            res = await response.json()
            return res['data']

        else:
            print(status_code)

async def fetch_all():
    urls = [
        'https://api-aws.huobi.pro/market/tickers',
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
        symbol = ad['symbol'].upper()
        if symbol in ban_list_huobi:
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
        symbol = ad['symbol'].upper()
        symbol = symbols.get(symbol)
        if not symbol: continue

        price = float(ad['close'])
        bid_price = float(ad['bid'])
        ask_price = float(ad['ask'])
        if price == 0 or bid_price == 0 or ask_price == 0: continue

        merge_list.append({
            'first': symbol['first'],
            'second': symbol['second'],
            'price': price,
            'bid_price': bid_price,
            'ask_price': ask_price,
            'bid_qty': float(ad['bidSize']),
            'ask_qty': float(ad['askSize']),
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
    data = merge(data, key_huobi)
    save(data, key_huobi)
    return len(data)