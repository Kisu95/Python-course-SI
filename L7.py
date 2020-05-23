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

import datetime
import requests
import math


daily_volumes, daily_differences, predict = [], [], []


def date_to_timestamp(date_string):
    date = datetime.datetime.strptime(date_string, "%m/%d/%Y")
    timestamp = datetime.datetime.timestamp(date)
    return timestamp


def get_data(date, crypto):
    url = "https://www.bitstamp.net/api/v2/ohlc/{crypto}usd?step=86400&limit=1000&start={timer}".format(
        timer=str(int(date_to_timestamp(date))), crypto=crypto)
    days = (datetime.datetime.now().timestamp() -
            float(date_to_timestamp(date))) / 86400
    return requests.get(url).json()['data']['ohlc'], int(days)


def get_volumes(ticker):
    for day in ticker:
        daily_volumes.append(float(day['volume']))


def get_volumes_diff(daily_volumes):
    for daily_volume in daily_volumes[1:]:
        daily_differences.append(abs(
            (daily_volume - daily_volumes[daily_volumes.index(daily_volume)-1])/daily_volume))


# def simulation(data, volumens):
#     avg, std = norm.fit(data)
#     print(avg, std)
#     predict = gauss(avg, std)
#     predict.append(predict * volumens[-1] + volumens[-1])
#     plt.plot(arange(0, len(volumens)), volumens, color='g')
#     plt.plot(arange(len(volumens), len(predict) +
#                     len(volumens)), predict, color='b')
#     plt.grid(True)
#     plt.xlabel("Days")
#     plt.ylabel("Volume")
#     plt.title("Prediction of volume")
#     plt.legend(['Historical data', 'Predicted data'])


# def pointer(predict):
#     med = median(predict)
#     avg, std = norm.fit(predict)
#     print('One simulation: ', predict[0])
#     print('Madian: ', med, '\nAvarange: ', avg, '\nStd: ', std)


# def calculate(date, crypto):
#     ticker, days = get_data(date, crypto)
#     get_volumes(ticker)
#     get_volumes_diff(daily_volumes)
#     for i in range(days):
#         simulation(daily_differences[i], daily_volumes[i])
#     pointer(predict)
#     plt.show()


# calculate("05/10/2020", 'btc')
