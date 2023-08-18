import datetime
from typing import List

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

from Modules.storage import Storage, Interface, Event, Calendar
from Modules.utils import Logger


def format_response_calendar(data) -> dict:
    today = datetime.date.today()
    one_week_later = today + datetime.timedelta(days=7)

    today_events = [x for x in data if datetime.datetime.strptime(x['start'], "%Y-%m-%d").date() == today]
    week_events = [x for x in data if datetime.datetime.strptime(x['start'], "%Y-%m-%d").date() <= one_week_later and x not in today_events]
    for event in week_events:
        event['name'] = f"{event['name']} - {datetime.datetime.strptime(event['start'], '%Y-%m-%d').strftime('%A')}"
    month_events = [x for x in data if x not in today_events and x not in week_events]
    for event in month_events:
        event['name'] = f"{event['name']} - {datetime.datetime.strptime(event['start'], '%Y-%m-%d').strftime('%-d')}"
    return {1: (today_events, "Today"), 2: (week_events, "This Week"), 3: (month_events, "This Month"), }


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

    def get_calendar_list(self) -> List[Calendar]:
        if self.active:
            self.log("Getting user calendars")
            calendars_result = self.service.calendarList().list().execute()
            calendars = [Calendar() for x in calendars_result['items']]
            for index, calendar in enumerate(calendars):
                calendar.from_google(calendars_result['items'][index])

            return calendars

    def fetch_calendar(self):
        if self.active:
            self.log("Fetching events")
            now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
            endTime = (datetime.datetime.utcnow() + datetime.timedelta(days=31)).isoformat() + "Z"
            events = []

            for calendar in self.get_calendar_list():
                events_result = self.service.events().list(calendarId=calendar.id,
                                                           timeMin=now,
                                                           timeMax=endTime,
                                                           maxResults=10, singleEvents=True,
                                                           orderBy='startTime').execute()
                events_result = events_result.get('items', [])
                new_events = [Event() for x in events_result]
                for index, event in enumerate(new_events):
                    event.from_google(events_result[index])
                    event.from_calendar(calendar)
                events = events + new_events

            results = list(set(events))

            results.sort()

            results = [x.model_dump() for x in results]

            return results
        return []

    def get_calendar_events(self) -> dict:

        data = self.storage.get_calendar()

        if data['refresh']:
            data = self.fetch_calendar()
            self.storage.save_calendar(data)
            return format_response_calendar(data)

        return format_response_calendar(data['data'])
