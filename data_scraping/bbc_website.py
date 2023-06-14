import requests
from bs4 import BeautifulSoup


def get_bbc_weather_report():
    url = "https://www.bbc.com/weather/2643743"
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")

        report_dict = {
            'today_title': soup.select_one("#wr-o-tabset__panel--today .wr-c-text-forecast__summary-title").text,
            'today_text': soup.select_one("#wr-o-tabset__panel--today .wr-c-text-forecast__summary-text").text,
            'tomorrow_title': soup.select_one("#wr-o-tabset__panel--tomorrow .wr-c-text-forecast__summary-title").text,
            'tomorrow_text': soup.select_one("#wr-o-tabset__panel--tomorrow .wr-c-text-forecast__summary-text").text,
            'outlook_title': soup.select_one("#wr-o-tabset__panel--outlook .wr-c-text-forecast__summary-title").text,
            'outlook_text': soup.select_one("#wr-o-tabset__panel--outlook .wr-c-text-forecast__summary-text").text
        }

        return report_dict
    else:
        return f"Error: {response.status_code}"
