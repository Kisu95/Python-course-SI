import requests
import time


def get_price():
    bitbay = requests.get('https://bitbay.net/API/Public/BTC/USD/ticker.json')
    cex = requests.get('https://cex.io/api/ticker/BTC/USD')
    bitstamp = requests.get('https://www.bitstamp.net/api/ticker')
    blockchain = requests.get("https://blockchain.info/ticker")
    return bitbay.json(), cex.json(), bitstamp.json(), blockchain.json()


def wallet_update(wallet, buy, sell):
    wallet[1] = wallet[1] + 0.1
    wallet[0] = wallet[0] - buy*0.1
    wallet[1] = wallet[1] - 0.1
    wallet[0] = wallet[0] + sell*0.1
    return wallet


def arbitration(wallet):
    bitbay_ticker, cex_ticker, bitstamp_ticker, blockchain_ticker = get_price()

    bitbay_sell_offers = bitbay_ticker['bid']
    bitbay_buy_offers = bitbay_ticker['ask']

    cex_sell_offers = cex_ticker['bid']
    cex_buy_offers = cex_ticker['ask']

    bitstamp_sell_offers = float(bitstamp_ticker['bid'])
    bitstamp_buy_offers = float(bitstamp_ticker['ask'])

    blockchain_sell_offers = blockchain_ticker["USD"]["sell"]
    blockchain_buy_offers = blockchain_ticker["USD"]["buy"]

    buy_offers = {'bitbay': bitbay_buy_offers*1.003,
                  'cex': cex_buy_offers*1.005, 'bitstamp': bitstamp_buy_offers*1.0024, 'bitstamp': blockchain_buy_offers*1.0025}
    sell_offers = {'bitbay': bitbay_sell_offers-bitbay_sell_offers*0.003,
                   'cex': cex_sell_offers-cex_sell_offers*0.005, 'bitstamp': bitstamp_sell_offers-bitstamp_sell_offers*0.0024, 'blockchain': blockchain_sell_offers-blockchain_sell_offers*0.0025}

    lowest_price_to_buy = min(buy_offers.values())
    lowest_price_to_buy_name = min(buy_offers, key=buy_offers.get)

    highiest_price_to_sell = max(sell_offers.values())
    highiest_price_to_sell_name = max(sell_offers, key=sell_offers.get)

    if lowest_price_to_buy < highiest_price_to_sell:
        print(f"On the {lowest_price_to_buy_name} you can buy 0,1 BTC for USD at the exchange rate of {lowest_price_to_buy} and sell on the {highiest_price_to_sell_name} at the exchange rate of {highiest_price_to_sell}, gaining {(highiest_price_to_sell-lowest_price_to_buy)*0.1}USD.")
        print(
            f"Wallet update: {wallet_update(wallet, lowest_price_to_buy, highiest_price_to_sell)}")


wallet = [1000, 0.5]
new_wallet = wallet[:]


while(True):
    arbitration(new_wallet)
    if (new_wallet[0]-wallet[0]) > 0:
        print(f"You earned on transactions: {new_wallet[0]-wallet[0]} USD")
    time.sleep(10)
