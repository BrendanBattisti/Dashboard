"""
Weather Module for dashboard
"""

import datetime
import json
from typing import Any, Tuple

import requests

from Modules.storage import Storage
from Modules.utils import annotate, Loggable, Logger

ICON_MAP = {"Clouds": "cloud", "Rain": "rainy", "Clear": "sunny"}


class WeatherInterface(Loggable):

    def __init__(self, city: str, state: str, api_key: str, storage: Storage, logger: Logger):
        super().__init__(logger)
        self.storage = storage
        self.api_key = api_key
        self.city = city
        self.state = state

    def get_weather_data(self):
        """
        Gets weather data and checks if new data needs to be fetched
        """

        data = self.storage.get_weather()

        if data['refresh']:
            data['data'] = self.refresh_weather_data()

        return data['data']

    def get_coordinates(self) -> Tuple[Any, Any]:
        self.log("Getting coordinates")
        response = requests.get(
            f"http://api.openweathermap.org/geo/1.0/direct?q={self.city}, {self.state}&limit={5}&appid={self.api_key}")
        data = json.loads(response.content)[0]
        return data['lat'], data['lon']

    @annotate
    def fetch_weather_data(self):
        self.log("Getting weather data")
        lat, lon = self.get_coordinates()
        response = requests.get(
            f"http://api.openweathermap.org/data/2.5/forecast?units=imperial&lat={lat}&lon={lon}&appid={self.api_key}")
        data = json.loads(response.content)
        return data

    @annotate
    def get_weather_datetime(self, weather_data):
        """
        Gets the datetime stamps from a weather data file
        """
        return datetime.datetime.fromtimestamp(weather_data[0]['chunks'][0]['dt'])

    @annotate
    def format_weather_data(self, raw_weather_data):
        """
        Formats weather data into a format to be stored in and sent to the server
        """
        new_weather_data = [{'chunks': []}]
        start_date = None

        # Loops over the 3 hour chunks and
        # Seperates them by day
        for chunk in raw_weather_data['list']:

            if not start_date: start_date = datetime.datetime.fromtimestamp(chunk['dt'])

            day_index = (datetime.datetime.fromtimestamp(chunk['dt']) - start_date).days

            if len(new_weather_data) < day_index + 1:
                new_weather_data.append({'chunks': []})

            new_chunk = {'dt': chunk['dt'], 'temp': chunk['main']['temp'],
                         'weather': ICON_MAP[chunk['weather'][0]['main']]}
            new_weather_data[day_index]['chunks'].append(new_chunk)

        # Aggregating the three hour chunks
        for index, day in enumerate(new_weather_data):
            dt = datetime.datetime.fromtimestamp(day['chunks'][0]['dt'])
            day['weekday'] = dt.weekday()
            day['day'] = dt.day
            day['month'] = dt.month
            day['index'] = index
            day['high'] = max([x['temp'] for x in day['chunks']])
            day['low'] = min([x['temp'] for x in day['chunks']])
            weather_types = [x['weather'] for x in day['chunks']]
            day['weather'] = max(set(weather_types), key=weather_types.count)

        return new_weather_data

    @annotate
    def refresh_weather_data(self):
        """
        Refreshes the server's stored weather data
        """
        self.log("Fetching recent weather data")
        raw_weather_data = self.fetch_weather_data()
        weather_data = self.format_weather_data(raw_weather_data)
        self.storage.save_weather(weather_data)
        return weather_data
