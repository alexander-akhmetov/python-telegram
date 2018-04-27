# [WIP] Python Telegram client

[![Build Status](https://travis-ci.org/alexander-akhmetov/python-telegram.svg?branch=master)](https://travis-ci.org/alexander-akhmetov/python-telegram)
[![PyPI](https://img.shields.io/pypi/v/python-telegram.svg)](https://pypi.python.org/pypi/python-telegram)

Client for the [tdlib](https://github.com/tdlib/td) library (very early stage :) ).
It can receive messages, process them and send some text back for now.

## Installation

Install with pip:

```sh
pip install python-telegram
```

## How to use

Basic example:

```python
    from telegram.client import Telegram


    tg = Telegram(
        api_id=args.api_id,
        api_hash=args.api_hash,
        phone=args.phone,
        library_path='/usr/local/lib/libtdjson.dylib',
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

More examples you can find in `telegram/examples/`.
