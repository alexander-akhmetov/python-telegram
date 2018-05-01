# [WIP] Python Telegram client

[![Build Status](https://travis-ci.org/alexander-akhmetov/python-telegram.svg?branch=master)](https://travis-ci.org/alexander-akhmetov/python-telegram)
[![PyPI](https://img.shields.io/pypi/v/python-telegram.svg)](https://pypi.python.org/pypi/python-telegram)
[![DockerHub](https://img.shields.io/docker/automated/akhmetov/python-telegram.svg)](https://hub.docker.com/r/akhmetov/python-telegram/)
![Read the Docs (version)](https://img.shields.io/readthedocs/pip/stable.svg)

Client for the [tdlib](https://github.com/tdlib/td) library (very early stage :) ).
If helps you build your own Telegram clients.

* [Changelog](docs/source/changelog.rst)
* [Documentation](http://python-telegram.readthedocs.io)
* [Tutorial](http://python-telegram.readthedocs.io/en/latest/tutorial.html)

## Installation

Install with pip:

```sh
pip install python-telegram
```

## How to use

This package already contains [pre-built tdlib](https://github.com/tdlib/td#building).
And you must register a new [telegram app](http://my.telegram.org/apps/) to get `API_ID` and `API_HASH`.

### How to use this library

Check the [tutorial](http://python-telegram.readthedocs.io/en/latest/tutorial.html) :)

Basic example:

```python
    from telegram.client import Telegram

    tg = Telegram(
        api_id='api_id',
        api_hash='api_hash',
        phone='+31611111111',
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

### Docker

This library has [docker image](https://hub.docker.com/r/akhmetov/python-telegram/):

```sh
docker run -i -t --rm \
            -v /tmp/docker-python-telegram/:/tmp/ \
            akhmetov/python-telegram \
            python3 /app/examples/send_message.py $(API_ID) $(API_HASH) $(PHONE) $(CHAT_ID) $(TEXT)
```

----

More information in the [documentation](http://python-telegram.readthedocs.io).
