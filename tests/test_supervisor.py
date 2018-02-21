import pytest
import yaml


@pytest.fixture
def config(config):
    config(yaml.load("""
    s:
      cls: aioworkers_aiohttp.supervisor.Supervisor
      ports: 5000-6000
      children: 1
      child:
        shell: false
        cmd: '{python} -m aiohttp.web --port {port}'
    """))
    return config


async def test_conf(context):
    assert context.s.get_child_config()
