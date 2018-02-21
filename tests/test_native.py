import pytest
import yaml


@pytest.fixture
def config(config):
    config(yaml.load("""
    app:
      router: null
      resources:
        /timestamp:
          name: timestamp
          priority: 1
          get:
            handler: datetime.datetime.now
        block:
          /date:
            name: date
            get: datetime.datetime.now
    app2:
       cls: aioworkers_aiohttp.app.Application
    """))
    return config


async def test_init(context):
    assert 'app' in context
    assert 'timestamp' in context.app.router
    assert 'block:date' in context.app.router
