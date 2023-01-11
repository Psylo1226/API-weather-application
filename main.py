import mongo
import get_weather_info
import get_pollution_info
import app


def service_func():
    print('Service is running...')


if __name__ == '__main__':
    service_func()
    get_weather_info.weather()
    get_pollution_info.air_pollution()
    mongo.MongoDB(dBName='Inzynierka', collectionName='Weather').InsertData(path="weather.csv")
    mongo.MongoDB(dBName='Inzynierka', collectionName='Air pollution').InsertData(path="air_pollution.csv")
    app.main()