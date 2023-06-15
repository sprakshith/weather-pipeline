$(document).ready(function () {
	var IP_ADDRESS = 'http://localhost'
	var BASE_URL = IP_ADDRESS + ':5050'

    $.ajax({
        url: BASE_URL + "/get_all_data",
        type: "GET",
        dataType: 'json',
        success: function(response) {
            generateHistoricalReport(response);
        }
    });

    const socket = io.connect(IP_ADDRESS + ':12345');

	socket.on('LATEST_WEATHER_REPORT', function(response) {
	    var latestWeatherData = JSON.parse(response);
	    destroyChart();
		generateCurrentWeatherReport(latestWeatherData.LATEST_WEATHER_DATA);
        generateSunRoutineReport(latestWeatherData.LATEST_WEATHER_DATA);
        generateBbcWeatherReport(latestWeatherData.BBC_WEATHER_REPORT);
	});
});

function generateCurrentWeatherReport(weatherData) {
	const weatherTitle = `${weatherData.name}`;
    const countryFlag = `https://flagsapi.com/${weatherData.sys.country}/shiny/64.png`;
    const weatherCondition = `${weatherData.weather[0].main}, ${weatherData.weather[0].description}`;
    const weatherIcon = `http://openweathermap.org/img/wn/${weatherData.weather[0].icon}.png`;
    const weatherTemperatures = [weatherData.main.temp_min-273.15, weatherData.main.feels_like-273.15,
                                 weatherData.main.temp-273.15, weatherData.main.temp_max-273.15];
    const weatherHumidity = weatherData.main.humidity;
    const weatherClouds = weatherData.clouds.all;
    const weatherVisibility = weatherData.visibility;

    $('#weather-title').text(weatherTitle);
    $('#country-flag').attr('src', countryFlag);
    $('#weather-condition').text(weatherCondition);
    $('#weather-icon').attr('src', weatherIcon);
    $('.visibility-value').text("Visibility: " + (weatherVisibility / 1000) + " KM");
    $('.wind-speed').text("Wind Speed: " + weatherData.wind.speed + " m/s")

    new Chart(document.getElementById('weather-chart'), {
        type: 'line',
        data: {
            labels: ['Min Temp', 'Feels Like', 'Temp', 'Max Temp'],
            datasets: [
                {
                    label: 'Temperature (°C)',
                    data: weatherTemperatures,
                    borderWidth: 4,
                    pointRadius: 2
                },
                {
                    label: 'Humidity (%)',
                    data: Array(4).fill(weatherHumidity),
                    type: 'line',
                    borderWidth: 4,
                    pointRadius: 0
                }
            ]
        },
        options: {
            responsive: true,
            scales: {
                y: { beginAtZero: true }
            }
        }
    });
}

function generateSunRoutineReport(weatherData) {
	var currentTime = Math.round(new Date()/1000) - 3600;
    var sunriseTime = weatherData.sys.sunrise - 3600;
    var sunsetTime = weatherData.sys.sunset - 3600;

    $('.sunrise').text("Sunrise at: " + convertEpochToTime(sunriseTime))
    $('.sunset').text("Sunset at: " + convertEpochToTime(sunsetTime))

    var totalDaylightDuration = sunsetTime - sunriseTime;
    var elapsedTimeSinceSunrise = currentTime - sunriseTime;
    var dayProgress = (elapsedTimeSinceSunrise / totalDaylightDuration) * 100;

    if(currentTime < sunriseTime) {
        dayProgress = 0;
    } else if(currentTime > sunsetTime) {
        dayProgress = 100;
    }

    var count = $('#count');
    $({ Counter: 0 }).animate({ Counter: dayProgress }, {
      duration: 2500 * (dayProgress/100),
      easing: 'linear',
      step: function () {
        count.text(Math.ceil(this.Counter)+ "%");
      }
    });

    var s = Snap('#sunr-suns');
    var progress = s.select('#progress');

    progress.attr({strokeDasharray: '0, 251.2'});
    Snap.animate(0,(dayProgress/100)*251.2, function( value ) {
        progress.attr({ 'stroke-dasharray':value+',251.2'});
    }, 2500 * (dayProgress/100));
}

function convertEpochToTime(epoch) {
    var date = new Date(epoch * 1000);
    var options = { hour12: true, hour: '2-digit', minute: '2-digit', second: '2-digit' };
    var timeStr = date.toLocaleTimeString('en-US', options);

    return timeStr;
}

function generateHistoricalReport(data) {
    generateChart(document.getElementById('tempChart').getContext('2d'), data.day, data.temperature, 'Temperature (°C)', '#f48037');
    generateChart(document.getElementById('humidityChart').getContext('2d'), data.day, data.humidity, 'Humidity (%)', '#0080FF');
    generateChart(document.getElementById('windChart').getContext('2d'), data.day, data.wind_speed, 'Wind Speed (m/s)', '#00FF00');
    generateChart(document.getElementById('cloudsChart').getContext('2d'), data.day, data.clouds, 'Clouds (%)', '#D3D3D3');
}

function generateChart(ctx, days, values, label, borderColor) {
	new Chart(ctx, {
        type: 'line',
        data: {
            labels: days,
            datasets: [{
                label: label,
                data: values,
                fill: false,
                borderColor: borderColor,
                tension: 0.3
            }]
        },
        options: {
            plugins: {
                title: {
                    display: true,
                    text: label
                },
                legend: {
                    display: false
                }
            }
        }
    });
}

function generateBbcWeatherReport(response) {
	$('.carousel-item h3').eq(0).html(response.today_title);
	$('.carousel-item h3').eq(1).html(response.tomorrow_title);
	$('.carousel-item h3').eq(2).html(response.outlook_title);

	$('.carousel-item p').eq(0).html(response.today_text);
	$('.carousel-item p').eq(1).html(response.tomorrow_text);
	$('.carousel-item p').eq(2).html(response.outlook_text);
}

function destroyChart() {
	var ctx = document.getElementById('weather-chart').getContext('2d');
	var chartInstance = Chart.getChart(ctx);

	if (chartInstance) {
	    chartInstance.destroy();
	}
}
