from asyncio.windows_events import NULL
import json
from pprint import pprint

with open('Backtesting/Bybit_funding_rates.json', 'r') as f:
    bybit = json.load(f)
with open('Backtesting/Binance_funding_rates.json', 'r') as f:
    binance = json.load(f)

comparison = {}
for ticker in bybit:
    if len(bybit[ticker]) > 0:
        bt = bybit[ticker]  # bt and bn for bybit and binance
        symbol = ticker[:-4]
        bn = binance[f'{symbol+"USDT"}']

        comparison[symbol] = []
        for block in bn:
            bybit_rate = next((data for data in bt if data['fundingRateTimestamp'] == block['fundingTime']), None)
            #ERROR: of course I cannot do that; will have to sort them correctly individually, and then just compare from the last datapoint
            if bybit_rate:
                data = {'timestamp': block['fundingTime'],
                        'Binance_fundingRate': float(block['fundingRate']),
                        'Bybit_fundingRate': float(bybit_rate)}
                data['difference'] = data['Binance_fundingRate'] - data['Bybit_fundingRate']
                # {'symbol': 'ZRXUSDT', 'fundingTime': 1680969600018, 'fundingRate': '-0.00025049'} for binance
                # {'symbol': 'ETHPERP', 'fundingRate': '-0.00049011', 'fundingRateTimestamp': '1678579200000'} for bybit

                comparison[symbol].append(data)
        print(f'{symbol} appended to comparison dictionary')

    with open('rates_comparison.json', 'w') as f:
        json.dump(comparison, f)