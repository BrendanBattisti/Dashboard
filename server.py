"""
SERVER
"""
import json
import subprocess

from flask import Flask, request
from Modules.storage import FileStorage

import env
from Modules.life360 import get_family_list
from Modules.lights import KasaInterface
from Modules.reddit import RedditInterface
from Modules.shopping import get_shopping_list, remove_from_list, add_to_list
from Modules.utils import FileLogger
from Modules.weather import get_weather_data
from env import PORT

app = Flask(__name__)


logger = FileLogger("log.txt")
storage = FileStorage("data.json", logger)
kasa = KasaInterface(storage, logger)
#reddit = RedditInterface()

def runListServer():
    subprocess.Popen(['node', r'listServer.js'])


@app.route('/api/weather')
def weather():
    return get_weather_data()


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
    pass
    #return top_threads()


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
