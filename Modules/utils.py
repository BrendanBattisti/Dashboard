from dataclasses import dataclass
import datetime
from abc import ABC, abstractmethod

from env import DEBUG


def get_datetime_int():
    return int(datetime.datetime.now().strftime('%Y%m%d'))


def get_time_difference(time_int: int) -> datetime.timedelta:
    return datetime.datetime.fromtimestamp(time_int) - datetime.datetime.now()


def debug_msg(text: str) -> None:
    if DEBUG: print(text)


def annotate(f):
    def inner(*args, **kwargs):
        print(f.__name__)
        result = f(*args, **kwargs)
        print(type(result))
        return result

    return inner

@dataclass
class Configuration:

    # Server
    port: int
    debug: bool

    # Reddit
    reddit_user: str
    reddit_password: str

    # Weather
    weather_key: str



class Loggable:

    def __init__(self, logger):
        self.logger = logger

    def log(self, msg):
        self.logger.log(msg)


class Logger(ABC):

    def __init__(self) -> None:
        pass

    @abstractmethod
    def log(self, msg) -> None:
        print(msg)


class PrintLogger(Logger):

    def __init__(self):
        super().__init__()

    def log(self, msg) -> None:
        print(msg)

class BlankLogger(Logger):

    def __init__(self) -> None:
        super().__init__()

    def log(self, msg) -> None:
        pass

class FileLogger(Logger):

    def __init__(self, file_path: str) -> None:
        super().__init__()
        self.path = file_path

    def log(self, msg):

        with open(self.path, 'w') as log_file:
            log_file.write(msg)