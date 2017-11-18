from aiohttp import web
from aioworkers.humanize import parse_size


class Application(web.Application):
    def __init__(self, config, *, context, **kwargs):
        self.config = config
        self.context = context
        if 'client_max_size' in config:
            kwargs['client_max_size'] = parse_size(config.client_max_size)
        super().__init__(**kwargs)
        context.run_forever = self.run_forever

    async def init(self):
        pass

    def run_forever(self):
        gconf = self.context.config
        host = gconf.http.host
        port = gconf.http.port
        web.run_app(self, host=host, port=port, loop=self.context.loop)
