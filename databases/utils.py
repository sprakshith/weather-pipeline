import os
import datetime
import pandas as pd
from pymongo import ASCENDING, DESCENDING
from databases.mongodb_connector import get_database


def get_latest_weather_data():
    database = get_database()
    collection = database['london_weather']
    latest_data = collection.find().sort('dt', DESCENDING).limit(1)[0]
    latest_data.pop('_id')

    return latest_data


def save_data_dataframe():
    database = get_database()
    collection = database['london_weather']
    all_data = collection.find({}).sort('dt', ASCENDING)

    dt = list()

    temperature = list()
    feels_like = list()
    temp_min = list()
    temp_max = list()

    pressure = list()
    humidity = list()
    visibility = list()

    wind_speed = list()
    wind_direction = list()
    clouds = list()

    for data in all_data:
        dt.append(data.get('dt'))

        temperature.append(data.get('main').get('temp'))
        feels_like.append(data.get('main').get('feels_like'))
        temp_min.append(data.get('main').get('temp_min'))
        temp_max.append(data.get('main').get('temp_max'))

        pressure.append(data.get('main').get('pressure'))
        humidity.append(data.get('main').get('humidity'))
        visibility.append(data.get('visibility'))

        wind_speed.append(data.get('wind').get('speed'))
        wind_direction.append(data.get('wind').get('deg'))
        clouds.append(data.get('clouds').get('all'))

    weather_dict = {
        'datetime': dt,
        'temperature': temperature,
        'feels_like': feels_like,
        'temp_min': temp_min,
        'temp_max': temp_max,
        'pressure': pressure,
        'humidity': humidity,
        'visibility': visibility,
        'wind_speed': wind_speed,
        'wind_direction': wind_direction,
        'clouds': clouds
    }

    df = pd.DataFrame(weather_dict)

    dir_path = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(dir_path, "../LatestWeatherData/HistoricalWeatherData.csv")
    df.to_csv(file_path, index=False)

    return df[['datetime', 'temperature', 'humidity', 'wind_speed', 'clouds']]


if __name__ == '__main__':
    print(get_latest_weather_data())
