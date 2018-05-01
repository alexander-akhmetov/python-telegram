# [WIP] Python Telegram client

[![Build Status](https://travis-ci.org/alexander-akhmetov/python-telegram.svg?branch=master)](https://travis-ci.org/alexander-akhmetov/python-telegram)
[![PyPI](https://img.shields.io/pypi/v/python-telegram.svg)](https://pypi.python.org/pypi/python-telegram)
[![DockerHub](https://img.shields.io/docker/automated/akhmetov/python-telegram.svg)](https://hub.docker.com/r/akhmetov/python-telegram/)
![Read the Docs (version)](https://img.shields.io/readthedocs/pip/stable.svg)

Client for the [tdlib](https://github.com/tdlib/td) library (very early stage :) ).
It can receive messages, process them and send some text back for now.

[Changelog](docs/source/changelog.rst)
[Documentation](http://python-telegram.readthedocs.io)

## Installation

Install with pip:

```sh
pip install python-telegram
```

## How to use

You have to build tdlib and install it. Or you can use it with [docker](https://github.com/alexander-akhmetov/tdlib-docker).
Also, you need to register a new [telegram app](http://my.telegram.org/apps/) to get `API_ID` and `API_HASH`.

### How to build tdlib

[Official documentation](https://github.com/tdlib/td#building)

Do not forget install the library after:

```sh
make install
```

### How to use this library

Basic example:

```python
    from telegram.client import Telegram


    tg = Telegram(
        api_id=args.api_id,
        api_hash=args.api_hash,
        phone=args.phone,
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
    # You can wait for a result with `wait` method.
    result.wait()
```

More examples you can find in `/examples/`.

### Docker

Try to use docker if you don't want to build tdlib:

```sh
API_ID=your_id API_HASH=your_hash PHONE=+123 CHAT_ID=chat_id TEXT='Hello world' make docker-send-message
```

It will start pre-built docker container with `tdlib` and `python-telegram` inside.
