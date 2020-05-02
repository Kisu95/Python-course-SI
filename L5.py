import requests
from collections import defaultdict
import time


def get_price():
    btc = requests.get(
        'https://www.bitstamp.net/api/v2/ticker/btcusd/')
    bch = requests.get('https://www.bitstamp.net/api/v2/ticker/bchusd/')
    eth = requests.get('https://www.bitstamp.net/api/v2/ticker/ethusd/')
    ltc = requests.get('https://www.bitstamp.net/api/v2/ticker/ltcusd/')
    eur = requests.get('https://www.bitstamp.net/api/v2/ticker/eurusd/')
    return btc.json(), bch.json(), eth.json(), ltc.json(), eur.json()


def transaction(investment_amount):
    while True:
        btc_ticker, bch_ticker, eth_ticker, ltc_ticker, eur_ticker = get_price()

        price_differences = {
            'btc': float(btc_ticker['high'])/float(btc_ticker['low']) - 1,
            'bch': float(bch_ticker['high'])/float(bch_ticker['low']) - 1,
            'eth': float(eth_ticker['high'])/float(eth_ticker['low']) - 1,
            'ltc': float(ltc_ticker['high'])/float(ltc_ticker['low']) - 1,
            'eur': float(eur_ticker['high'])/float(eur_ticker['low']) - 1,
        }

        volumes = {
            'btc': float(btc_ticker['volume']),
            'bch': float(bch_ticker['volume']),
            'eth': float(eth_ticker['volume']),
            'ltc': float(ltc_ticker['volume']),
            'xrp': float(eur_ticker['volume']),
        }

        lowest_price = {
            'btc': float(btc_ticker['low']),
            'bch': float(bch_ticker['low']),
            'eth': float(eth_ticker['low']),
            'ltc': float(ltc_ticker['low']),
            'xrp': float(eur_ticker['low']),
        }

        sorted_crypto = sorted(price_differences,
                               key=price_differences.get, reverse=True)

        for cryptocurrency in sorted_crypto:
            print(
                f'{cryptocurrency} {price_differences[cryptocurrency]*100:.2f}%')

        for cryptocurrency in sorted_crypto:
            if investment_amount > 0:
                if volumes[cryptocurrency]*lowest_price[cryptocurrency] < investment_amount:
                    investment_amount = investment_amount - \
                        volumes[cryptocurrency]*lowest_price[cryptocurrency]
                    print(
                        f"You can buy: {volumes[cryptocurrency]*lowest_price[cryptocurrency]:.2f} {cryptocurrency}")
                    print(
                        f"You have left: {investment_amount:.2f} USD")
                else:
                    print(
                        f"You can buy: {investment_amount/lowest_price[cryptocurrency]:.2f} {cryptocurrency}")
                    investment_amount = 0
                    print(
                        f"You have no funds left: {investment_amount:.2f} USD")

        time.sleep(300)


transaction(1000000)
