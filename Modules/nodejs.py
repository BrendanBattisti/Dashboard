from Modules.utils import Loggable


class NodeJSInterface(Loggable):

    def __init__(self, logger, port: int, path: str):
        super().__init__(logger)
        self.port = port
        self.path = path

    def get_url(self) -> str:
        return f"http://localhost:{self.port}/" + self.path
