import pytest


@pytest.fixture
def config_yaml():
    return """
    app:
      router: null
      resources:
        /static1:
          static: tests
        /static2:
          static:
            path: tests
    """


async def test_init(context, aiohttp_client):
    client = await aiohttp_client(context.app)
    response = await client.get('/static1/test_static.py')
    assert response.status == 200, await response.text()
    text = await response.text()
    assert '/static' in text
    response = await client.get('/static2/test_static.py')
    assert response.status == 200, await response.text()
    text = await response.text()
    assert '/static' in text
