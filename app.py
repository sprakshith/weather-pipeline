from flask_cors import CORS
from flask import Flask, Response
from databases.utils import get_all_weather_data


app = Flask(__name__)
CORS(app)


@app.route('/get_all_data', methods=['GET'])
def get_all_data():
    return get_all_weather_data()


@app.route('/get_historical_data')
def provide_data():
    historical_weather = open('LatestWeatherData/HistoricalWeatherData.csv', 'r')
    return Response(
        historical_weather,
        mimetype='text/csv'
    )


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050)
