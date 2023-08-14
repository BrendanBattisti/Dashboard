"""
SERVER
"""
import json
import subprocess

from flask import Flask, request

from Modules.life360 import get_family_list
from Modules.lights import KasaInterface
from Modules.reddit import RedditInterface
from Modules.shopping import get_shopping_list, remove_from_list, add_to_list
from Modules.storage import FileStorage
from Modules.utils import load_config, PrintLogger
from Modules.weather import WeatherInterface
from env import PORT

app = Flask(__name__)

config = load_config("config.json")

logger = PrintLogger()
storage = FileStorage(config.storage_file, logger)
kasa = KasaInterface(storage, logger)
reddit_interface = RedditInterface({
    "username": config.reddit_user,
    "password": config.reddit_password,
    "secret": config.reddit_secret,
    "client_id": config.reddit_client_id,
    "user_agent": config.reddit_user_agent
}, storage, logger)

weather_interface = WeatherInterface("Rochester", "New York", config.weather_key, storage, logger)


def runListServer():
    subprocess.Popen(['node', r'listServer.js'])


@app.route('/api/weather')
def weather():
    return weather_interface.get_weather_data()


@app.route('/api/shopping', methods=['GET', 'POST'])
def shopping_list():
    if request.method == "GET":

        return get_shopping_list()

    elif request.method == "POST":

        return add_to_list(json.loads(request.data)['item'])


@app.route('/api/shopping/<item>', methods=['DELETE'])
def shopping_delete(item):
    return remove_from_list(item)


@app.route("/api/reddit")
def reddit():
    return reddit_interface.get_threads()


@app.route('/api/lights', methods=['GET', 'PUT'])
def lights():
    if request.method == "GET":
        return kasa.get_lights()

    elif request.method == "PUT":
        data = request.data
        if not data:
            return kasa.get_lights()
        data = json.loads(data)
        return kasa.update_device_state(data['name'], data['on'])


@app.route("/api/life360", methods=['GET'])
def life360():
    if request.method == "GET":
        return get_family_list()


if __name__ == "__main__":
    runListServer()
    app.run(port=PORT)
