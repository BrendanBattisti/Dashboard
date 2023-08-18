import datetime
from typing import List

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

from Modules.storage import Storage, Interface, Event
from Modules.utils import Logger


class CalendarInterface(Interface):

    def __init__(self, storage: Storage, logger: Logger):
        super().__init__(storage, logger)

        google_data = self.storage.get_google()

        if 'data' in google_data:
            self.active = True
            self.credentials = Credentials.from_authorized_user_info(
                google_data['data']
            )
            self.service = build('calendar', 'v3', credentials=self.credentials)
        else:
            self.active = False

    def get_calendar_list(self):
        if self.active:
            self.log("Getting user calendars")
            calendars_result = self.service.calendarList().list().execute()
            calendars = [{'id': x['id'], 'summary': x['summary']} for x in calendars_result['items']]
            return calendars

    def fetch_calendar(self):
        if self.active:
            self.log("Fetching events")
            now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
            endTime = (datetime.datetime.utcnow() + datetime.timedelta(days=31)).isoformat() + "Z"
            events = []

            for calendar in self.get_calendar_list():
                events_result = self.service.events().list(calendarId=calendar['id'],
                                                           timeMin=now,
                                                           timeMax=endTime,
                                                           maxResults=10, singleEvents=True,
                                                           orderBy='startTime').execute()
                events = events + events_result.get('items', [])

            results = [Event() for x in events]

            for index, event in enumerate(results):
                event.from_google(events[index])

            results = list(set(results))

            results.sort()

            results = [x.model_dump() for x in results]

            return results
        return []

    def get_calendar_events(self) -> List[dict]:

        data = self.storage.get_calendar()

        if data['refresh']:
            data = self.fetch_calendar()
            self.storage.save_calendar(data)
            return data

        return data['data']
