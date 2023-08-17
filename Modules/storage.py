"""
Module for defining classes for storing/retrieving
data for the dashboard
"""

from abc import ABC, abstractmethod, ABCMeta
import datetime
import json
from dataclasses import dataclass

from pydantic import BaseModel

from Modules.utils import Loggable, Logger


class Storage(Loggable, metaclass=ABCMeta):

    def __init__(self, logger):
        super().__init__(logger)
        self.data = {}

    def _generic_get(self, name: str):
        self.log(f"Getting {name}")
        self.load()

        if name not in self.data:
            return {'refresh': True}

        if not self.data[name]['data']:
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

    def get_calendar(self):
        return self._generic_get('calendar')

    def save_calendar(self, data):
        self._generic_save(data, 'calendar')

    def get_google(self):
        return self._generic_get('google')
    
    def save_google(self, data):
        return self._generic_save(data, 'google')

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


class Interface(Loggable):

    def __init__(self, storage: Storage, logger: Logger):
        super().__init__(logger)
        self.storage = storage


"""
Kasa Lights
"""


class Light(BaseModel):
    ip: str
    on: bool
    name: str

    def to_public(self):
        return PublicLight(**{'on': self.on, 'name': self.name})


class PublicLight(BaseModel):
    on: bool
    name: str


    def __lt__(self, other: 'Light'):
        return self.name < other.name



"""
Reddit
"""


class Thread(BaseModel):
    title: str
    upvotes: int
    comments: int
    link: str
    subreddit_img: str

"""
Google
"""

class GoogleCredentials(BaseModel):

    token: str = "" 
    refresh_token: str = ""
    token_uri: str = "" 
    client_id: str = "" 
    client_secret: str = ""
    expiry: str = "" 

"""
Calendar
"""

class Event(BaseModel):

    name: str = ""
    organizer: str = ""
    organizer_email: str = ""
    link: str = ""
    start: datetime.datetime = None
    end: datetime.datetime = None

    def __hash__(self) -> int:
        return hash(self.name + self.start)
    
    def __lt__(self, other: 'Event'):
        return datetime.datetime.strptime(self.start, "%Y-%m-%d") < datetime.datetime.strptime(other.start, "%Y-%m-%d") 

    def from_google(self, event: dict):
        if event is None:
            return
        if 'organizer' in event:
            self.organizer = event['organizer']['displayName']
            self.organizer_email = event['organizer']['email']

        if 'start' in event:
            self.start = event['start']['date']
        if 'end' in event:
            self.end = event['end']['date']


        self.link = event['htmlLink']
        self.name = event['summary']    


