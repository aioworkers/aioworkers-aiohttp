from aiohttp import web
from aioworkers.net.server import SocketServer
from aioworkers.utils import import_name


class WebServer(SocketServer):
    port = None

    @classmethod
    def set_port(cls, port: int) -> None:
        cls.port = port

    def __init__(self, *args, **kwargs):
        self._runner = None
        self._kwargs = {}
        super().__init__(*args, **kwargs)

    def set_config(self, config):
        if self.port:
            config = config.new_child(port=self.port)
        super().set_config(config)
        access_log_cls = self.config.get('access_log.cls')
        if access_log_cls:
            cls = import_name(access_log_cls)
            self._kwargs['access_log_class'] = cls

    async def init(self):
        access_log_format = self.config.get('access_log.format')
        if not access_log_format:
            cfg = self.context.config
            for i in 'logging.formatters.access'.split('.'):
                if not cfg:
                    break
                cfg = cfg.get(i, {})
            else:
                access_log_format = cfg.get('format')
        if access_log_format:
            self._kwargs['access_log_format'] = access_log_format

        groups = self.config.get('groups', ())
        self.context.on_start.append(self.start, groups)
        self.context.on_stop.append(self.stop, groups)

    async def start(self):
        self._runner = web.AppRunner(self.context.app, **self._kwargs)
        await self._runner.setup()
        for sock in self._sockets:
            await web.SockSite(self._runner, sock).start()

    async def stop(self):
        await self._runner.cleanup()
