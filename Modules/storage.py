"""
Module for defining classes for storing/retrieving
data for the dashboard
"""

from abc import ABC, abstractmethod, ABCMeta
import datetime
import json
from Modules.utils import Loggable, get_datetime_int, get_time_difference


class Storage(Loggable, metaclass=ABCMeta):

    def __init__(self, logger):
        super().__init__(logger)
        self.data = {}

    def _generic_get(self, name: str):

        self.log(f"Getting {name}")
        self.load()
        last_refresh = self.data[name]['refresh_time']

        refresh = get_time_difference(last_refresh) > datetime.timedelta(day=1)

        response = {'data': self.data[name]['data'],
                    'refresh': refresh}
        
        return response

    def _generic_save(self, data, name: str):
        
        self.log(f"Saving {name}")
        self.data[name]['data'] = data
        self.data[name]['refresh_time'] = get_datetime_int()
        self.save()

    @abstractmethod
    def get_weather(self):
        return self._generic_get('weather')

    def save_weather(self, data):
        self._generic_save(data, 'weather')

    @abstractmethod
    def get_reddit(self):
        return self._generic_get('reddit')


    def save_reddit(self, data):
        self._generic_save(data, 'reddit')

    @abstractmethod
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
        self.file_path = file_path

    def save(self) -> None:
        super().save()
        with open(self.file_path, 'w') as file:
            json.dump(file, self.data)
    
    def load(self) -> None:
        
        super().load()
        with open(self.file_path) as file:
            self.data = json.load(file)
        
    

    