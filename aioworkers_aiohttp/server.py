from aiohttp import web
from aioworkers.net.server import SocketServer


class WebServer(SocketServer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._runner = None
        self._site = None

    async def init(self):
        self._runner = web.AppRunner(self.context.app)
        await self._runner.setup()
        self.context.on_connect.append(
            self.connect,
            self.config.get('groups', ())
        )
        self.context.on_disconnect.append(
            self.disconnect,
            self.config.get('groups', ())
        )

    async def connect(self):
        for sock in self._sockets:
            await web.SockSite(self._runner, sock).start()

    async def disconnect(self, ):
        await self._runner.cleanup()
