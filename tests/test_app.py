import pytest
import yaml


async def startup(app):
    app['1234'] = None


@pytest.fixture
def config(config):
    config.update(yaml.load("""
    app:
      router:
        search_in_modules:
          - datetime
      resources:
        /timestamp:
          name: timestamp
          priority: 1
          get:
            handler: uuid.uuid4
        block:
          /date:
            name: date
            get: datetime.datetime.now
      on_startup:
        s1: tests.test_app.startup
    """))
    return config


async def test_init(context):
    assert 'app' in context
    assert 'timestamp' in context.app.router
    assert 'block:date' in context.app.router
