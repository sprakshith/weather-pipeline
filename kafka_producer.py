import time
import json
from confluent_kafka import Producer
from databases.utils import get_latest_weather_data
from data_scraping.bbc_website import get_bbc_weather_report


configuration = {'bootstrap.servers': 'localhost:9092'}
producer = Producer(**configuration)

while True:
    latest_weather_data = {
        "LATEST_WEATHER_DATA": get_latest_weather_data(),
        "BBC_WEATHER_REPORT": get_bbc_weather_report(),
    }

    latest_weather_data_json = json.dumps(latest_weather_data)
    producer.produce('LATEST_WEATHER_TOPIC', latest_weather_data_json)
    producer.flush()

    print("Produced Data...!")

    time.sleep(120)
