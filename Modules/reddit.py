import dataclasses
from dataclasses import dataclass
from typing import List, Union

from Modules.storage import Storage
from Modules.utils import Loggable, Logger, annotate


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

    def __init__(self, user: Union[User, dict], storage: Storage, logger: Logger):
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
        self.storage = storage

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
    def get_top_threads(self, subreddits: List[str], limit: int = 5):
        self.log("Getting top threads")

        index = 0
        threads = [None] * len(subreddits) * limit

        for sub in subreddits:
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
        return [dataclasses.asdict(x) for x in threads if x is not None]

    def save_threads(self, threads) -> None:
        self.storage.save_reddit(threads)

    @annotate
    def get_threads(self):
        self.log("Loading Threads")
        data = self.storage.get_reddit()
        if data['refresh']:

            if 'data' not in data:
                data['data'] = {'threads': [], "subreddits": []}

            if 'subreddits' in data['data']:
                data['data']['threads'] = self.get_top_threads(data['data']['subreddits'])

            self.storage.save_reddit(data['data'])
        return data['data']['threads']

