import os
import datetime
import pandas as pd
from pymongo import ASCENDING, DESCENDING
from database.mongodb_connector import get_database


def get_day_labels():
    days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    today = datetime.date.today()
    day = today.strftime("%A")
    day_index = days.index(day)
    day_labels = days[day_index + 1:] + days[:day_index + 1]
    day_labels = day_labels[-7:]
    day_labels[-1] = "Today"
    day_labels[-2] = "Yesterday"

    return day_labels


def get_latest_weather_data():
    database = get_database()
    collection = database['london_weather']
    latest_data = collection.find().sort('dt', DESCENDING).limit(1)[0]
    latest_data.pop('_id')

    return latest_data


def get_all_weather_data():
    df = save_data_dataframe()

    df['datetime'] = pd.to_datetime(df['datetime'], unit='s')
    df['day_number'] = df['datetime'].dt.dayofyear

    mean_df = df.groupby('day_number').mean().reset_index()
    mean_df.columns = ['day_number', 'datetime', 'mean_temperature', 'mean_humidity', 'mean_wind_speed', 'mean_clouds']
    mean_df = mean_df.sort_values('day_number')
    mean_df = mean_df.tail(7)
    mean_df.reset_index(drop=True, inplace=True)
    mean_df.drop(columns=['day_number', 'datetime'], inplace=True)
    mean_df['day_label'] = get_day_labels()

    mean_df['mean_temperature'] = mean_df['mean_temperature'].apply(lambda x: round(x-273.15, 2))
    mean_df['mean_humidity'] = mean_df['mean_humidity'].apply(lambda x: round(x, 2))
    mean_df['mean_wind_speed'] = mean_df['mean_wind_speed'].apply(lambda x: round(x, 2))
    mean_df['mean_clouds'] = mean_df['mean_clouds'].apply(lambda x: round(x, 2))

    response = {
        'day': list(mean_df.day_label),
        'temperature': list(mean_df.mean_temperature),
        'humidity': list(mean_df.mean_humidity),
        'wind_speed': list(mean_df.mean_wind_speed),
        'clouds': list(mean_df.mean_clouds)
    }

    return response


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
    print(get_all_weather_data())
