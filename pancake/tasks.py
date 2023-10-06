import requests
import aiohttp
import asyncio
import redis

from myproject.celery import app
from base_app.info import key_pancake, crypto_list, ban_list_pancake
from django.core.cache import cache


def handler_data(data, responses):
    data = data['data']['pageList']

    for ad in data:
        first_token = ad['baseTokenSymbol']
        base_address = ad['baseTokenAddress']
        second_token = ad['quotoTokenSymbol']
        quoto_address = ad['quotoTokenAddress']
        platform_name = ad['platformName']
        price = ad['priceQuote']
        
        price = float(price)
        exchange = 'pancake'

        token = first_token + second_token
        if token in ban_list_pancake:
            continue

        responses[token] = {
            'first': first_token,
            'base_address': base_address,
            'second': second_token,
            'quoto_address': quoto_address,
            'exchange': exchange,
            
            'price': price,
            'real_price': price,
            'bid_price': price,
            'ask_price': price,
            'bid_qty': 1000000,
            'ask_qty': 1000000,
            'real_ask_price': price,
            'real_bid_price': price,
        }

        responses[f'{token}_new'] = {
            'first': second_token,
            'base_address': quoto_address,
            'second': first_token,
            'quoto_address': base_address,
            'exchange': exchange,

            'price': 1/price,
            'real_price': price,
            'bid_price': 1/price,
            'ask_price': 1/price,
            'bid_qty': 1000000,
            'ask_qty': 1000000,
            'real_ask_price': price,
            'real_bid_price': price,
        }


async def fetch_data(session, url, headers, responses):
    async with session.get(url, headers=headers) as response:
        status_code = response.status

        if status_code == 200:
            data = await response.json()
            handler_data(data, responses)
        else:
            print(status_code)


async def fetch_all():
    url_template = 'https://api.coinmarketcap.com/dexer/v3/platformpage/pair-pages?platform-id=14&dexer-id=6706&sort-field=txns24h&category=spot&page={page}'
    headers = {
        'Host': 'api.coinmarketcap.com',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0',
        'Accept': 'application/json',
    }

    responses = {}
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_data(session, url_template.format(page=page), headers, responses) for page in range(23)]
        await asyncio.gather(*tasks)
    
    return responses


def save_db(responses):
    time_cash = 60
    cache.set(key_pancake, responses, time_cash)


@app.task
def main():
    responses = asyncio.run(fetch_all())
    save_db(responses)
    return len(responses)