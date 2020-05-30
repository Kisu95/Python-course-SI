import requests
from datetime import datetime
from math import sqrt
import matplotlib.pyplot as plt
import numpy as np


daily_volumes, daily_differences, predict = [], [], []


def date_to_timestamp(date_string):
    date = datetime.strptime(date_string, "%d/%m/%Y")
    timestamp = datetime.timestamp(date)
    return int(timestamp)


def get_data(date, crypto):
    url = "https://www.bitstamp.net/api/v2/ohlc/{crypto}usd?step=86400&limit=1000&start={timer}".format(
        timer=str(date), crypto=crypto)
    days = (datetime.now().timestamp() -
            float(date)) / 86400
    return requests.get(url).json()['data']['ohlc'], int(days)


def get_volumes(ticker):
    for day in ticker:
        print(day)
        daily_volumes.append(float(day['volume']))


def get_volumes_diff(daily_volumes):
    for daily_volume in daily_volumes[1:]:
        daily_differences.append(
            (daily_volume - daily_volumes[daily_volumes.index(daily_volume)-1])/daily_volume)


def changes_ava(data, days=30):
    new_data = data.copy()
    new_values = []
    for i in range(days):
        avg = np.sum(new_data) / len(new_data)
        avg = avg * (1+daily_differences[i])
        new_data.pop(0)
        new_data.append(avg)
        new_values.append(avg)
    return new_values


def simulation(simulation, days):
    simulated_data = []
    for i in range(simulation):
        data = changes_ava(daily_volumes, days)
        simulated_data.append(data)
    simulated_result = []
    for i in range(len(simulated_data[0])):
        index_values = []
        for j in range(len(simulated_data)):
            index = simulated_data[j][i]
            index_values.append(index)
        avarage = np.sum(index_values) / len(index_values)
        simulated_result.append(avarage)
    return simulated_result


date = date_to_timestamp("20/05/2020")
ticker, days = get_data(date, 'btc')
get_volumes(ticker)
get_volumes_diff(daily_volumes)
print()
predicted = changes_ava(daily_volumes, days)
simulated = simulation(100, days)

fig = plt.figure()
plt.axis([0, 20, 0, 20000])
plt.plot(daily_volumes, '-r')
plt.plot(range(11, 21), predicted, '-b')
plt.show()
