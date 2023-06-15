"""
SERVER
"""
import json

from flask import Flask, request

from Modules.lights import get_lights, send_update_lights
from Modules.weather import get_weather_data

app = Flask(__name__)


@app.route('/weather')
def weather():
    return get_weather_data()


@app.route('/life360')
def life360():
    return "Penis"


@app.route('/lights', methods=['GET'])
def lights():
    return get_lights()


@app.route('/lights', methods=['PUT'])
def lights():
    data = json.loads(request.data)
    if not data:
        return send_update_lights()
    print(data)


app.run(port=3001)
