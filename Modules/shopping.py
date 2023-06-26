"""
Shopping module
"""
import json
import requests


def get_config() -> dict:
    with open('shoppingEnv.json') as json_file:
        return json.load(json_file)


def get_url() -> str:
    config = get_config()

    return f"http://localhost:{config['port']}/shopping"


def get_list() -> bytes:
    response = requests.get(get_url())
    return response.content


def remove_from_list(name: str) -> None:
    requests.delete(get_url(), params={'name': name})
