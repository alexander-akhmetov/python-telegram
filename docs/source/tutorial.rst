.. _tutorial:

========
Tutorial
========

How to build a simple echo-bot with ``python-telegram``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Install the library:

.. code-block:: bash

     python3 -m pip install python-telegram

Let's create a simple echo-bot that replies "pong" when it receives "ping".

You need an ``api_id`` and an ``api_hash``. Get them by registering a new application at `my.telegram.org/apps <https://my.telegram.org/apps/>`_.

Initialize a new Telegram client with your credentials:

.. code-block:: python

    from telegram.client import Telegram

    tg = Telegram(
        api_id=123456,
        api_hash='api_hash',
        phone='+31611111111',
        database_encryption_key='changeme1234',
    )

.. note::
    By default, the library tells ``tdlib`` to store the message database and the downloaded files in a temporary directory,
    ``/tmp/.tdlib_files/<md5 of your phone number or bot token>/``.
    Pass the ``files_directory`` parameter to store them somewhere else.
    Use it if you want to keep the database between runs, because most systems clean up ``/tmp``.

.. note::
    To sign in as a bot, pass ``bot_token`` instead of ``phone``.

Now you need to log in. Call the ``login`` method:

.. code-block:: python

    tg.login()

This example uses the blocking version of ``login``. For an example of non-blocking usage, see :ref:`non_blocking_login`.
Telegram sends you a code, either as an SMS or as a Telegram message. If you have two-factor authentication enabled, you are asked for your password as well.
After you sign in, you can start using the library:

.. code-block:: python

    # This function will be called for each received message.
    def new_message_handler(update):
        print('New message!')

    tg.add_message_handler(new_message_handler)
    tg.idle()  # Blocking, waiting for CTRL+C.

This code adds a message handler that prints a line every time the client receives a new message.
``tg.idle()`` is necessary to block the script and wait for an exit signal (``CTRL+C``).

If you run this code, you see something like this:

.. code-block:: sh

    New message!
    New message!

Let's add more logic to the message handler:

.. code-block:: python

    def new_message_handler(update):
        # We want to process only text messages.
        message_content = update['message']['content'].get('text', {})
        message_text = message_content.get('text', '').lower()
        is_outgoing = update['message']['is_outgoing']

        if not is_outgoing and message_text == 'ping':
            chat_id = update['message']['chat_id']
            print(f'Ping has been received from {chat_id}')
            tg.send_message(
                chat_id=chat_id,
                text='pong',
            )

Full code of our new bot:

.. code-block:: python

    from telegram.client import Telegram

    tg = Telegram(
        api_id=123456,
        api_hash='api_hash',
        phone='+31611111111',
        database_encryption_key='changeme1234',
    )
    tg.login()

    def new_message_handler(update):
        # We want to process only text messages.
        message_content = update['message']['content'].get('text', {})
        message_text = message_content.get('text', '').lower()
        is_outgoing = update['message']['is_outgoing']

        if not is_outgoing and message_text == 'ping':
            chat_id = update['message']['chat_id']
            print(f'Ping has been received from {chat_id}')
            tg.send_message(
                chat_id=chat_id,
                text='pong',
            )

    tg.add_message_handler(new_message_handler)
    tg.idle()

Done! You have written your first Telegram client.

idle and stop
-------------

You must call ``stop`` to shut down ``python-telegram`` and ``tdlib`` cleanly.
It calls the ``close`` method of ``tdlib`` and waits until it has finished.

``idle`` blocks until you call ``stop`` from another thread, or until the process receives one of the stop signals.
By default these are ``SIGINT``, ``SIGTERM`` and ``SIGABRT``; you can change them with the ``stop_signals`` parameter.
When one of them arrives, ``idle`` calls ``stop`` for you, which is why the example above does not call it directly.
