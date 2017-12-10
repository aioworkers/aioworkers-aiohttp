from pathlib import Path

from aiohttp_apiset import SwaggerRouter
from aioworkers.utils import import_name


class Router(SwaggerRouter):
    def __init__(self, search_in_modules=(), search_dirs=(), **kwargs):
        modules = map(import_name, search_in_modules)
        dirs = [Path(x.__file__).parent for x in modules]
        dirs.extend(search_dirs)
        kwargs['search_dirs'] = dirs
        super().__init__(**kwargs)

    def include(self, include, *,
                base=None,
                mapping=None,
                name=None):

        return super().include(
            include, basePath=base,
            operationId_mapping=mapping,
            name=name)
