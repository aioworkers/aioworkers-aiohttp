import argparse

from aioworkers_aiohttp import plugin


def test_plugin_add_argument(context):
    parser = argparse.ArgumentParser()
    p = plugin()
    p.add_arguments(parser)
    p.add_arguments(parser)


def test_plugin_port(context):
    parser = argparse.ArgumentParser()
    p = plugin()
    p.add_arguments(parser)
    p.parse_known_args([], parser.parse_args(["--port", "9090"]))
