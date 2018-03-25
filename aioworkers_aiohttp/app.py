from aiohttp import web
from aioworkers.humanize import parse_size
from aioworkers.utils import import_name

from .abc import AbstractSwaggerRouter


class Application(web.Application):
    def __init__(self, config, *, context, **kwargs):
        self.config = config
        self.context = context
        cors = None

        debug = config.get('debug')
        if isinstance(debug, bool):
            kwargs.setdefault('debug', debug)

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
            cors = cfg.pop('cors', None)
            kwargs['router'] = cls(**cfg)

        if not config.get('middlewares'):
            pass
        elif isinstance(config.middlewares, list):
            kwargs['middlewares'] = map(import_name, config.middlewares)
        else:
            raise TypeError('Middlewares should be described in list')

        super().__init__(**kwargs)

        if cors is not None:
            kwargs['router'].set_cors(self, **cors)

        if config.get('main'):
            context.run_forever = self.run_forever

    async def init(self):
        resources = self.config.get('resources')
        is_swagger = isinstance(self.router, AbstractSwaggerRouter)
        default_validate = self.config.get('router.default_validate', True)
        for url, name, routes in sort_resources(resources):
            if 'include' in routes:
                self.router.include(**routes)
                continue
            resource = self.router.add_resource(url, name=name)
            for method, operation in routes.items():
                handler = operation.pop('handler')
                validate = operation.pop('validate', default_validate)
                if handler.startswith('.'):
                    handler = self.context[handler[1:]]
                elif not is_swagger:
                    handler = import_name(handler)
                if is_swagger:
                    resource.add_route(method.upper(), handler, swagger_data=operation, validate=validate)
                else:
                    resource.add_route(method.upper(), handler)

    def run_forever(self, host=None, port: int=None):
        gconf = self.context.config
        kwargs = {}
        host = host or gconf.http.host
        if host:
            kwargs['host'] = host
        port = port or gconf.http.port
        if port:
            kwargs['port'] = port
        web.run_app(self, **kwargs)

    def make_handler(self, *, loop=None, **kwargs):
        access_log_format = self.config.get('access_log_format')
        if access_log_format:
            kwargs['access_log_format'] = access_log_format
        access_log_class = self.config.get('access_log_class')
        if access_log_class:
            cls = import_name(access_log_class)
            kwargs['access_log_class'] = cls
        return super().make_handler(loop=loop, **kwargs)


def iter_resources(resources, prefix=''):
    if not resources:
        return
    elif not isinstance(resources, dict):
        raise TypeError(
            'Resources should be described in dict %s' % resources)
    prefix += resources.get('prefix', '')
    for name, sub in resources.items():
        if name == 'prefix':
            continue
        elif not isinstance(sub, dict):
            raise TypeError(
                'Resource should be described in dict %s' % sub)
        routes = sub.copy()
        priority = routes.pop('priority', 0)
        if 'include' in routes:
            url = name if name.startswith('/') else None
            if url:
                url = prefix + url
            else:
                url = prefix
            if url:
                routes['prefix'] = url + routes.get('prefix', '')
            yield priority, url or None, name, routes
            continue
        elif not name.startswith('/'):
            for p, u, n, rs in iter_resources(sub, prefix):
                if n:
                    n = ':'.join((name, n))
                yield p, u, n, rs
            continue
        url = name
        name = routes.pop('name', None)
        for k, v in routes.items():
            if 'include' in routes:
                continue
            elif isinstance(v, str):
                routes[k] = {'handler': v}
        yield priority, prefix + url, name, routes


def sort_resources(resources):
    r = sorted(iter_resources(resources), key=lambda x: x[0], reverse=True)
    return map(lambda x: x[1:], r)
