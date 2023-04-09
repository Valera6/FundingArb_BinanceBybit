Websocket streams for all tickers listed on Bybit and Binance perps
fetching funding rate from the response
dumping into according json files

in main
from evaluate import exit()
load openPositions.json, check if any of exit conditions is met on every turn.
when triggered, pass the ticker to the exit() function of execution module

from evaluate import entry(); check if the situation is good enough by itself, if so
ask rm module

if green, start enter() of execution module, knowing the (size, leverage, exit criterias)
Pull the books, start filling the side with less demand and balancing the other
shoulder immediately

dump into openPositions.json, control in websockets module

rebalancing module is always active in the background, sending pings to main, to control for
it being up.