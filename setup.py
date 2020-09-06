import re
from pathlib import Path

from setuptools import find_packages, setup


requirements = [
    'aioworkers>=0.13.0',
    'aiohttp>=3.1',
    'aiohttp-apiset>=0.9.6',
]

test_requirements = [
    'pytest',
    'pytest-aioworkers',
    'pytest-mock',
]

pkg = 'aioworkers_aiohttp'


def read(f):
    path = Path(__file__).parent / f
    if not path.exists():
        return ''
    return path.read_text(encoding='latin1').strip()


def get_version():
    text = read(pkg + '/version.py')
    if not text:
        text = read(pkg + '/__init__.py')
    try:
        return re.findall(r"__version__ = '([^']+)'$", text, re.M)[0]
    except IndexError:
        raise RuntimeError('Unable to determine version.')


setup(
    name='aioworkers-aiohttp',
    version=get_version(),
    description="",
    author="Alexander Malev",
    author_email='yttrium@somedev.ru',
    url='https://github.com/aioworkers/aioworkers-aiohttp',
    packages=find_packages(include=[pkg]),
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
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    test_suite='tests',
    tests_require=test_requirements,
)
