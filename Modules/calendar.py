from ast import List
import datetime
from Modules.storage import Storage
from Modules.utils import Logger
from utils import Logger
from storage import Storage, Interface
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']


class CalendarInterface(Interface):

    def __init__(self, Credentials, storage: Storage, logger: Logger):
        super().__init__(storage, logger)
        self.credentials = Credentials.from_authorized_user_info(

        )
        self.service = build('calendar', 'v3', credentials=self.credentials)

    def get_calendar_list(self):
        calendars_result = self.service.calendarList.list().execute()
        print(calendars_result)
        return calendars_result

    def fetch_calendar(self) -> List[any]:
        self.log("Fetching events")
        now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        # events_result = self.service.events().list(calendarId='family14527635731341883679@group.calendar.google.com',
        #                                           timeMin=now,
        #                                           maxResults=10, singleEvents=True,
        #                                           orderBy='startTime').execute()
        # events = events_result.get('items', [])

        # with open("calendarstuff.json", 'w') as file:
        #    json.dump(calendars, file, indent=2)
        # print(calendars)

        # Prints the start and name of the next 10 events
        # for event in events:
        #    start = event['start'].get('dateTime', event['start'].get('date'))
        #    print(start, event['summary'])
