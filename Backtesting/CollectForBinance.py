from ast import Try
import requests, json, time
import pandas as pd
from pprint import pprint

params = {
    "limit": 1000,
    "symbol": "INJUSDT",
    "endTime": '1680912000000'
}

funding_rates = {}
def collect(symbol):
    global params, funding_rates
    funding_rates[symbol] = []
    params['symbol'] = symbol

    newEndTime = str(round(time.time()*1000))
    while True:
        params['endTime'] = newEndTime
        r = requests.get('https://fapi.binance.com/fapi/v1/fundingRate', params=params).json()
        # , {'symbol': 'ZRXUSDT', 'fundingTime': 1680969600018, 'fundingRate': '-0.00025049'}]
        # request weight is 1

        for datapoint in r:
            funding_rates[symbol].append(datapoint)

        print(f'successfully requested data up to {newEndTime} for {symbol}')
        if len(r) == 1000:
            newEndTime = str(r[0]['fundingTime'])
        else:
            print(f'end of data on {symbol}')
            break

r = requests.get('https://fapi.binance.com/fapi/v1/exchangeInfo').json()
symbols = []
for symbol in r['symbols']:
    if (symbol['contractType'] == 'PERPETUAL' and symbol['quoteAsset'] == 'USDT'):
        symbols.append(symbol['symbol'])

for symbol in symbols:
    try:
        collect(symbol)
        print(f'----Collected for {symbol}')
    except:
        print(f'----Failed to collect data for {symbol}')


with open('funding_rates.json', 'w') as f:
    json.dump(funding_rates, f)