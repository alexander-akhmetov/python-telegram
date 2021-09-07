.. _tutorial:

========
Tutorial
========

How to build a simple echo-bot with ``python-telegram``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Install the library:

.. code-block:: bash

     python3 -m pip install python-telegram

Let's create a simple echo-bot, which sends "pong" when it receives "ping".

Initialize a new telegram client with your credentials:

.. code-block:: python

    from telegram.client import Telegram

    tg = Telegram(
        api_id=123456,
        api_hash='api_hash',
        phone='+31611111111',
        database_encryption_key='changeme1234',
    )

.. note::
    The library (actually ``tdlib``) stores messages database and received files in the ``/tmp/.tdlib_files/{phone_number}/``.
    You can change this behaviour with the ``files_directory`` parameter.

.. note::
    You can use bot tokens: just pass ``bot_token`` instead of ``phone``.

After that, you have to login:

.. code-block:: python

    tg.login()

In this example we use a blocking version of the `login` function.  You can find an example for non-blocking usage here: :ref:`non_blocking_login`.
Telegram will send you a code in an SMS or as a Telegram message. If you have enabled 2FA, you will be asked for your password too. After successful login you can start using the library:

.. code-block:: python

    # this function will be called
    # for each received message
    def new_message_handler(update):
        print('New message!')

    tg.add_message_handler(new_message_handler)
    tg.idle()  # blocking waiting for CTRL+C

This code adds a new message handler which prints a simple text every time it receives a new message.
``tg.idle()`` is neccessary to block your script and wait for an exit shortcut (``CTRL+C``).

If you run this code, you will see something like that:

.. code-block:: sh

    New message!
    New message!

Let's add more logic to the message handler:

.. code-block:: python

    def new_message_handler(update):
        # we want to process only text messages
        message_content = update['message']['content'].get('text', {})
        message_text = message_content.get('text', '').lower()

        if message_text == 'ping':
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
        # we want to process only text messages
        message_content = update['message']['content'].get('text', {})
        message_text = message_content.get('text', '').lower()

        if message_text == 'ping':
            chat_id = update['message']['chat_id']
            print(f'Ping has been received from {chat_id}')
            tg.send_message(
                chat_id=chat_id,
                text='pong',
            )

    tg.add_message_handler(new_message_handler)
    tg.idle()

Done! You have created your first client for the Telegram Messenger.

idle and stop
-------------

You must call `stop` to properly stop python-telegram and tdlib.
It calls tdlib's `close` method and waits until it's finished.

When you use `idle`, it automatically waits until you call `stop` in another thread, or one of the stop signals is received.
