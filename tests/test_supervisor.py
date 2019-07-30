import pytest


@pytest.fixture
def config_yaml():
    return """
    s:
      cls: aioworkers_aiohttp.supervisor.Supervisor
      ports: 5000-6000
      children: 1
      child:
        shell: false
        cmd: '{python} -m aiohttp.web --port {port}'
    """


async def test_conf(context):
    assert context.s.get_child_config()
