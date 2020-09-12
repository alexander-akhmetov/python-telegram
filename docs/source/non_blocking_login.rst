.. _non_blocking_login:

==================
Non blocking login
==================

By default python-telegram uses blocking login method. It presents a prompt to the user for password and code.
It makes it hard to use python-telegram as a web app. In this case you might want non blocking login.

``telegram.client.Telegram`` instance keeps current authoriaztion state in ``authorization_state`` property. You can also request it from tdlib by calling ``get_authorization_state()`` method.
``login(blocking=False)`` tries to login, but when Telegram needs a password or a code, it returns current authorization state and gives you ability to provide it manually.
When the code is sent (using ``send_code`` method), you can call ``login(bloking=False)`` again to continue the process. When the user logged it, login returns ``AuthorizationState.READY``.

Let's have a look at the example.

1. Initialize the client:

.. code-block:: python

    from telegram.client import Telegram, AuthorizationState

    tg = Telegram(
        api_id='api_id',
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
    # You can also check that tg.authorization state is AuthorizationState.READY.

We analyze the authorization state, send code or password and continue the login process after.
Currently you can expect only two blocking authorization states: ``AuthorizationState.WAIT_CODE`` and ``AuthorizationState.WAIT_PASSWORD``.

You can find the full example in the repository, ``examples/get_me_non_blocking_login.py``.
