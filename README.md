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

This library requires Python 3.8+ and Linux or MacOS.

```shell
pip install python-telegram
```

See [documentation](http://python-telegram.readthedocs.io/en/latest/#installation) for more details.

### Docker

This library has a [docker image](https://hub.docker.com/r/akhmetov/python-telegram/):

```sh
docker run -i -t --rm \
            -v /tmp/docker-python-telegram/:/tmp/ \
            akhmetov/python-telegram \
            python3 /app/examples/send_message.py $(API_ID) $(API_HASH) $(PHONE) $(CHAT_ID) $(TEXT)
```

## How to use

Have a look at the [tutorial](http://python-telegram.readthedocs.io/en/latest/tutorial.html) :)

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

# if this is the first run, library needs to preload all chats
# otherwise the message will not be sent
result = tg.get_chats()
result.wait()

chat_id: int
result = tg.send_message(chat_id, Spoiler('Hello world!'))
# `tdlib` is asynchronous, so `python-telegram` always returns you an `AsyncResult` object.
# You can receive a result with the `wait` method of this object.
result.wait()
print(result.update)

tg.stop()  # you must call `stop` at the end of the script
```

More examples you can find in the [/examples/ directory](/examples/).

---

More information in the [documentation](http://python-telegram.readthedocs.io).

## Development

See [CONTRIBUTING.md](/CONTRIBUTING.md).

### build tdlib

[build from github](https://github.com/tdlib/td#building) and provide path when calling *Telegram* client constructor.

### Add-on to better call the raw tdlib API

to further extend using raw TD-API use [raw_api.py](telegram/raw_api.py).

example: 

~~~python
    from telegram.client import Telegram
    from telegram.raw_api import Location, SearchChatsNearby
    
    tg = Telegram(
        api_id=12345,
        api_hash='api hash from my.telegram.org',
        #phone=cfg['phonenumber'] # if not a bot ...,
        bot_token='bot token from @BotFather',
        files_directory='/path/to/dir/to/mantain/session/',
        database_encryption_key='some secret string',
        library_path='path/to/tdjson_library_compiled_for_your_arch')
    )

    # call searchChatsNearby
    l = Location(1.2345, 6.7890)
    fun = SearchChatsNearby(l)
    res = tg.send_raw_api(fun)
    res.wait()
    # ...
~~~

> further raw api will be added if needed ....