from pathlib import Path

import pytest

import aioworkers_aiohttp


CONFIG_PATH = Path(aioworkers_aiohttp.__file__).with_name('plugin.ini')


@pytest.fixture
def config(config):
    config.load(CONFIG_PATH)
    return config
