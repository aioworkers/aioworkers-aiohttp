#!/usr/bin/env python

from setuptools import setup, find_packages

requirements = [
    'aioworkers>=0.11',
    'aiohttp-apiset>=0.9.1',
]

test_requirements = [
    'pytest',
    'pytest-aiohttp',
]

setup(
    name='aioworkers-aiohttp',
    version='0.4',
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
