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


def remove_from_list(name: str) -> None:
    requests.delete(get_url(), params={'name': name})
