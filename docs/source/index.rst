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

This library requires Python 3.10 or higher. Windows is not supported.

.. code-block:: bash

     python3 -m pip install python-telegram

Next, `register <https://my.telegram.org/apps/>`_ a new Telegram application to get an ``api_id`` and an ``api_hash``.

Now you can start using the library: :ref:`tutorial`.

.. note::
    More examples can be found `here <https://github.com/alexander-akhmetov/python-telegram/tree/main/examples>`_.

tdlib
~~~~~

Four wheels bundle a ``tdlib`` binary. Each one works on Python 3.10 through 3.14:

.. list-table::
   :header-rows: 1

   * - Platform
     - Wheel
     - Needs at least
   * - Linux x86_64
     - ``manylinux_2_28_x86_64``
     - glibc 2.28
   * - Linux aarch64
     - ``manylinux_2_28_aarch64``
     - glibc 2.28
   * - macOS arm64
     - ``macosx_11_0_arm64``
     - macOS 11
   * - macOS x86_64
     - ``macosx_10_15_x86_64``
     - macOS 10.15

Those binaries link OpenSSL and zlib statically, so they need nothing from the system.

Anywhere else, pip installs the source distribution, which carries no binary. On musl, on
32-bit ARM, or with a glibc older than 2.28, build ``tdlib`` yourself. See the
`official build instructions <https://github.com/tdlib/td#building>`_, and do not forget to
install it afterwards:

.. code-block:: bash

    make install

``python-telegram`` looks for the library in this order, and logs which one it used:

1. the ``library_path`` argument
2. the ``PYTHON_TELEGRAM_TDLIB_PATH`` environment variable
3. a system-wide ``tdjson``, through ``ctypes.util.find_library``
4. the binary bundled in the wheel

A system-wide ``tdlib`` therefore wins over the bundled one.
To point at a specific build, pass its path.
The file is called ``libtdjson.so`` on Linux and ``libtdjson.dylib`` on macOS:

.. code-block:: python

    from telegram.client import Telegram

    tg = Telegram(
        # ...
        library_path='/usr/local/lib/libtdjson.so',
    )

If nothing can be found, ``TDJson()`` raises ``TDLibNotFoundError``, an ``OSError`` subclass
whose message names the platform, the paths tried and the overrides.

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
