import json
from Modules.config import CalendarConfig, load_config
from Modules.storage import FileStorage, Interface, Storage
from Modules.utils import Logger, PrintLogger
import re
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
class GoogleInterface(Interface):

    def __init__(self, config: CalendarConfig, storage: Storage, logger: Logger):
        super().__init__(storage, logger)
        self.config = config

    def check_credentials(self):
        token = self.storage.get_google()
        
        redirects = self.config.credentials.web.redirect_uris
        port = None
        for url in redirects:
            local_host_url = re.findall("localhost:[0-9]+", url)
            if local_host_url:
                port = int(local_host_url[0].split(":")[1])

        if not port:
            
            print("No valid redirect")
            return

        if 'data' in token:
            token = token['data']
        else:
            token = None

        creds = None

        if token:
            creds = Credentials.from_authorized_user_info(token, self.config.scopes)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_config(
                    self.config.credentials.model_dump(), self.config.scopes)
                creds = flow.run_local_server(port=port)
        self.storage.save_google(json.loads(creds.to_json()))
            
def main():

    config = load_config("config.json")

    logger = PrintLogger()
    storage = FileStorage(config.storage_file, logger)

    interface = GoogleInterface(config.calendar, storage, logger)

    interface.check_credentials()

main()