import datetime
from env import DEBUG
from abc import ABC

def get_datetime_int():
    return int(datetime.datetime.now().strftime('%Y%m%d'))


def get_time_difference(time_int: int) -> datetime.timedelta:
    return datetime.datetime.fromtimestamp(time_int) - datetime.datetime.now()


def debug_msg(text: str) -> None:
    if DEBUG: print(text)

def annotate(f):
    

    def inner():
        print(f.__name__)
        result = f()
        print(type(result))
        return result
    return inner

class Logger(ABC):

    def __init__(self) -> None:
        pass
    
    @ABC.abstractmethod
    def log(self, msg) -> None:
        print(msg)

