aioworkers-aiohttp
==================

The package to integration aioworkers with aiohttp

.. image:: https://github.com/aioworkers/aioworkers-aiohttp/workflows/Tests/badge.svg
  :target: https://github.com/aioworkers/aioworkers-aiohttp/actions?query=workflow%3ATests

.. image:: https://codecov.io/gh/aioworkers/aioworkers-aiohttp/branch/master/graph/badge.svg
  :target: https://codecov.io/gh/aioworkers/aioworkers-aiohttp

.. image:: https://img.shields.io/pypi/v/aioworkers-aiohttp.svg
  :target: https://pypi.python.org/pypi/aioworkers-aiohttp

.. image:: https://pyup.io/repos/github/aioworkers/aioworkers-aiohttp/shield.svg
  :target: https://pyup.io/repos/github/aioworkers/aioworkers-aiohttp/
  :alt: Updates

.. image:: https://readthedocs.org/projects/aioworkers-aiohttp/badge/?version=latest
  :target: http://aioworkers-aiohttp.readthedocs.io/en/latest/?badge=latest
  :alt: Documentation Status

.. image:: https://img.shields.io/pypi/pyversions/aioworkers-aiohttp.svg
  :target: https://pypi.python.org/pypi/aioworkers-aiohttp


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
  logging:
    version: 1
    formatters:
      access:
        format: %a %t "%r" %s %b "%{Referer}i" "%{User-Agent}i"
