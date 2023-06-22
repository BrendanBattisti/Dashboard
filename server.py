"""
SERVER
"""
import json

from flask import Flask, request

from Modules.lights import get_lights, send_update_lights, update_device_state
from Modules.weather import get_weather_data
from Modules.reddit import top_threads

app = Flask(__name__)


@app.route('/weather')
def weather():
    return get_weather_data()


@app.route('/life360')
def life360():
    return "Penis"


@app.route("/reddit")
def reddit():
    return top_threads()


@app.route('/lights', methods=['GET', 'PUT'])
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


app.run(port=3001)
