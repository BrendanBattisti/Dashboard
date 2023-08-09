import dataclasses
import datetime
import json
import random
from dataclasses import dataclass
from typing import List, Union

from Modules.utils import Loggable, Logger, annotate, get_datetime_int



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

class RedditInterface(Loggable):

    def __init__(self, user: Union[User, dict], file: str, subreddits: List[str], logger: Logger):
        super().__init__(logger)

        if user is None:
            self.active = False

        try:
            import praw
            self.praw = praw
            self.active = True
        except ImportError:
            self.active = False

        self.reddit = self.login_user(user)
        self.file = file
        self.subreddits = subreddits

    def login_user(self, user: Union[dict, User]) -> 'praw.Reddit':
        """
        Logs in a user and returns a Reddit instance.

        Parameters:
        - user: An instance of the User class with the fields populated with the login credentials.

        Returns:
        - A Reddit instance that is logged in with the provided login credentials.
        """
        if type(user) == dict:
            user = User(**user)

        reddit = self.praw.Reddit(
            client_id=user.client_id,
            client_secret=user.secret,
            password=user.password,
            user_agent=user.user_agent,
            username=user.username,
        )
        reddit.read_only = True

        return reddit

    @annotate
    def get_top_threads(self, limit: int = 5):
        self.log("Getting top threads")
        


        index = 0
        threads = [None] * len(self.subreddits) * limit

        for sub in self.subreddits:
            subreddit = self.reddit.subreddit(sub)

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

    def save_threads(self, threads) -> None:
        with open(self.file, 'w') as json_file:
            json.dump(threads, json_file, indent=2)

    @annotate
    def load_threads(self):
        self.log("Loading Threads")
        try:
            with open(self.file) as json_file:
                obj = json.load(json_file)

            return obj
        except FileNotFoundError:
            return {}



    @annotate
    def top_threads(self):
        threads = self.load_threads()

        if threads:

            time_since_update = datetime.datetime.fromtimestamp(threads['dt']) - datetime.datetime.now()
            if time_since_update > datetime.timedelta(days=5):
                threads = self.get_top_threads()

                self.save_threads(threads)

        else:
            threads = self.get_top_threads()
            self.save_threads(threads)

        threads_list = threads['threads']
        random.shuffle(threads_list)
        return threads_list
