"""
SERVER
"""

from flask import Flask

from weather import get_weather_data

app = Flask(__name__)


@app.route('/weather')
def index():
    return get_weather_data()


app.run(port=3001)
