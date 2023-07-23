"""
SERVER
"""
import json

from flask import Flask, request
import subprocess

from Modules.life360 import get_family_list
from Modules.lights import get_lights, send_update_lights, update_device_state
from Modules.shopping import get_shopping_list, remove_from_list
from Modules.weather import get_weather_data
from Modules.reddit import top_threads
from env import PORT

app = Flask(__name__)


def runListServer():
    subprocess.Popen(['node', r'listServer.js'])


@app.route('/api/weather')
def weather():
    return get_weather_data()


@app.route('/api/shopping', methods=['GET', 'PUT', 'DELETE'])
def shopping_list():
    if request.method == "GET":

        return get_shopping_list()

    elif request.method == "PUT":
        print(request.data)

    elif request.method == "DELETE":
        print(request.data)
        # return remove_from_list()


@app.route("/api/reddit")
def reddit():
    return top_threads()


@app.route('/api/lights', methods=['GET', 'PUT'])
def lights():
    if request.method == "GET":
        return get_lights()

    elif request.method == "PUT":
        data = request.data
        if not data:
            return send_update_lights()
        data = json.loads(data)
        return update_device_state(data['name'], data['on'])

    return ["Nothing"]


@app.route("/api/life360", methods=['GET'])
def life360():
    
    if request.method == "GET":
        return get_family_list()

if __name__ == "__main__":
    runListServer()
    app.run(port=PORT)
