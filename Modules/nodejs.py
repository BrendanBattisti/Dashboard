import json


def get_config() -> dict:
    with open('nodeEnv.json') as json_file:
        return json.load(json_file)


def get_url(path: str) -> str:
    config = get_config()

    return f"http://localhost:{config['server']['port']}/" + path
