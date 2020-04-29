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


version = get_version('python_telegram')


setup(
    name='python-telegram',
    version=version,
    description='Python library to help you build your own Telegram clients',
    author='Alexander Akhmetov',
    author_email='me@aleks.sh',
    url='https://github.com/alexander-akhmetov/python-telegram',
    packages=[
        'python_telegram',
    ],
    package_data={
        'python_telegram': [
            'lib/darwin/*',
            'lib/linux/*',
        ],
    },
)
