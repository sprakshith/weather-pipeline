import os
from confluent_kafka import Consumer


config = {
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'WEATHER_GROUP',
    'auto.offset.reset': 'earliest'
}

consumer = Consumer(config)
consumer.subscribe(['LATEST_WEATHER_TOPIC'])

while True:
    msg = consumer.poll(1.0)
    if msg is None:
        continue
    if msg.error():
        print("Consumer error: {}".format(msg.error()))
        continue

    msg_str = str(msg.value().decode('utf-8'))
    print('Consumed Data...!')

    dir_path = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(dir_path, "LatestWeatherData/latest_weather_data.txt")

    with open(file_path, 'w') as file:
        file.write(msg_str)
