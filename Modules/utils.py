import datetime
from env import DEBUG


def get_datetime_int():
    return int(datetime.datetime.now().strftime('%Y%m%d'))


def debug_msg(text: str) -> None:
    if DEBUG: print(text)
