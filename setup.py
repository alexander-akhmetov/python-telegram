#!/usr/bin/env python
import os
import re
from distutils.core import setup


def get_version(package):
    """
    Returns version of a package (`__version__` in `init.py`).
    """
    init_py = open(os.path.join(package, '__init__.py')).read()
    return re.match("__version__ = ['\"]([^'\"]+)['\"]", init_py).group(1)


version = get_version('telegram')


setup(
    name='python-telegram',
    version=version,
    description='Python library to help you build your own Telegram clients',
    author='Alexander Akhmetov',
    author_email='me@aleks.sh',
    url='https://github.com/alexander-akhmetov/python-telegram',
    long_description=open(os.path.join(os.path.dirname(__file__), 'README.md')).read(),
    packages=[
        'telegram',
    ],
    package_data={
        'telegram': [
            'lib/darwin/*',
            'lib/linux/*',
        ],
    },
    install_requires=[
        'telegram-text>=0.1.1',
    ],
)
