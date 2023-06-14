import os
import time
import eventlet
from flask import Flask
from flask_socketio import SocketIO

eventlet.monkey_patch()

app = Flask(__name__)
socketio = SocketIO(app, async_mode='eventlet', cors_allowed_origins="*")


def background_thread():
    while True:
        dir_path = os.path.dirname(os.path.realpath(__file__))
        file_path = os.path.join(dir_path, "LatestWeatherData/latest_weather_data.txt")

        with open(file_path, 'r') as file:
            latest_message = file.read()
            socketio.emit('LATEST_WEATHER_REPORT', latest_message)
            print("Emitted Data...!")

        time.sleep(120)


@socketio.on('connect')
def test_connect():
    print('Client connected')
    socketio.start_background_task(background_thread)


@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=12345)
