# Dynamic Weather Monitoring 
### An Application of Python, MongoDB and Kafka

---

<h3><u>1. Project Structure:</u></h3>

```
weather-pipeline
│   app.py
│   cronjob_app.py
│   kafka_consumer.py
│   kafka_producer.py
│   socket_app.py
│   README.md
│   requirements.txt
│
└───data_scraping
│   │   bbc_website.py
│   │
│
└───database
│   │   mongodb_connector.py
│   │   utils.py
│
└───project_credentials
│   │   api_credentials.py
│   │   db_credentials.py
│
└───weather_api
│   │   london_weather.py
│   │   
│
└───flask_template_app
│   │   flask_static.py
│   │
│   └───static
│   │   │
│   │   └───css
│   │   │   style.css   
│   │   │
│   │   └───img
│   │   │   favicon.ico
│   │   │
│   │   └───js
│   │   │   script.js   
│   │
│   └───templates
│   │   │   index.html
│   │   │
│   
└───LatestWeatherData
│   │   HistoricalWeatherData.csv
│   │   latest_weather_data.txt
│   │
```

<h3><u>2. Setup Procedure:</u></h3>

1. Navigate to the directory where you want to set up this project.
<br><br>
2. Open cmd/bash and run the below command:<br>
On Mac/Win: ``git clone https://github.com/sprakshith/weather-pipeline.git``
<br><br>
3. Now create a virtual enviroment. <br>
On Mac: ``python3 -m venv ./venv``<br>
Example: ``python3 -m venv ./venv``
<br><br>
On Win: ``python -m venv  "[Path to weather-pipeline Directory]\[NAME_OF_VIRTUAL_ENV]"``<br>
Example: ``python -m venv "D:\weather-pipeline\venv"``
<br><br>
4. To activate the venv run the below command. <br>
On Mac: ``source venv/bin/activate`` <br>
On Win: ``venv\Scripts\activate.bat``
<br><br>
5. To install all the requirements run the below command. Execute this command whenever there is a change in requirements.txt file.<br>
On Mac/Win: ``pip install -r requirements.txt``
6. Run Zookeeper and Kafka servers.
7. Run the following python files in order: ``app.py``, ``kafka_producer.py``, ``kafka_consumer.py``, ``socket_app.py`` and ``flask_static.py``.
8. Visit ``http://localhost:8080``

<hr>

<h3><u>3. Website Screenshot:</u></h3>

<img src="https://github.com/sprakshith/weather-pipeline/blob/master/WeatherPipeline.png" alt="Opps!"/>
