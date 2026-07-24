Welcome to python-telegram's documentation
===========================================

|build-status| |pypi|

.. toctree::
   :maxdepth: 1

   tutorial
   non_blocking_login
   telegram
   tdlib
   proxy
   changelog

Client for the `tdlib <https://github.com/tdlib/td>`_ library.

``tdlib`` connects to Telegram over MTProto, the same protocol the official apps use.
This library signs in as a full Telegram account with a phone number, and it can do what a regular client can do.

It is not a wrapper around the HTTP Bot API.
If you only need a bot, `python-telegram-bot <https://github.com/python-telegram-bot/python-telegram-bot>`_ is a better fit.
You can still sign in as a bot here by passing ``bot_token`` instead of ``phone``.

Installation
------------

This library requires Python 3.9 or higher, and Linux or macOS. Windows is not supported.

.. code-block:: bash

     python3 -m pip install python-telegram

Next, `register <https://my.telegram.org/apps/>`_ a new Telegram application to get an ``api_id`` and an ``api_hash``.

Now you can start using the library: :ref:`tutorial`.

.. note::
    More examples can be found `here <https://github.com/alexander-akhmetov/python-telegram/tree/main/examples>`_.

tdlib
~~~~~

``python-telegram`` comes with a precompiled ``tdlib`` binary for Linux and macOS, so it works without any extra steps.
That binary is dynamically linked and needs specific versions of other system libraries, so it does not work everywhere.
Building ``tdlib`` yourself is more reliable. See the `official build instructions <https://github.com/tdlib/td#building>`_,
and do not forget to install it afterwards:

.. code-block:: bash

    make install

If ``tdlib`` is installed system-wide, ``python-telegram`` finds it automatically.
Otherwise, pass the path to the compiled library.
The file is called ``libtdjson.so`` on Linux and ``libtdjson.dylib`` on macOS:

.. code-block:: python

    from telegram.client import Telegram

    tg = Telegram(
        # ...
        library_path='/usr/local/lib/libtdjson.so',
    )

.. note::
    Since version ``0.10.0``, the ``tdlib`` binary for Linux that comes with ``python-telegram`` is built on Ubuntu against ``glibc``. Earlier versions were built on Alpine Linux against ``musl``.

Docker
------

A Docker image for this library is available `here <https://hub.docker.com/r/akhmetov/python-telegram/>`_

.. code-block:: bash

    docker run -i -t --rm \
                -v /tmp/docker-python-telegram/:/tmp/ \
                akhmetov/python-telegram \
                python3 /app/examples/send_message.py $API_ID $API_HASH $PHONE $CHAT_ID $TEXT


.. |build-status| image:: https://github.com/alexander-akhmetov/python-telegram/workflows/python-telegram%20tests/badge.svg
    :alt: build status
    :target: https://github.com/alexander-akhmetov/python-telegram/actions

.. |pypi| image:: https://img.shields.io/pypi/v/python-telegram.svg
    :alt: pypi package
    :target: https://pypi.org/project/python-telegram/
