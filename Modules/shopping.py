"""
Shopping module
"""
import json

import requests

from Modules.nodejs import NodeJSInterface
from Modules.utils import annotate, Logger


class ShoppingInterface(NodeJSInterface):

    def __init__(self, port: int, logger: Logger):
        super().__init__(logger, port, "shopping")

    def get_shopping_list(self) -> bytes:
        response = requests.get(self.get_url())
        return response.content

    @annotate
    def remove_from_list(self, name: str):
        data = requests.delete(self.get_url(), json={'item': name})
        return json.loads(data.content)

    @annotate
    def add_to_list(self, item: str):
        data = requests.post(self.get_url(), json={'item': item})
        return json.loads(data.content)