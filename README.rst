aioworkers-aiohttp
==================

The package to integration aioworkers with aiohttp

.. image:: https://img.shields.io/pypi/v/aioworkers-aiohttp.svg
  :target: https://pypi.org/project/aioworkers-aiohttp

.. image:: https://github.com/aioworkers/aioworkers-aiohttp/workflows/Tests/badge.svg
  :target: https://github.com/aioworkers/aioworkers-aiohttp/actions?query=workflow%3ATests

.. image:: https://codecov.io/gh/aioworkers/aioworkers-aiohttp/branch/master/graph/badge.svg
  :target: https://codecov.io/gh/aioworkers/aioworkers-aiohttp
  :alt: Coverage

.. image:: https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v0.json
  :target: https://github.com/charliermarsh/ruff
  :alt: Code style: ruff

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
  :target: https://github.com/psf/black
  :alt: Code style: black

.. image:: https://img.shields.io/badge/types-Mypy-blue.svg
  :target: https://github.com/python/mypy
  :alt: Code style: Mypy

.. image:: https://readthedocs.org/projects/aioworkers-aiohttp/badge/?version=latest
  :target: https://github.com/aioworkers/aioworkers-aiohttp#readme
  :alt: Documentation Status

.. image:: https://img.shields.io/pypi/pyversions/aioworkers-aiohttp.svg
  :target: https://pypi.org/project/aioworkers-aiohttp
  :alt: Python versions

.. image:: https://img.shields.io/pypi/dm/aioworkers-aiohttp.svg
  :target: https://pypi.org/project/aioworkers-aiohttp

.. image:: https://img.shields.io/badge/%F0%9F%A5%9A-Hatch-4051b5.svg
  :alt: Hatch project
  :target: https://github.com/pypa/hatch


Features
--------

- Building of the routing from config like swagger
- Start aiohttp project with multiprocessing mode

Example
-------

.. code-block:: yaml

  http:
    port: 8080
    access_log:
      format: %a %t "%r" %s %b "%{Referer}i" "%{User-Agent}i"

  app:
    routes:
      - mymodule.route_table
      - mymodule.route
    resources:
      /html:
        static: static/html
      /css:
        static:
          path: static/css
      api:
        prefix: /api
        pets:
          /pet/{pet_id}:
            get:
              tags: [Pet]
              handler: mymodule.mycoro
              description: Info about pet
              parameters:
                - name: pet_id
                  in: path
                  type: integer
                  minimum: 0
              responses:
                200:
                  description: OK
                400:
                  description: Validation error
                404:
                  description: Not found


Development
-----------

Check code:

.. code-block:: shell

    hatch run lint:all


Format code:

.. code-block:: shell

    hatch run lint:fmt


Run tests:

.. code-block:: shell

    hatch run pytest


Run tests with coverage:

.. code-block:: shell

    hatch run cov
