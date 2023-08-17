import datetime
from Modules.config import CalendarConfigData
from Modules.storage import Storage, Interface
from Modules.utils import Logger
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


class CalendarInterface(Interface):

    def __init__(self, storage: Storage, logger: Logger):
        super().__init__(storage, logger)
        self.credentials = Credentials.from_authorized_user_info(
            self.storage.get_google()['data']
        )
        self.service = build('calendar', 'v3', credentials=self.credentials)

    def get_calendar_list(self):
        self.log("Getting user calendars")
        calendars_result = self.service.calendarList().list().execute()
        calendars = [{'id': x['id'], 'summary': x['summary']} for x in calendars_result['items']]
        return calendars



    def fetch_calendar(self):
        self.log("Fetching events")
        now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        
        events = []

        for calendar in self.get_calendar_list():
            events_result = self.service.events().list(calendarId=calendar['id'],
                                                    timeMin=now,
                                                    maxResults=10, singleEvents=True,
                                                    orderBy='startTime').execute()
            events = events + events_result.get('items', [])
        return events
        # with open("calendarstuff.json", 'w') as file:
        #    json.dump(calendars, file, indent=2)
        # print(calendars)

        # Prints the start and name of the next 10 events
        # for event in events:
        #    start = event['start'].get('dateTime', event['start'].get('date'))
        #    print(start, event['summary'])
