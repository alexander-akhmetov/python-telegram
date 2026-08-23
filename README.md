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

This library requires Python 3.10+. Windows is not supported.

```shell
pip install python-telegram
```

See [documentation](https://python-telegram.readthedocs.io/latest/#installation) for more details.

### tdlib

Four wheels bundle a `tdlib` binary. Each one works on Python 3.10 through 3.14:

| Platform | Wheel | Needs at least |
| --- | --- | --- |
| Linux x86_64 | `manylinux_2_28_x86_64` | glibc 2.28 |
| Linux aarch64 | `manylinux_2_28_aarch64` | glibc 2.28 |
| macOS arm64 | `macosx_11_0_arm64` | macOS 11 |
| macOS x86_64 | `macosx_10_15_x86_64` | macOS 10.15 |

Those binaries link OpenSSL and zlib statically, so they need nothing from the system.

Anywhere else, pip installs the source distribution, which carries no binary. On musl, on
32-bit ARM, or with an older glibc, [compile](https://tdlib.github.io/td/build.html) `tdlib`
yourself.

`python-telegram` looks for the library in this order, and logs which one it used:

1. the `library_path` argument
2. the `PYTHON_TELEGRAM_TDLIB_PATH` environment variable
3. a system-wide `tdjson`
4. the bundled binary

A system-wide `tdlib` therefore wins over the bundled one. To point at a specific build,
pass its path. The file is called `libtdjson.so` on Linux and `libtdjson.dylib` on macOS:

```python
tg = Telegram(
    # ...
    library_path="/usr/local/lib/libtdjson.so",
)
```

If nothing can be found, `TDJson()` raises `TDLibNotFoundError`, an `OSError` subclass whose
message names the platform, the paths tried and the overrides.

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

# The chat must be in the tdlib database before you can send a message to it.
# `get_chats` loads up to `limit` chats from the main chat list.
result = tg.get_chats(limit=100)
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
