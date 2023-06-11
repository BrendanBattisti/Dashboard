from typing import Tuple, Any
import json
import datetime
from env import WEATHER_API_KEY as API_KEY
import requests

ICON_MAP = {"Clouds": "cloud", "Rain": "rainy", "Clear": "sunny"}


def get_coordinates(city, state) -> tuple[Any, Any]:
    print("Getting coordinates")
    response = requests.get(f"http://api.openweathermap.org/geo/1.0/direct?q={city}, {state}&limit={5}&appid={API_KEY}")
    data = json.loads(response.content)[0]
    return (data['lat'], data['lon'])


def fetch_weather_data(city, state):
    print("Getting weather data")
    lat, lon = get_coordinates(city, state)
    response = requests.get(
        f"http://api.openweathermap.org/data/2.5/forecast?units=imperial&lat={lat}&lon={lon}&appid={API_KEY}")
    data = json.loads(response.content)
    return data


def get_weather_datetime(weather_data):
    """
    Gets the datetime stamps from a weather data file
    """
    return datetime.datetime.fromtimestamp(weather_data[0]['chunks'][0]['dt'])


def load_weather_data():
    """
    Loads weather data from the server's storage
    """
    try:
        with open("weather_data.json") as weather_data_file:
            return json.load(weather_data_file)

    except FileNotFoundError:
        return refresh_weather_data()


def save_weather_data(weather_data) -> None:
    """
    Saves weather data in the server's storage
    """

    with open("weather_data.json", 'w') as weather_data_file:
        json.dump(weather_data, weather_data_file, indent=2)


def format_weather_data(raw_weather_data):
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

        new_chunk = {'dt': chunk['dt'], 'temp': chunk['main']['temp'], 'weather': ICON_MAP[chunk['weather'][0]['main']]}
        new_weather_data[day_index]['chunks'].append(new_chunk)

    # Aggregating the three hour chunks
    for day in new_weather_data:
        dt = datetime.datetime.fromtimestamp(day['chunks'][0]['dt'])
        day['weekday'] = dt.weekday()
        day['day'] = dt.day
        day['month'] = dt.month
        day['high'] = max([x['temp'] for x in day['chunks']])
        day['low'] = min([x['temp'] for x in day['chunks']])
        weather_types = [x['weather'] for x in day['chunks']]
        day['weather'] = max(set(weather_types), key=weather_types.count)

    return new_weather_data


def refresh_weather_data():
    """
    Refreshes the server's stored weather data
    """
    print("Fetching recent weather data")
    raw_weather_data = fetch_weather_data("Rochester", "New York")
    weather_data = format_weather_data(raw_weather_data)
    save_weather_data(weather_data)
    return weather_data


def get_weather_data():
    """
    Gets weather data and checks if new data needs to be fetched
    """

    weather_data = load_weather_data()

    time_diff = datetime.datetime.now() - get_weather_datetime(weather_data)
    # Checks if the weather data needs to be updated
    if time_diff > datetime.timedelta(days=1):
        weather_data = refresh_weather_data()

    return weather_data
