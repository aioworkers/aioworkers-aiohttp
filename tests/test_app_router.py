import pytest

from aioworkers_aiohttp.abc import AbstractSwaggerRouter


@pytest.fixture
def config_yaml():
    return """
    app:
      router:
        setup: true
      resources:
        /timestamp:
          name: timestamp
          priority: 1
          get:
            handler: uuid.uuid4
    """


async def test_init(context):
    assert 'app' in context
    assert 'timestamp' in context.app.router
    assert not isinstance(context.app.router, AbstractSwaggerRouter)
