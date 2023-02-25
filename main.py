import asyncio
import platform
import logging
import sys
from datetime import datetime, timedelta

import aiohttp

def get_urls_by_date(days: int):

    if days > 10:
        while True:
            days = int(input('10 days max. Enter number of days: '))
            if days <= 10:
                break

    date = datetime.now()
    date_for_url = datetime.now().strftime('%d.%m.%Y')
    delta = timedelta(days=1)
    url = 'https://api.privatbank.ua/p24api/exchange_rates?date='

    urls = []

    for day in range(days):
        urls.append(url + date_for_url)
        date -= delta
        date_for_url = date.strftime('%d.%m.%Y')

    return urls

async def request(url):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    return data
                logging.error(f'error status {response.status} for {url}')
        except aiohttp.ClientConnectorError as e:
            logging.error(f'connection error for {url}: {e}')
    return None
    
async def main():
    r = []
    for url in urls:
        r.append(request(url))
    rates = await asyncio.gather(*r)
    
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

    return result

if __name__ == "__main__":
    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    urls = get_urls_by_date(int(sys.argv[1]))
    result = asyncio.run(main())
    print(result)
    
    
