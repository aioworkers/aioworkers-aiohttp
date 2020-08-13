import pytest


@pytest.fixture
def config_yaml():
    return """
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
    """


async def test_init(context):
    assert 'app' in context
    assert 'timestamp' in context.app.router
    assert 'block:date' in context.app.router
