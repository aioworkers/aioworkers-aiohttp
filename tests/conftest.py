from pathlib import Path

import pytest
from aioworkers.core.config import Config
from aioworkers.core.context import Context

import aioworkers_aiohttp


CONFIG_PATH = Path(aioworkers_aiohttp.__file__).with_name('plugin.ini')


@pytest.fixture
def config():
    return Config().load(CONFIG_PATH)


@pytest.fixture
def context(loop, config):
    with Context(config, loop=loop) as ctx:
        yield ctx
