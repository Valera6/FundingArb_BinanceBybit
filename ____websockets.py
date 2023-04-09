import asyncio
import websockets

async def binance_ticker():
    uri = 'wss://fstream.binance.com/ws/!markPrice@arr'
    async with websockets.connect(uri) as websocket:
        while True:
            binance_rates = await websocket.recv()
            print(binance_rates)

async def bybit_ticker():
    uri = "wss://stream.bybit.com/realtime?symbol=BTCUSD"
    async with websockets.connect(uri) as websocket:
        while True:
            ticker = await websocket.recv()
            print(f"Bybit ticker: {ticker}")

async def main():
    await asyncio.gather(binance_ticker(), bybit_ticker())

if __name__=='__main__':
    asyncio.run(main())
