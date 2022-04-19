import logging
import sys
from typing import Dict
from aiohttp.web import Application

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


class LoggerFactory:
    def __init__(self):
        self.loggers: Dict[str, logging.Logger] = dict()

    def get_logger(self, name: str) -> logging.Logger:
        if name not in self.loggers:
            self.loggers[name] = logging.getLogger(name)
        return self.loggers[name]


async def setup_logger_factory(app: Application):
    app['logger_factory'] = LoggerFactory()
    yield
