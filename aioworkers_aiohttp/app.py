from pathlib import Path

from aiohttp import web
from aioworkers.humanize import parse_size
from aioworkers.utils import import_name


class Application(web.Application):
    def __init__(self, config, *, context, **kwargs):
        self.config = config
        self.context = context
        if 'client_max_size' in config:
            kwargs['client_max_size'] = parse_size(config.client_max_size)

        if not config.get('router'):
            pass
        elif isinstance(config.router, str):
            cls = import_name(config.router)
            kwargs['router'] = cls()
        else:
            cfg = config.router.copy()
            cls = import_name(cfg.pop('cls'))
            kwargs['router'] = cls(**cfg)

        if not config.get('middlewares'):
            pass
        elif isinstance(config.middlewares, list):
            kwargs['middlewares'] = map(import_name, config.middlewares)
        else:
            raise TypeError('Middlewares should be described in list')

        super().__init__(**kwargs)

        resources = self.config.get('resources')
        for url, name, routes in sort_resources(resources):
            if 'include' in routes:
                self.router.include(**routes)
                continue
            resource = self.router.add_resource(url, name=name)
            for method, params in routes.items():
                handler = params.pop('handler')
                resource.add_route(method.upper(), import_name(handler))

        context.run_forever = self.run_forever

    async def init(self):
        pass

    def run_forever(self, host=None, port: int=None):
        gconf = self.context.config
        host = host or gconf.http.host
        port = port or gconf.http.port
        web.run_app(self, host=host, port=port, loop=self.context.loop)


def iter_resources(resources):
    if not resources:
        return
    elif not isinstance(resources, dict):
        raise TypeError(
            'Resources should be described in dict %s' % resources)
    for name, sub in resources.items():
        if not isinstance(sub, dict):
            raise TypeError(
                'Resource should be described in dict %s' % sub)
        routes = sub.copy()
        priority = routes.pop('priority', 0)
        if 'include' in routes:
            url = name if name.startswith('/') else None
            sub.setdefault('base', url)
            assert sub['base'] == url
            yield priority, url, name, sub
            continue
        elif not name.startswith('/'):
            for p, u, n, rs in iter_resources(sub):
                yield priority + p, u, ':'.join((name, n)), rs
            continue
        url = name
        name = routes.pop('name', None)
        for k, v in routes.items():
            if 'include' in routes:
                continue
            elif isinstance(v, str):
                routes[k] = {'handler': v}
        yield priority, url, name, routes


def sort_resources(resources):
    r = sorted(iter_resources(resources), key=lambda x: x[0], reverse=True)
    return map(lambda x: x[1:], r)
