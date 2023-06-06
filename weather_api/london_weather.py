import requests
from databases.mongodb_connector import get_database
from project_credentials.api_crendentials import *


def fetch_current_weather_data():
    try:
        response = requests.get(f'{ENDPOINT}?lat={LAT}&lon={LON}&appid={APPID}').json()
        return response
    except AttributeError as e:
        print(e)
    except Exception as e:
        print(e)

    return dict()


def save_current_weather_data():
    try:
        database = get_database()
        london = database.get_collection("london_weather")
        london.insert_one(fetch_current_weather_data())
    except Exception as e:
        print(e)


if __name__ == '__main__':
    save_current_weather_data()
