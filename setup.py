#!/usr/bin/env python

from setuptools import setup, find_packages

version = __import__('aioworkers_aiohttp').__version__

requirements = [
    'aioworkers>=0.13.0',
    'aiohttp-apiset>=0.9.6',
]

test_requirements = [
    'pytest',
    'pytest-aiohttp',
]

setup(
    name='aioworkers-aiohttp',
    version=version,
    description="",
    author="Alexander Malev",
    author_email='yttrium@somedev.ru',
    url='https://github.com/aioworkers/aioworkers-aiohttp',
    packages=[i for i in find_packages() if i.startswith('aioworkers_aiohttp')],
    include_package_data=True,
    install_requires=requirements,
    license="Apache Software License 2.0",
    keywords='aioworkers aiohttp',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    test_suite='tests',
    tests_require=test_requirements,
)
