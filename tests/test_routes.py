import pytest
from aiohttp import web


route_table = web.RouteTableDef()


@pytest.fixture
def config_yaml():
    return """
    app:
      routes:
        - tests.test_routes.route_table
        - tests.test_routes.static
    """


@route_table.get('/a')
async def a(request):
    return web.HTTPOk()


static = web.static('/static', 'tests')


async def test_routes(context, aiohttp_client):
    client = await aiohttp_client(context.app)
    response = await client.get('/a')
    assert response.status == 200

    response = await client.get('/b')
    assert response.status == 404

    response = await client.get('/static/test_routes.py')
    assert response.status == 200
