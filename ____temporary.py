import json

rates = {
    'lastUpdateBinance': 0,
    'lastUpdateBybit': 0,
    'list':{}}

with open('rates.json', 'w') as f:
    json.dump(rates, f, indent=4, separators=(",", ": "))