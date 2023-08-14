"""
Module for defining classes for storing/retrieving
data for the dashboard
"""

from abc import ABC, abstractmethod, ABCMeta
import datetime
import json
from Modules.utils import Loggable


class Storage(Loggable, metaclass=ABCMeta):

    def __init__(self, logger):
        super().__init__(logger)
        self.data = {}

    def _generic_get(self, name: str):
        self.log(f"Getting {name}")
        self.load()

        if name not in self.data:
            return {'refresh': True}

        last_refresh = self.data[name]['refresh_time']
        refresh_datetime = datetime.datetime.strptime(last_refresh, "%H: %M %d/%m/%Y")
        refresh = (datetime.datetime.now() - refresh_datetime) > datetime.timedelta(days=1)

        response = {
            'data': self.data[name]['data'],
            'refresh': refresh
        }

        return response

    def _generic_save(self, data, name: str):
        self.log(f"Saving {name}")
        if name not in self.data:
            self.data[name] = {}

        self.data[name]['data'] = data
        self.data[name]['refresh_time'] = datetime.datetime.now().strftime("%H: %M %d/%m/%Y")
        self.save()

    def get_weather(self):
        return self._generic_get('weather')

    def save_weather(self, data):
        self._generic_save(data, 'weather')

    def get_reddit(self):
        return self._generic_get('reddit')

    def save_reddit(self, data):
        self._generic_save(data, 'reddit')

    def get_lights(self):
        return self._generic_get('lights')

    def save_lights(self, data):
        self._generic_save(data, 'lights')

    @abstractmethod
    def save(self) -> None:
        self.log("Saving data")

    @abstractmethod
    def load(self) -> None:
        self.log("Loading data")


class FileStorage(Storage, ABC):

    def __init__(self, file_path: str, logger):
        super().__init__(logger)

        if not file_path:
            raise FileNotFoundError("Storage file not designated")
        self.file_path = file_path

    def save(self) -> None:
        super().save()
        with open(self.file_path, 'w') as file:
            json.dump(self.data, file, indent=2)

    def load(self) -> None:
        super().load()

        try:
            with open(self.file_path) as file:
                self.data = json.load(file)
        except FileNotFoundError:
            self.data = {}
