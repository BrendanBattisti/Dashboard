import dataclasses
import datetime
import json
import random
from dataclasses import dataclass
from typing import List

import praw as praw

from Modules.utils import get_datetime_int, debug_msg
from env import REDDIT_USER, SUBREDDITS_FILE, THREADS_FILE


@dataclass
class User:
    username: str
    password: str
    secret: str
    client_id: str
    user_agent: str


@dataclass
class Thread:
    title: str
    upvotes: int
    comments: int
    link: str
    subreddit_img: str


def login_user(user: User) -> praw.Reddit:
    """
    Logs in a user and returns a Reddit instance.

    Parameters:
    - user: An instance of the User class with the fields populated with the login credentials.

    Returns:
    - A Reddit instance that is logged in with the provided login credentials.
    """
    reddit = praw.Reddit(
        client_id=user.client_id,
        client_secret=user.secret,
        password=user.password,
        user_agent=user.user_agent,
        username=user.username,
    )
    reddit.read_only = True

    return reddit


def get_top_threads(limit: int = 5):
    debug_msg("Getting top threads")
    reddit = login_user(User(**REDDIT_USER))

    subreddits = get_subreddits()

    index = 0
    threads = [None] * len(subreddits) * limit

    for sub in subreddits:
        subreddit = reddit.subreddit(sub)

        # Scrape the threads
        for thread in subreddit.hot(limit=limit):
            if thread.stickied:
                continue

            new_thread = Thread(title=thread.title,
                                upvotes=thread.ups,
                                comments=thread.num_comments,
                                link=f"https://www.reddit.com/{thread.permalink}",
                                subreddit_img=subreddit.icon_img)
            threads[index] = new_thread
            index += 1
    return {"dt": get_datetime_int(), "threads": [dataclasses.asdict(x) for x in threads if x is not None]}


def save_threads(filename: str, threads) -> None:
    with open(filename, 'w') as json_file:
        json.dump(threads, json_file, indent=2)


def load_threads(filename: str):
    debug_msg("Loading Threads")
    try:
        with open(filename) as json_file:
            obj = json.load(json_file)

        return obj
    except FileNotFoundError:
        return {}


def get_subreddits() -> List[str]:
    return ['technology']


def top_threads():
    threads = load_threads(THREADS_FILE)

    if threads:

        time_since_update = datetime.datetime.fromtimestamp(threads['dt']) - datetime.datetime.now()
        if time_since_update > datetime.timedelta(days=5):
            threads = get_top_threads()

            save_threads(THREADS_FILE, threads)

    else:
        threads = get_top_threads()
        save_threads(THREADS_FILE, threads)

    threads_list = threads['threads']
    random.shuffle(threads_list)
    return threads_list
