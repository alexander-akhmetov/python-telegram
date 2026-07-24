.. _non_blocking_login:

==================
Non blocking login
==================

By default, ``python-telegram`` uses the blocking login method. It asks the user for the code and the password with an interactive prompt.
That makes it hard to use the library inside a web application, where there is no terminal to prompt. In that case you want the non-blocking login.

A ``telegram.client.Telegram`` instance keeps the current authorization state in the ``authorization_state`` attribute.
You can also request it from ``tdlib`` by calling the ``get_authorization_state()`` method.

``login(blocking=False)`` tries to log in, but when Telegram needs a code or a password, it returns the current authorization state instead of prompting, so that you can supply the value yourself.
After you send the code with the ``send_code`` method, call ``login(blocking=False)`` again to continue.
Once the user is logged in, ``login`` returns ``AuthorizationState.READY``.

Let's have a look at the example.

1. Initialize the client:

.. code-block:: python

    from telegram.client import Telegram, AuthorizationState

    tg = Telegram(
        api_id=123456,
        api_hash='api_hash',
        phone='+31611111111',
        database_encryption_key='changeme1234',
    )


2. Call ``tg.login(blocking=False)``. It returns a new ``AuthorizationState``:

.. code-block:: python

    code = 'some-code'
    password = 'secret-password'

    state = tg.login(blocking=False)

    if state == AuthorizationState.WAIT_CODE:
        # Telegram expects a pin code
        tg.send_code(code)
        state = tg.login(blocking=False)  # continue the login process

    if state == AuthorizationState.WAIT_PASSWORD:
        tg.send_password(password)
        state = tg.login(blocking=False)  # continue the login process

    # Logged in.
    # You can also check that tg.authorization_state is AuthorizationState.READY.

The code checks the authorization state, sends the code or the password, and then continues the login process.

These authorization states stop and wait for input:

- ``AuthorizationState.WAIT_CODE``: send the code with ``send_code``.
- ``AuthorizationState.WAIT_EMAIL_ADDRESS``: Telegram asks for the login email address of the account. Send it with ``send_email_address``.
- ``AuthorizationState.WAIT_EMAIL_CODE``: send the code from that email with ``send_email_code``.
- ``AuthorizationState.WAIT_PASSWORD``: send the password with ``send_password``.
- ``AuthorizationState.WAIT_REGISTRATION``: the account does not exist yet. Send the first and the last name with ``register_user``.

You can find the full example in the repository, ``examples/get_me_non_blocking_login.py``.
