"""
Life 360 module for Dashboard
"""
import requests

import Modules.nodejs


def get_url():
    return Modules.nodejs.get_url("life360")


def get_family_list() -> bytes:
    response = requests.get(get_url())
    print(response.content)
    return response.content


def remove_from_list(name: str) -> None:
    requests.delete(get_url(), params={'name': name})
