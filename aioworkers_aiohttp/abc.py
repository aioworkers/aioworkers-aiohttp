from abc import ABC, abstractmethod
from typing import Protocol

from aiohttp.web import Application


class PRouter(Protocol):
    @abstractmethod
    def setup(self, app: Application):
        pass

    @abstractmethod
    def set_cors(self, app: Application, **kwargs):
        pass

    @abstractmethod
    def add_resource(self, url: str, **kwargs):
        pass


class AbstractSwaggerRouter(ABC):
    pass
