import pytest
import yaml


@pytest.fixture
def config(config):
    config(yaml.load("""
    app:
      resources:
        /timestamp:
          name: timestamp
          priority: 1
          get:
            handler: time.time
        block:
          /date:
            name: date
            get: datetime.datetime.now
    """))
    return config


async def test_init(context):
    assert 'app' in context
    assert 'timestamp' in context.app.router
    assert 'block:date' in context.app.router
