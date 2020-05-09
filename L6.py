import requests
import datetime
import pyodbc
import time


def get_price(currency):
    currency_ticker = requests.get(
        f'https://www.bitstamp.net/api/v2/ticker/{currency}usd/')
    return currency_ticker.json()


def print_current_data():
    conn = pyodbc.connect('Trusted_Connection=yes', driver='{ODBC Driver 17 for SQL Server}',
                          server='localhost', database='crypto')
    cursor = conn.cursor()
    cursor.execute('Select * from crypto')

    for row in cursor:
        currences[row[0]] = row[1:]

    for item in currences:
        print(currences[item])


def update_resource():
    currency = input("Enter currency. Type: BTC, EUR, ITC, ETH or BCH: ")
    while True:
        if currency not in supported_currencies:
            currency = input(
                "Unsupported currency. Re-enter. Type: BTC, EUR, ITC, ETH or BCH: ")
        else:
            break

    value = float(input(f"Enter value of {currency}: "))
    connection = pyodbc.connect('Trusted_Connection=yes', driver='{ODBC Driver 17 for SQL Server}',
                                server='localhost', database='crypto')

    cursor = connection.cursor()
    sql_update_query = """UPDATE crypto SET Amount = ? WHERE Currency = ?"""
    inputData = (value, currency)
    cursor.execute(sql_update_query, inputData)
    connection.commit()


def update_percent_change(currency, value):
    connection = pyodbc.connect('Trusted_Connection=yes', driver='{ODBC Driver 17 for SQL Server}',
                                server='localhost', database='crypto')

    cursor = connection.cursor()
    sql_update_query = """UPDATE crypto SET Last24_percentage_change = ? WHERE Currency = ?"""
    inputData = (value, currency)
    cursor.execute(sql_update_query, inputData)
    connection.commit()


def update_value_change(currency, value):
    connection = pyodbc.connect('Trusted_Connection=yes', driver='{ODBC Driver 17 for SQL Server}',
                                server='localhost', database='crypto')

    cursor = connection.cursor()
    sql_update_query = """UPDATE crypto SET Last24_value_change = ? WHERE Currency = ?"""
    inputData = (value, currency)
    cursor.execute(sql_update_query, inputData)
    connection.commit()


def update_time(currency, time):
    connection = pyodbc.connect('Trusted_Connection=yes', driver='{ODBC Driver 17 for SQL Server}',
                                server='localhost', database='crypto')

    cursor = connection.cursor()
    sql_update_query = """UPDATE crypto SET Update_time = ? WHERE Currency = ?"""
    inputData = (time, currency)
    cursor.execute(sql_update_query, inputData)
    connection.commit()


def purchase_price_change(currency, last_price):
    conn = pyodbc.connect('Trusted_Connection=yes', driver='{ODBC Driver 17 for SQL Server}',
                          server='localhost', database='crypto')
    cursor = conn.cursor()
    sql_update_query = """Select PurchasePrice from crypto where Currency = ?"""
    inputData = (currency)
    cursor.execute(sql_update_query, inputData)
    for row in cursor:
        purchase_price_percentage_change = last_price/float(row[0]) - 1
        purchase_price_value_change = last_price - float(row[0])

    return purchase_price_percentage_change, purchase_price_value_change


supported_currencies = ['btc', 'eur', 'ltc', 'eth', 'bch']
currences = {}

print("Your current resources with 24h update:")
print_current_data()

while True:
    step = input(
        "Type 'update_resource' to update your resources or something else to skip this step: ")
    if step == 'update_resource':
        update_resource()
    else:
        break

for currency in supported_currencies:
    ticker = get_price(currency)
    percentage_change = float(ticker['last'])/float(ticker['vwap']) - 1
    value_change = float(ticker['last']) - float(ticker['vwap'])
    purchase_price_percentage_change, purchase_price_value_change = purchase_price_change(
        currency, float(ticker['last']))
    date = datetime.datetime.fromtimestamp(
        int(ticker["timestamp"])).isoformat()
    update_percent_change(currency, percentage_change)
    update_value_change(currency, value_change)
    update_time(currency, date)
    print(f"percentage change for {currency} : {percentage_change:.4f}")
    print(f"value change for {currency}: {value_change:.2f}")
    print(
        f"percentage change for {currency} from buy price : {purchase_price_percentage_change:.4f}")
    print(
        f"value change for {currency} from buy price: {purchase_price_value_change:.2f}")
