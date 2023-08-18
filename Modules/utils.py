from abc import ABC, abstractmethod


def annotate(f):
    def inner(*args, **kwargs):
        # print(f.__name__)
        result = f(*args, **kwargs)
        # print(type(result))
        return result

    return inner


class Loggable:

    def __init__(self, logger):
        self.logger = logger

    def log(self, msg):
        self.logger.log(msg)


class Logger(ABC):

    def __init__(self) -> None:
        pass

    @abstractmethod
    def log(self, msg) -> None:
        print(msg)


class PrintLogger(Logger):

    def __init__(self):
        super().__init__()

    def log(self, msg) -> None:
        print(msg)


class BlankLogger(Logger):

    def __init__(self) -> None:
        super().__init__()

    def log(self, msg) -> None:
        pass


class FileLogger(Logger):

    def __init__(self, file_path: str) -> None:
        super().__init__()
        self.path = file_path

    def log(self, msg):
        with open(self.path, 'a') as log_file:
            log_file.write(msg + "\n")
