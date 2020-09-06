import json
from contextlib import suppress
from json import JSONDecodeError

from aiohttp.abc import AbstractAccessLogger


class DebugAccessLogClass(AbstractAccessLogger):
    def log(self, request, response, time):
        data = ''
        with suppress(JSONDecodeError, UnicodeDecodeError):
            data = response.body.decode()
            data = json.dumps(json.loads(data), indent=2, ensure_ascii=False)
        self.logger.info(
            f'{request.remote} {request.method} {request.path} - {response.status}\n'
            f'{data[:100]}\n'
        )
