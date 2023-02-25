import platform

import aiohttp
import asyncio
import requests
import sys
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor

days_to_count = int(sys.argv[1])
if days_to_count > 10:
    while True:
        days_to_count = int(input('10 days max. Enter number of days: '))
        if days_to_count <= 10:
            break
date = datetime.now()
date_for_url = datetime.now().strftime('%d.%m.%Y')
delta = timedelta(days=1)
url_privat = 'https://api.privatbank.ua/p24api/exchange_rates?date='

urls = []

for day in range(days_to_count):
    urls.append(url_privat + date_for_url)
    date -= delta
    date_for_url = date.strftime('%d.%m.%Y') 

def get_exchange(url):
    result = requests.get(url)
    return result.json()

async def get_exchange_rates():
    loop = asyncio.get_running_loop()

    with ThreadPoolExecutor(days_to_count) as pool:
        futures = [loop.run_in_executor(pool, get_exchange, url) for url in urls]
        result = await asyncio.gather(*futures, return_exceptions=True)
        return result
    
if __name__ == "__main__":
    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    rates = asyncio.run(get_exchange_rates())
    result = []

    for rate in rates:
        
        format_rate = {
          rate['date']: {
            'EUR': {
            'sale': rate['exchangeRate'][8]['saleRate'],
            'purchase': rate['exchangeRate'][8]['purchaseRate'],
            },
            'USD': {
            'sale': rate['exchangeRate'][23]['saleRate'],
            'purchase': rate['exchangeRate'][23]['purchaseRate'],
            }
          }
        }
        result.append(format_rate)
        
    print(result)