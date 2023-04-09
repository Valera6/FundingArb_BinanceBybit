import websocket, json, requests, time

#TODO: only load the symbols listed on both exchanges
#========================================================== 
def on_message(vws, message):
    global ratesBybit
    message = json.loads(message)

    try:
        with open('rates.json', 'r') as f:
            data = json.load(f)
            rates = data['list']
        rate = message['data']['fundingRate']
        symbol = message['data']['symbol']
        rates[symbol] = (rates[symbol][0], rate) # to pass on the binance rate, sitting in the [0] of the tupple
        data['list'] = rates
        data['lastUpdateBybit'] = time.time()*1000
        with open('rates.json', 'w') as f:
            json.dump(data, f, indent=4, separators=(",", ": "))
    except:
        pass

def construct_args():
    global args

    r = requests.get('https://api.bybit.com/v5/market/tickers', params={'category': 'linear'}).json()
    for chunk in r['result']['list']:
        symbol = chunk['symbol']
        if symbol[-4:] == 'USDT':
            args.append(f"tickers.{symbol}")

#---------------------------------------------------------- 
def on_error(ws, error):
    print(error)
def on_close(close_msg):
    print(close_msg)
def on_open(ws):
    subscribe_message = {
        "op": "subscribe",
        "args": args
    }
    ws.send(json.dumps(subscribe_message))
def streamKline():
    ws = websocket.WebSocketApp("wss://stream.bybit.com/v5/public/linear",
                              on_message = on_message,
                              on_error = on_error,
                              on_close = on_close)
    ws.on_open = on_open
    ws.run_forever(ping_interval=1800)
    #TODO: send pings every 30m

#==========================================================
args = []
ratesBybit = {}
def main():
    print('bybit started')
    construct_args()
    streamKline()

if __name__ == "__main__":
   main()


# can do it by requests to 'https://api.bybit.com/v5/market/tickers' > fundingRate