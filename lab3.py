"""
1. Znaleźć w internecie API ze źródłem danych o rynkach finansowych, przykłady:
https://bittrex.github.io/api/v1-1
https://bitbay.net/en/public-api
https://www.tradingview.com/rest-api-spec/#section/Authentication

Stworzyć prostą funkcję, która łączy się z danym API, pobiera listę ofert kupna oraz listę ofert sprzedaży i printuje do konsoli. (5pkt)

2. Znaleźć API z drugiego źródła - giełdy / instytucji finansowej, wybrać jeden zasób finansowy, a właściwie ich parę (bitcoin-usd / ropa-usd / złoto-usd / eur - usd)
porównać gdzie bardziej opłaca się kupić (oferty sprzedaży są niższe), a gdzie sprzedać (oferty kupna są wyższe) (5pkt)
"""

import requests


def get_bitbay_orderbook_data():
    response_request = requests.get(
        'https://bitbay.net/API/Public/BTCPLN/orderbook.json')
    return response_request.json()


def get_bitbay_ticker_data():
    response_request = requests.get(
        'https://bitbay.net/API/Public/BTCPLN/ticker.json')
    return response_request.json()


def get_blockchain_ticker_data():
    response_request = requests.get(
        'https://blockchain.info/ticker')
    return response_request.json()


orderbook_data = get_bitbay_orderbook_data()
sell_offers = orderbook_data['bids']
buy_offers = orderbook_data['asks']

print(f"Bids list: ")
for offer in enumerate(sell_offers):
    print(f"{offer[0]}. {offer[1][0]}zł")

print(f"First 10 asks: ")
for offer in enumerate(buy_offers[:10]):
    print(f"{offer[0]}. {offer[1][0]}zł")

bitbay_ticker = get_bitbay_ticker_data()
blockchain_ticker = get_blockchain_ticker_data()

bitbay_sell = bitbay_ticker['bid']
bitbay_buy = bitbay_ticker['ask']

blockchain_sell = blockchain_ticker['PLN']['sell']
blockchain_buy = blockchain_ticker['PLN']['buy']

print(
    f"You can buy bitcoin cheaper on bitbay.net {bitbay_sell}") if bitbay_sell < blockchain_sell else print(
    f"You can buy bitcoin cheaper on blockchain.info {blockchain_sell}")

print(
    f"Better profit on selling bitcoin on bitbay.net {bitbay_buy}") if bitbay_buy > blockchain_buy else print(
    f"Better profit on selling bitcoin on blockchain.info {blockchain_buy}")
