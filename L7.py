# Stworzyć funkcję, która dla różnych zakresów czasu notowań z przeszłości wygeneruje symulację
# ziennego wolumenu dla wybranego waloru(w przyszłości).
# Funkcja przyjmuje argumenty wejściowe - walor(1 z 3 predefiniowanych przez Was) i datę "od".
# Data w dowolnie wybranym przez was formacie, może być to string "2016-01-01" może być to pełny timestamp.
# Symulacja ma bazować na danych od wprowadzonej daty do daty obecnej. Na podstawie tych danych historycznych tworzycie model, z którego generujecie dane dot. przyszłości.
# Proponuję bazować Wasz model na obserwacji zachowania z przeszłości(dziennego wolumenu, czyli obrotu danym walorem).
# Podpowiedź: policzyć prawdopodobieństwa wystąpienia zdarzeń(spadku/wzrostu wolumenu) oraz jego wielkości(o ile % spadnie/wzrośnie) i na tej podstawie generować dzienne wolumeny w przyszłości.

# Przeprowadzić pojedynczą oraz wielokrotną symulację, zapisać wyniki, policzyć wskaźniki grupy symulacji(takie jak średnia, mediana, odchylenia).
# Wygenerować wykres przedstawiający notowania historyczne oraz kontynuację notowań bazowaną na modelu(wybrany okres, proponuję taki sam na jaki patrzyliśmy wstecz)
# Na wykresie nanieść wynik pojedynczej symulacji oraz uśrednienia ze 100 symulacji.
# Uwaga - zostawcie sobie czas na przeprowadzenie symulacji, w zależności od sprzętu oraz jakości Waszego kodu symulacje mogą trochę trwać.
# (10pkt)

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
