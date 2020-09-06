from collections import Mapping

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
            cfg = dict(config.router)
            cls = import_name(cfg.pop('cls'))
            cors = cfg.pop('cors', None)
            kwargs['router'] = cls(**cfg)

        if not config.get('middlewares'):
            pass
        elif isinstance(config.middlewares, list):
            kwargs['middlewares'] = map(
                self.context.get_object, config.middlewares,
            )
        else:
            raise TypeError('Middlewares should be described in list')

        super().__init__(**kwargs)

        if cors is not None:
            kwargs['router'].set_cors(self, **cors)

        for signal in (
            'on_startup', 'cleanup_ctx',
            'on_cleanup', 'on_response_prepare',
        ):
            sigs = config.get(signal)
            signals = getattr(self, signal, None)
            if sigs and signals is not None:
                for _, s in sorted(sigs.items(), key=lambda x: x[0]):
                    coro = self.context.get_object(s)
                    signals.append(coro)

    async def init(self):
        for routes_line in self.config.get('routes') or ():
            routes = self.context.get_object(routes_line)
            if isinstance(routes, web.AbstractRouteDef):
                self.add_routes([routes])
            else:
                self.add_routes(routes)
        resources = self.config.get('resources')
        is_swagger = isinstance(self.router, AbstractSwaggerRouter)
        default_validate = self.config.get('router.default_validate', True)
        for url, name, routes in sort_resources(resources):
            if 'include' in routes:
                self.router.include(**routes)
                continue
            if 'static' in routes:
                static_params = routes.pop('static')
                if isinstance(static_params, Mapping):
                    kwargs = static_params
                else:
                    kwargs = {'path': static_params}
                self.router.add_static(url, **kwargs)
            resource = self.router.add_resource(url, name=name)
            for method, operation in routes.items():
                if not isinstance(operation, Mapping):
                    raise TypeError(
                        'operation for {method} {url} expected Mapping, '
                        'not {t}'.format(
                            method=method.upper(), url=url, t=type(operation),
                        )
                    )
                operation = dict(operation)
                handler = operation.pop('handler')
                validate = operation.pop('validate', default_validate)
                if not is_swagger or handler.startswith('.'):
                    handler = self.context.get_object(handler)
                if is_swagger:
                    resource.add_route(
                        method.upper(), handler,
                        swagger_data=operation, validate=validate,
                    )
                else:
                    resource.add_route(method.upper(), handler)


def iter_resources(resources, prefix=''):
    if not resources:
        return
    elif not isinstance(resources, Mapping):
        raise TypeError(
            'Resources should be described in dict %s' % resources)
    prefix += resources.get('prefix', '')
    for name, sub in resources.items():
        if name == 'prefix':
            continue
        elif not isinstance(sub, Mapping):
            raise TypeError(
                'Resource should be described in dict %s' % sub)
        routes = dict(sub)
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
            elif 'static' in routes:
                continue
            elif isinstance(v, str):
                routes[k] = {'handler': v}
        yield priority, prefix + url, name, routes


def sort_resources(resources):
    r = sorted(iter_resources(resources), key=lambda x: x[0], reverse=True)
    return map(lambda x: x[1:], r)
