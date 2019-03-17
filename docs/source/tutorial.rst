.. _tutorial:

========
Tutorial
========

How to build a simple echo-bot with ``python-telegram``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

     python3 -m pip install python-telegram

Ok, now you have installed the library. Let's create a simple echo-bot, which sends "pong" if receives "ping".

At first, initialize telegram client with your credentials:

.. code-block:: python

    from telegram.client import Telegram

    tg = Telegram(
        api_id='api_id',
        api_hash='api_hash',
        phone='+31611111111',
        database_encryption_key='changeme1234',
    )

.. note::
    The library (actually ``tdlib``) stores messages database and received files in the ``/tmp/.tdlib_files/{phone_number}/``.
    You can change this behaviour with the ``files_directory`` parameter.

.. note::
    You can use bot token: just pass ``bot_token`` instead of ``phone``.

After, you have to login:

.. code-block:: python

    tg.login()

It's a blocking call. Telegram will send you a code in an SMS or in the messenger. Enter this code. If you have enabled 2FA,
you will be asked for a password too. After successful login you can start using the library:

.. code-block:: python

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

Let's add more logic inside the message handler:

.. code-block:: python

    def new_message_handler(update):
        message_content = update['message']['content'].get('text', {})
        # we need this because of different message types: photos, files, etc.
        message_text = message_content.get('text', '').lower()

        if message_text == 'ping':
            chat_id = update['message']['chat_id']
            print(f'Ping has been received from {chat_id}')
            tg.send_message(
                chat_id=chat_id,  # str
                text='pong',
            )

The full code:

.. code-block:: python


    from telegram.client import Telegram

    tg = Telegram(
        api_id='api_id',
        api_hash='api_hash',
        phone='+31611111111',
        database_encryption_key='changeme1234',
    )
    tg.login()

    def new_message_handler(update):
        message_content = update['message']['content'].get('text', {})
        # we need this because of different message types: photos, files, etc.
        message_text = message_content.get('text', '').lower()

        if message_text == 'ping':
            chat_id = update['message']['chat_id']
            print(f'Ping has been received from {chat_id}')
            tg.send_message(
                chat_id=chat_id,
                text='pong',
            )

    tg.add_message_handler(new_message_handler)
    tg.idle()  # blocking waiting for CTRL+C

Done! You have built your first and very simple client for the Telegram Messenger.
