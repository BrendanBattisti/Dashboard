from typing import List
import json

from pydantic import BaseModel


class RedditUser(BaseModel):
    username: str = ""
    password: str = ""
    secret: str = ""
    client_id: str = ""
    user_agent: str = ""


class ShoppingConfig(BaseModel):
    username: str = ""
    password: str = ""
    shopping_list: str = ""

class CalendarConfigData(BaseModel):

    client_id: str = "" 
    project_id: str = "" 
    auth_uri: str = "" 
    token_uri: str = "" 
    auth_provider_x509_cert_url: str = "" 
    client_secret: str = "" 
    redirect_uris: List[str] = [] 
  

class CalendarConfig(BaseModel):
    web: CalendarConfigData = CalendarConfigData(**{})


class Configuration(BaseModel):
    # Server
    server_port: int = 3001
    node_port: int = 3002
    debug: bool = False

    # Storage
    storage_file: str = ""

    # Reddit
    reddit: RedditUser = RedditUser(**{})

    # Shopping
    shopping: ShoppingConfig = ShoppingConfig(**{})

    # Calendar
    calendar: CalendarConfig = CalendarConfig(**{})

    # Weather
    weather_key: str = ""


def load_config(filename: str) -> Configuration:
    try:
        with open(filename) as file:
            data = json.load(file)
    except FileNotFoundError:
        print("Config File not found")
        data = {}

    config = Configuration(**data)
    

    with open(filename, 'w') as file:
        file.write(config.model_dump_json( indent=2),)

    return config
