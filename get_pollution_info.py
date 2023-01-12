import requests
import sys
import schedule
import time
import pandas as pd

"""
load & loads
dump & dumps
"""

BASE_URL = 'http://api.waqi.info/feed/'
API_KEY = '92ef90d337038716de6ec4f388b025d6b41020c5'
CITIES = ['Nowa Ruda', 'Nowy Sącz', 'Przemyśl', 'Tychy', 'Zamość', 'Gorzów Wielkopolski', 'Jelenia Góra', 'Wrocław',
          'Wałbrzych',
          'Legnica', 'Lębork', 'Kędzierzyn-Koźle', 'Gdańsk', 'Katowice', 'Piła', 'Szczecinek', 'Tczew',
          'Wodzisław Śląski',
          'Konin', 'Dzierżoniów', 'Żyrardów', 'Zakopane', 'Kościerzyna', 'Suwałki', 'Legionowo', 'Trzebinia', 'Kłodzko',
          'Cieszyn', 'Ząbkowice Śląskie', 'Zabrze', 'Poznań', 'Bogatynia', 'Rzeszów', 'Częstochowa', 'Łomża',
          'Szczecin',
          'Słupsk', 'Piastów', 'Rybnik', 'Białystok', 'Zielona Góra', 'Jasło', 'Płock', 'Opole', 'Knurów', 'Zgierz',
          'Dębica',
          'Otwock', 'Nisko', 'Lublin', 'Jarosław', 'Kalisz', 'Warszawa', 'Mielec', 'Ustroń', 'Sopot', 'Toruń',
          'Sosnowiec', 'Koszalin',
          'Kielce', 'Żywiec', 'Dąbrowa Górnicza', 'Grudziądz', 'Siedlce', 'Kraków', 'Skawina', 'Żary', 'Pabianice',
          'Starogard Gdański',
          'Włocławek', 'Olkusz', 'Gdynia', 'Gliwice', 'Łódź', 'Tarnów', 'Świdnica', 'Piotrków Trybunalski', 'Malbork',
          'Bielsko-Biała',
          'Inowrocław', 'Bydgoszcz', 'Biała Podlaska', 'Radom', 'Piaseczno', 'Knurów', 'Suwałki', 'Police', 'Lębork',
          'Żary', 'Zielona Góra', ]


def air_pollution():
    sys.stdout = open('air_pollution.txt', 'w', encoding='utf-8')
    print('City,Longitude,Latitude,Url,Pm10,Pm25,O3,No2,So2,Co')

    for i in CITIES:
        url = BASE_URL + i + '/?token=' + API_KEY
        response = requests.get(url).json()

        longitude = response['data']['city']['geo'][0]
        latitude = response['data']['city']['geo'][1]
        url_address = response['data']['city']['url']
        # none = 'None'
        try:
            pm10 = response['data']['iaqi']['pm10']['v']
        except KeyError:
            pm10 = 0
        try:
            pm25 = response['data']['iaqi']['pm25']['v']
        except KeyError:
            pm25 = 0
        try:
            o3 = response['data']['iaqi']['o3']['v']
        except KeyError:
            o3 = 0
        try:
            no2 = response['data']['iaqi']['no2']['v']
        except KeyError:
            no2 = 0
        try:
            so2 = response['data']['iaqi']['so2']['v']
        except KeyError:
            so2 = 0
        try:
            co = response['data']['iaqi']['co']['v']
        except KeyError:
            co = 0

        print(f"{i},{longitude},{latitude},{url_address},{pm10},{pm25},{o3},{no2},{so2},{co}")

    sys.stdout.close()

    dataframe1 = pd.read_csv('air_pollution.txt')

    dataframe1.to_csv('air_pollution.csv', index=False, encoding='utf-8')
    return


if __name__ == '__main__':
    air_pollution()
