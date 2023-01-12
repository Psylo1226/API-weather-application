import datetime as dt
import requests
import sys
import pandas as pd
import schedule
import time
from cities import CITIES
from voivodeships import pomorskie, zachodniopomorskie, warminsko_mazurskie, kujawsko_pomorskie, lubuskie, \
    dolnoslaskie, wielkopolskie, lubelskie, podlaskie, podkarpackie, malopolskie, slaskie, swietokrzyskie, \
    opolskie, mazowieckie, lodzkie
from provinces import province

BASE_URL = 'https://api.openweathermap.org/data/2.5/weather?'
API_KEY = '2d48f1aa43f965c330e7cfd6dc6cc2d9'


def weather():
    sys.stdout = open('weather.txt', 'w', encoding='utf-8')
    print(
        'City,Longitude,Latitude,Temperature_cel,Temperature_fah,Feels_like_cel,Feels_like_fah,Wind_speed,Humidity,'
        'Pressure,Degree,Description,Sunrise_time,Sunset_time,Voivodeship,Province')

    def kelvin_to_celsius_fahrenheit(kelvin):
        celsius = kelvin - 273.15
        fahrenheit = (kelvin - 273.15) * 9 / 5 + 32
        return celsius, fahrenheit

    for i in CITIES:
        url = BASE_URL + 'appid=' + API_KEY + '&q=' + i
        response = requests.get(url).json()

        longitude = response['coord']['lon']
        latitude = response['coord']['lat']
        temp_kelvin = response['main']['temp']
        temp_celsius, temp_fahrenheit = kelvin_to_celsius_fahrenheit(temp_kelvin)
        feels_like_kelvin = response['main']['feels_like']
        feels_like_celsius, feels_like_fahrenheit = kelvin_to_celsius_fahrenheit(feels_like_kelvin)
        wind_speed = response['wind']['speed']
        humidity = response['main']['humidity']
        pressure = response['main']['pressure']
        degree = response['wind']['deg']
        description = response['weather'][0]['description']
        sunrise_time = dt.datetime.utcfromtimestamp(response['sys']['sunrise'] + response['timezone']).strftime(
            '%H:%M:%S')
        sunset_time = dt.datetime.utcfromtimestamp(response['sys']['sunset'] + response['timezone']).strftime(
            '%H:%M:%S')
        voivodeship = 'zachodniopomorskie' if i in zachodniopomorskie else 'pomorskie' if i in pomorskie \
        else 'warmińsko-mazurskie' if i in warminsko_mazurskie else 'kujawsko-pomorskie' if i in kujawsko_pomorskie \
        else 'lubuskie' if i in lubuskie else 'wielkopolskie' if i in wielkopolskie else 'zachodniopomorskie' \
        if i in zachodniopomorskie else 'lubelskie' if i in lubelskie else 'podlaskie' if i in podlaskie else \
        'mazowieckie' if i in mazowieckie else 'łódzkie' if i in lodzkie else 'śląskie' if i in slaskie else \
        'świętokrzyskie' if i in swietokrzyskie else 'małopolskie' if i in malopolskie else 'podkarpackie' \
        if i in podkarpackie else 'opolskie' if i in opolskie else 'dolnośląskie' if i in dolnoslaskie else \
        'śląskie' if i in slaskie else 'świętokrzyskie' if i in swietokrzyskie else 'małopolskie' if i in \
        malopolskie else 'podkarpackie' if i in podkarpackie else 'opolskie' if i in opolskie else \
        'dolnośląskie' if i in dolnoslaskie else 'error'

        provinces = [k for k, v in province.items() if (isinstance(v, list) and i in v) or v == i][0] if \
            [k for k, v in province.items() if (isinstance(v, list) and i in v) or v == i] else ''

        print(
            f" {i}, {longitude}, {latitude}, {temp_celsius:.2f}, {temp_fahrenheit:.2f}, {feels_like_celsius:.2f}, "
            f"{feels_like_fahrenheit:.2f}, {wind_speed}, {humidity}, {pressure}, {degree}, {description},"
            f"{sunrise_time}, {sunset_time},{voivodeship},{'powiat ' + str(provinces)}")

    sys.stdout.close()

    dataframe1 = pd.read_csv('weather.txt')

    dataframe1.to_csv('weather.csv', index=False, encoding='utf-8')
    return dataframe1


if __name__ == '__main__':
    weather()

