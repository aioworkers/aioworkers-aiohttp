import pytest


@pytest.fixture
def aioworkers(aioworkers):
    aioworkers.plugins.append('aioworkers_aiohttp')
    return aioworkers
