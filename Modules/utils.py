import dataclasses
import json
from abc import ABC, abstractmethod
from dataclasses import dataclass
from storage import Storage
from env import DEBUG


def debug_msg(text: str) -> None:
    if DEBUG: print(text)


def annotate(f):
    def inner(*args, **kwargs):
        # print(f.__name__)
        result = f(*args, **kwargs)
        # print(type(result))
        return result

    return inner


@dataclass
class Configuration:
    # Server
    server_port: int = 3001
    node_port: int = 3002
    debug: bool = False

    # Storage
    storage_file: str = ""

    # Reddit
    reddit_user: str = ""
    reddit_password: str = ""
    reddit_secret: str = ""
    reddit_client_id: str = ""
    reddit_user_agent: str = ""

    # Shopping List
    shopping_username: str = ""
    shopping_password: str = ""
    shopping_list: str = ""

    # Weather
    weather_key: str = ""


def load_config(filename: str) -> Configuration:
    try:
        with open(filename) as file:
            data = json.load(file)
    except FileNotFoundError:
        print("Config File not found")
        data = {}

    config = Configuration(**data)
    with open(filename, 'w') as file:
        json.dump(dataclasses.asdict(config), file, indent=2)

    return config


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
        with open(self.path, 'a') as log_file:
            log_file.write(msg + "\n")


class Interface(Loggable):

    def __init__(self, storage: Storage, logger: Logger):
        super().__init__(logger)
        self.storage = storage