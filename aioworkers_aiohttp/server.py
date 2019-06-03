from aiohttp import web
from aioworkers.net.server import SocketServer


class WebServer(SocketServer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._runner = None

    async def init(self):
        groups = self.config.get('groups', ())
        self.context.on_start.append(self.start, groups)
        self.context.on_stop.append(self.stop, groups)

    async def start(self):
        self._runner = web.AppRunner(self.context.app)
        await self._runner.setup()
        for sock in self._sockets:
            await web.SockSite(self._runner, sock).start()

    async def stop(self):
        await self._runner.cleanup()
