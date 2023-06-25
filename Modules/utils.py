import datetime
from env import DEBUG


def get_datetime_int():
    return int(datetime.datetime.now().strftime('%Y%m%d'))


def get_time_difference(time_int: int) -> datetime.timedelta:
    return datetime.datetime.fromtimestamp(time_int) - datetime.datetime.now()


def debug_msg(text: str) -> None:
    if DEBUG: print(text)
