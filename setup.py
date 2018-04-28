#!/usr/bin/env python
import os
import re
import sys
from distutils.core import setup


def get_version(package):
    """
    Return package version as listed in `__version__` in `init.py`.
    """
    init_py = open(os.path.join(package, '__init__.py')).read()
    return re.match("__version__ = ['\"]([^'\"]+)['\"]", init_py).group(1)


version = get_version('telegram')


if sys.argv[-1] == 'publish':
    os.system("python setup.py sdist upload")
    os.system("python setup.py bdist_wheel upload")
    print("You probably want to also tag the version now:")
    print("  git tag -a %s -m 'version %s'" % (version, version))
    print("  git push --tags")
    sys.exit()


setup(
    name='python-telegram',
    version=version,
    description='Python library to interact with Telegram\'s tdlib (https://github.com/tdlib/td)',
    author='Aleksandr Akhmetov',
    author_email='me@aleks.sh',
    url='https://github.com/alexander-akhmetov/python-telegram',
    packages=[
        'telegram',
    ],
)
