========
Tutorial
========

How to build a simple echo-bot with ``python-telegram``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Ok, now you have installed ``python-telegram`` and ``tdlib``. Let's create a simple echo-bot, which sends ``pong`` if receives ``ping``.

At first, import ``Telegram`` and initialize it with your credentials.

.. code-block:: python

    from telegram.client import Telegram

    tg = Telegram(
        api_id=args.api_id,
        api_hash=args.api_hash,
        phone=args.phone,
    )

.. note::
    ``tdlib`` stores login information and messages database on the filesystem.
    This library is configured to save this information to the ``/tmp/.tdlib_files_{phone_number}/``.

When you have to login:

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
                chat_id=chat_id,
                text='pong',
            )

The full code:

.. code-block:: python


    from telegram.client import Telegram

    tg = Telegram(
        api_id=args.api_id,
        api_hash=args.api_hash,
        phone=args.phone,
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

Done! Now you have built your first and very simple client for the Telegram Messenger.
