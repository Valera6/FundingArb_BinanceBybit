import requests, json, time
import pandas as pd
from pprint import pprint

params = {
    "category": 'linear',
    "symbol": "BTCUSDT",
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
        r = requests.get('https://api.bybit.com/v5/market/funding/history', params=params).json()
        r = r['result']['list']
        # {'symbol': 'ZRXUSDT', 'fundingTime': 1680969600018, 'fundingRate': '-0.00025049'} for binance
        # {'symbol': 'ETHPERP', 'fundingRate': '-0.00049011', 'fundingRateTimestamp': '1678579200000'} for bybit
        # request weight is 1

        for datapoint in r:
            funding_rates[symbol].append(datapoint)

        print(f'successfully requested data up to {newEndTime} for {symbol}')
        if len(r) == 200:
            newEndTime = str(r[-1]['fundingRateTimestamp'])
        else:
            print(f'end of data on {symbol}')
            break
        time.sleep(1)

r = requests.get('https://fapi.binance.com/fapi/v1/exchangeInfo').json()
symbols = []
for symbol in r['symbols']:
    if (symbol['contractType'] == 'PERPETUAL' and symbol['quoteAsset'] == 'USDT'):
        symbols.append(symbol['symbol'])

for symbol in symbols:
    #symbol = symbol[:-4]+'PERP' it might be so that I don't need to do that at all
    try:
        collect(symbol)
        print(f'----Collected for {symbol}')
    except:
        print(f'----Failed to collect data for {symbol}')


with open('Bybit_funding_rates.json', 'w') as f:
    json.dump(funding_rates, f)