from aiohttp import web
from aioworkers.humanize import parse_size
from aioworkers.utils import import_name


class Application(web.Application):
    def __init__(self, config, *, context, **kwargs):
        self.config = config
        self.context = context
        if 'client_max_size' in config:
            kwargs['client_max_size'] = parse_size(config.client_max_size)
        super().__init__(**kwargs)

        resources = self.config.get('resources', ())
        for url, name, routes in sort_resources(resources):
            resource = self.router.add_resource(url, name=name)
            for method, handler in routes.items():
                resource.add_route(method.upper(), import_name(handler))

        context.run_forever = self.run_forever

    async def init(self):
        pass

    def run_forever(self, host=None, port: int=None):
        gconf = self.context.config
        host = host or gconf.http.host
        port = port or gconf.http.port
        web.run_app(self, host=host, port=port, loop=self.context.loop)


def iter_resouces(resources):
    for name, sub in resources.items():
        if not name.startswith('/'):
            for p, u, n, rs in iter_resouces(sub):
                yield p, u, ':'.join((name, n)), rs
            continue
        url = name
        routes = sub.copy()
        name = routes.pop('name', None)
        priority = routes.pop('priority', 0)
        yield priority, url, name, routes


def sort_resources(resources):
    r = sorted(iter_resouces(resources), key=lambda x: x[0])
    return map(lambda x: x[1:], r)
