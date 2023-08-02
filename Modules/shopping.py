"""
Shopping module
"""
import json
import requests

import Modules.nodejs


def get_url():
    return Modules.nodejs.get_url("shopping")


def get_shopping_list() -> bytes:
    response = requests.get(get_url())
    return response.content


def remove_from_list(name: str):
    data = requests.delete(get_url(), json={'item': name})
    return json.loads(data.content)


def add_to_list(item: str):
    data = requests.post(get_url(), json={'item': item})
    return json.loads(data.content)