import json
from pprint import pprint

with open('Backtesting/rates_comparison.json', 'r') as f:
    rates = json.load(f)

pprint(rates)