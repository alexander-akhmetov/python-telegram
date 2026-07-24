# python-telegram

[![Build Status](https://github.com/alexander-akhmetov/python-telegram/workflows/python-telegram%20tests/badge.svg)](https://github.com/alexander-akhmetov/python-telegram/actions)
[![PyPI](https://img.shields.io/pypi/v/python-telegram.svg)](https://pypi.python.org/pypi/python-telegram)
[![Read the Docs](https://img.shields.io/readthedocs/python-telegram/latest.svg)](https://python-telegram.readthedocs.io/latest/)

Python API for the [tdlib](https://github.com/tdlib/td) library.
It helps you build your own Telegram clients.

`tdlib` connects to Telegram over MTProto, the same protocol the official apps use.
This library signs in as a full Telegram account with a phone number, and it can do what a regular client can do.

It is not a wrapper around the HTTP Bot API.
If you only need a bot, [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) is a better fit.
You can still sign in as a bot here by passing `bot_token` instead of `phone`.

- [Changelog](https://python-telegram.readthedocs.io/latest/changelog.html)
- [Documentation](https://python-telegram.readthedocs.io/latest/)
- [Tutorial](https://python-telegram.readthedocs.io/latest/tutorial.html)

## Installation

This library requires Python 3.9+ and Linux or MacOS. Windows is not supported.

```shell
pip install python-telegram
```

See [documentation](https://python-telegram.readthedocs.io/latest/#installation) for more details.

### tdlib

`python-telegram` comes with a precompiled `tdlib` library for Linux and MacOS. But it is highly recommended to [compile](https://tdlib.github.io/td/build.html) it yourself.
The precompiled library may not work on some systems, it is dynamically linked and requires specific versions of additional libraries.

If you installed `tdlib` system-wide, `python-telegram` finds it automatically.
Otherwise, pass the path to the compiled library. The file is called `libtdjson.so` on Linux and `libtdjson.dylib` on MacOS:

```python
tg = Telegram(
    # ...
    library_path="/usr/local/lib/libtdjson.so",
)
```

### Docker

This library has a [docker image](https://hub.docker.com/r/akhmetov/python-telegram/):

```sh
docker run -i -t --rm \
            -v /tmp/docker-python-telegram/:/tmp/ \
            akhmetov/python-telegram \
            python3 /app/examples/send_message.py $API_ID $API_HASH $PHONE $CHAT_ID $TEXT
```

## How to use the library

First, [register a new Telegram application](https://my.telegram.org/apps/) to get your `api_id` and `api_hash`.
Check out the [tutorial](https://python-telegram.readthedocs.io/latest/tutorial.html) for more details.

Basic example:

```python
from telegram.client import Telegram
from telegram.text import Spoiler

tg = Telegram(
    api_id=123456,
    api_hash="api_hash",
    phone="+31611111111",  # you can pass 'bot_token' instead
    database_encryption_key="changekey123",
    files_directory="/tmp/.tdlib_files/",
)
tg.login()

# If this is the first run, the library needs to preload all chats.
# Otherwise, the message will not be sent.
result = tg.get_chats()
result.wait()

chat_id = 123456789
result = tg.send_message(chat_id, Spoiler("Hello world!"))

# `tdlib` is asynchronous, so `python-telegram` always returns an `AsyncResult` object.
# You can receive a result with the `wait` method of this object.
result.wait()
print(result.update)

tg.stop()  # You must call `stop` at the end of the script.
```

You can also use `call_method` to call any [tdlib method](https://core.telegram.org/tdlib/docs/classtd_1_1td__api_1_1_function.html):

```python
tg.call_method("getUser", params={"user_id": user_id})
```

More examples can be found in the [/examples/ directory](/examples/).

---

More information is available in the [documentation](https://python-telegram.readthedocs.io/latest/).

## Development

See [CONTRIBUTING.md](/CONTRIBUTING.md).
