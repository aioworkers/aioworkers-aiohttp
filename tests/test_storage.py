import tempfile

import pytest
from aiohttp import web
from aioworkers.core.config import Config
from aioworkers.core.context import Context
from aioworkers.storage import StorageError
from yarl import URL

from aioworkers_aiohttp.storage import Storage


@pytest.fixture
def config(config):
    with tempfile.TemporaryDirectory() as d:
        config.update(
            fs=dict(
                cls='aioworkers.storage.filesystem.FileSystemStorage',
                path=d,
                format='json',
            )
        )
        return config


async def test_set_get(event_loop, aiohttp_client):
    app = web.Application()
    app.router.add_get("/test/1", lambda x: web.json_response(["Python"]))  # type: ignore
    client = await aiohttp_client(app)
    url = client.make_url('/')

    data = 'Python'
    config = Config()
    config.update(
        storage=dict(
            cls='aioworkers_aiohttp.storage.Storage',
            prefix=str(url),
            semaphore=1,
            format='json',
        )
    )
    async with Context(config=config, loop=event_loop) as context:
        storage = context.storage
        assert data in await storage.get('test/1')
        with pytest.raises(StorageError):
            await storage.set('test/1', data)


async def test_copy(event_loop, aiohttp_client, config):
    app = web.Application()
    app.router.add_get("/test/1", lambda x: web.json_response(["Python"]))  # type: ignore
    client = await aiohttp_client(app)
    url = client.make_url('/')

    data = 'Python'
    config.update(
        storage=dict(
            cls='aioworkers_aiohttp.storage.Storage',
            prefix=str(url),
            semaphore=1,
            format='json',
        )
    )
    async with Context(config=config, loop=event_loop) as context:
        await context.storage.copy('test/1', context.fs, 'test/1')
        assert data in await context.fs.get('test/1')


async def test_format(event_loop):
    config = Config()
    config.update(
        dict(
            name="",
            semaphore=1,
            format="bytes",
        )
    )
    context = Context(config=config, loop=event_loop)
    await context.init()
    storage = Storage(config, context=context, loop=event_loop)
    await storage.init()
    assert isinstance(storage.raw_key('test'), URL)
    await storage.cleanup_session()
