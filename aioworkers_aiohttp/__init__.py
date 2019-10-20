import argparse
from pathlib import Path
from typing import Dict, Iterable, Tuple

from aioworkers.core.plugin import Plugin

from .server import WebServer


try:
    from .version import __version__
except ImportError:
    __version__ = 'dev'

BASE = Path(__file__).parent


class plugin(Plugin):
    configs = (
        BASE / 'plugin.ini',
    )

    def __init__(self):
        super().__init__()
        self._config = {}

    def get_config(self) -> Dict:
        return self._config

    def add_arguments(self, parser: argparse.ArgumentParser):
        try:
            parser.add_argument('--port', type=int)
        except argparse.ArgumentError:
            pass

    def parse_known_args(
        self, args: Iterable[str],
        namespace: argparse.Namespace,
    ) -> Tuple[argparse.Namespace, Iterable[str]]:
        if namespace.port:
            WebServer.set_port(namespace.port)
        return namespace, args
