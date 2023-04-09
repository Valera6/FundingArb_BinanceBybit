import websocket, json, time

#========================================================== 
def on_message(vws, message):
    with open('rates.json', 'r') as f:
        data = json.load(f)
        rates = data['list']
        # rates now contains {'symbol': (binance_p, bybit_p), ...}
    message = json.loads(message)
    for ticker in message:
        rates[ticker['s']] = (ticker['r'], rates[ticker['s']][1]) # so bybit_p is unchanged
    data['list'] = rates
    data['lastUpdateBinance'] = time.time()*1000
    with open('rates.json', 'w') as f:
        json.dump(data, f, indent=4, separators=(",", ": "))

#---------------------------------------------------------- 
def on_error(ws, error):
    print(error)
def on_close(close_msg):
    print(close_msg)
def streamKline():
    socket = f'wss://fstream.binance.com/ws/!markPrice@arr'
    ws = websocket.WebSocketApp(socket,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.run_forever()

#========================================================== 
def main():
    print('binance started')

    streamKline()


if __name__ == "__main__":
   main()
