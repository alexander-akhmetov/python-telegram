.. _non_blocking_login:

==================
Non blocking login
==================

By default python-telegram uses blocking login method. It presents a prompt to the user for password and code.
It makes it hard to use python-telegram as a web app. In this case you might want non blocking login.


Initialize the client as usually:

.. code-block:: python

    from telegram.client import Telegram, AuthorizationState

    tg = Telegram(
        api_id='api_id',
        api_hash='api_hash',
        phone='+31611111111',
        database_encryption_key='changeme1234',
    )


And call ``tg.login(blocking=False)``. It returns a new ``telegram.client.AuthorizationState``:

.. code-block:: python

    code = ...
    password = ...

    state = tg.login(blocking=False)

    if state == AuthorizationState.WAIT_CODE:
        tg.send_code(code)
        tg.login(blocking=False)  # continue the login process

    if state == AuthorizationState.WAIT_PASSWORD:
        tg.send_password(password)
        tg.login(blocking=False)  # continue the login process

    # logged in

    
Currently there are only two blocking authorization states: AuthorizationState.WAIT_CODE and AuthorizationState.WAIT_PASSWORD.

You can find the full example in ``examples/get_me_non_blocking_login.py``.
