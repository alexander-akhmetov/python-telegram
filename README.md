# python-telegram

[![Build Status](https://travis-ci.org/alexander-akhmetov/python-telegram.svg?branch=master)](https://travis-ci.org/alexander-akhmetov/python-telegram)
![Build Status](https://github.com/alexander-akhmetov/python-telegram/workflows/.github/workflows/tests.yml/badge.svg)
[![PyPI](https://img.shields.io/pypi/v/python-telegram.svg)](https://pypi.python.org/pypi/python-telegram)
[![DockerHub](https://img.shields.io/docker/automated/akhmetov/python-telegram.svg)](https://hub.docker.com/r/akhmetov/python-telegram/)
![Read the Docs (version)](https://img.shields.io/readthedocs/pip/stable.svg)

Python API for the [tdlib](https://github.com/tdlib/td) library.
It helps you build your own Telegram clients.

* [Changelog](docs/source/changelog.rst)
* [Documentation](http://python-telegram.readthedocs.io)
* [Tutorial](http://python-telegram.readthedocs.io/en/latest/tutorial.html)

## Installation

This library works with Python 3.6+ only.

```shell
pip install python-telegram
```

See [documentation](http://python-telegram.readthedocs.io/en/latest/#installation) for more details.

### Docker

This library has [docker image](https://hub.docker.com/r/akhmetov/python-telegram/):

```sh
docker run -i -t --rm \
            -v /tmp/docker-python-telegram/:/tmp/ \
            akhmetov/python-telegram \
            python3 /app/examples/send_message.py $(API_ID) $(API_HASH) $(PHONE) $(CHAT_ID) $(TEXT)
```

## How to use

Check the [tutorial](http://python-telegram.readthedocs.io/en/latest/tutorial.html) :)

Basic example:

```python
    from telegram.client import Telegram

    tg = Telegram(
        api_id='api_id',
        api_hash='api_hash',
        phone='+31611111111',  # you can pass 'bot_token' instead
        database_encryption_key='changekey123',
    )
    tg.login()

    # if this is the first run, library needs to preload all chats
    # otherwise the message will not be sent
    result = tg.get_chats()
    result.wait()

    result = tg.send_message(
        chat_id=args.chat_id,
        text=args.text,
    )
    # `tdlib` is asynchronous, so `python-telegram` always returns you an `AsyncResult` object.
    # You can receive a result with the `wait` method of this object.
    result.wait()
    print(result.update)
```

More examples you can find in the [/examples/ directory](/examples/).

----

More information in the [documentation](http://python-telegram.readthedocs.io).

## Development

### Tests

To run tests you need to install [tox](https://tox.readthedocs.io/en/latest/) first.

Start tests:

```shell
tox
```

Run a specific test for python3.7:

```shell
tox -e py37 -- tests/test_telegram_methods.py::TestTelegram::test_add_message_handler
```
