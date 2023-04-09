# transactions are not frictionless, so we are 
# rebalancing only when close to liquidation. I will have it
# be 4% by default, but should be adjusted based on liqudity and
# volatility in the past 5 days
# # or can trust binance and use /fapi/v1/adlQuantile endpoint, [0, 1, 2, 3, 4], if 4 - transfer

# now assuming all the money on the accounts are for this strategy only
import json

with open('openPositions', 'r') as f:
    open_positions = json.load(f)

#<clients initiation>
import binance 
client = binance.Client('BINANCE_API_KEY', 'BINANCE_API_SECRET')

from pybit import HTTP
session = HTTP('BYBIT_API_KEY', 'BYBIT_API_SECRET')
#</clients initiation>


def to_bybit(average):
    amount = average - bybit_balance
    address = 'BYBIT_ADRESS'

    # Transfer USDT from futures cross wallet to spot wallet
    result = client.futures_account_transfer(asset='USDT', amount=amount, type=2)
    print(result)
    # And now to Bybit
    result = client.withdraw(asset='USDT', address=address, amount=amount, network='TRX')
    print(result)

def to_binance(average):
    address = 'BINANCE_ADRESS'
    amount = average - binance_balance

    # I think it's alright if I have the cross-everything Bybit account, to withdraw immidiately
    result = session.request_withdrawal(coin='USDT', address=address, amount=amount)

    # Don't forget to transfer the money to the futures wallet within binance now:
    result = client.futures_account_transfer(asset='USDT', amount=amount, type=1)
    print(result)

    print(result)

while True:
    # /fapi/v1/forceOrders for binance
    # for symbol in open_positions:
    #       session.query_forced_orders(symbol=symbol) for bybit
    # if in proximity of a force order:
        # calculate total strategy balance, take steps to achieve even distribution
        # (done to minimize total transactions number when more when one position open)

    #TODO: have a forced strategy stop if we were close to liquidation twice in 30m


    binance_balance = client.futures_account_balance()
    bybit_balance = session.get_wallet_balance(coin='USDT')
    average = (binance_balance+bybit_balance)/2
    to_bybit(average) # or to_binance(average)