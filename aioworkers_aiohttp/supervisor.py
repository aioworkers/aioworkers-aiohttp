from collections import Mapping

from aioworkers.worker import subprocess, supervisor
from aioworkers import utils


class Supervisor(supervisor.Supervisor):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._iterport = self.gen_port(self.config.ports)

    def gen_port(self, ports):
        last_port = 65535
        if isinstance(ports, Mapping):
            first_port = ports['first']
        elif isinstance(ports, str):
            p = map(lambda x: int(x.strip()), ports.split('-', 1))
            first_port = next(p)
            last_port = next(p, last_port)
        elif isinstance(ports, int):
            first_port = ports
        else:
            raise ValueError('Error value for ports {}'.format(ports))
        return iter(range(first_port, last_port))

    def get_child_config(self):
        c = super().get_child_config()
        params = c.get('params') or {}
        if params:
            params = dict(params)
        params['port'] = next(self._iterport)
        cls = c.get('cls') or utils.import_uri(subprocess.Subprocess)
        c = c.new_child(params=params, daemon=True, cls=cls)
        return c
