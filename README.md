# python-telegram

[![Build Status](https://github.com/alexander-akhmetov/python-telegram/workflows/python-telegram%20tests/badge.svg)](https://github.com/alexander-akhmetov/python-telegram/actions)
[![PyPI](https://img.shields.io/pypi/v/python-telegram.svg)](https://pypi.python.org/pypi/python-telegram)
[![DockerHub](https://img.shields.io/docker/automated/akhmetov/python-telegram.svg)](https://hub.docker.com/r/akhmetov/python-telegram/)
![Read the Docs (version)](https://img.shields.io/readthedocs/pip/stable.svg)

Python API for the [tdlib](https://github.com/tdlib/td) library.
It helps you build your own Telegram clients.

- [Changelog](https://python-telegram.readthedocs.io/en/latest/changelog.html)
- [Documentation](http://python-telegram.readthedocs.io)
- [Tutorial](http://python-telegram.readthedocs.io/en/latest/tutorial.html)

## Installation

This library requires Python 3.9+ and Linux or MacOS. Windows is not supported.

```shell
pip install python-telegram
```

See [documentation](http://python-telegram.readthedocs.io/en/latest/#installation) for more details.

### tdlib

`python-telegram` comes with a precompiled `tdlib` library for Linux and MacOS. But it is highly recommended to [compile](https://tdlib.github.io/td/build.html) it yourself.
The precompiled library may not work on some systems, it is dynamically linked and requires specific versions of additional libraries.

```shell

### Docker

This library has a [docker image](https://hub.docker.com/r/akhmetov/python-telegram/):

```sh
docker run -i -t --rm \
            -v /tmp/docker-python-telegram/:/tmp/ \
            akhmetov/python-telegram \
            python3 /app/examples/send_message.py $(API_ID) $(API_HASH) $(PHONE) $(CHAT_ID) $(TEXT)
```

## How to use the library

Check out the [tutorial](http://python-telegram.readthedocs.io/en/latest/tutorial.html) for more details.

Basic example:

```python
from telegram.client import Telegram
from telegram.text import Spoiler

tg = Telegram(
    api_id='api_id',
    api_hash='api_hash',
    phone='+31611111111',  # you can pass 'bot_token' instead
    database_encryption_key='changekey123',
    files_directory='/tmp/.tdlib_files/',
)
tg.login()

# If this is the first run, the library needs to preload all chats.
# Otherwise, the message will not be sent.
result = tg.get_chats()
result.wait()

chat_id: int
result = tg.send_message(chat_id, Spoiler('Hello world!'))

# `tdlib` is asynchronous, so `python-telegram` always returns an `AsyncResult` object.
# You can receive a result with the `wait` method of this object.
result.wait()
print(result.update)

tg.stop()  # You must call `stop` at the end of the script.
```

You can also use `call_method` to call any [tdlib method](https://core.telegram.org/tdlib/docs/classtd_1_1td__api_1_1_function.html):

``` python
tg.call_method('getUser',  params={'user_id': user_id})
```

More examples can be found in the [/examples/ directory](/examples/).

---

More information is available in the [documentation](http://python-telegram.readthedocs.io).

## Development

See [CONTRIBUTING.md](/CONTRIBUTING.md).
