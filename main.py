import schedule
import time
import get_weather_info
import get_pollution_info
import mongo
import app


def weather_pollution_func():
    get_weather_info.weather()
    get_pollution_info.air_pollution()


def service_func():
    print('Service is running...')
    weather_pollution_func()
    mongo.MongoDB(dBName='Inzynierka', collectionName='Weather').InsertData(path="weather.csv")
    mongo.MongoDB(dBName='Inzynierka', collectionName='Air pollution').InsertData(path="air_pollution.csv")
    app.main()


if __name__ == '__main__':
    schedule.every(1).hour.do(weather_pollution_func)
    schedule.every(1).hour.do(service_func)
    while True:
        schedule.run_pending()
        time.sleep(1)
