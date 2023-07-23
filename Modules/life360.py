"""
Life 360 module for Dashboard
"""
import json
import requests


def get_config() -> dict:
    with open('nodeEnv.json') as json_file:
        return json.load(json_file)


def get_url() -> str:
    config = get_config()

    return f"http://localhost:{config['server']['port']}/life360"


def get_family_list() -> bytes:
    response = requests.get(get_url())
    print(response.content)
    return response.content


def remove_from_list(name: str) -> None:
    requests.delete(get_url(), params={'name': name})