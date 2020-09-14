.. _proxy:

========
Proxy
========

How to use a proxy with tdlib
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. note::
    The proxy definition has been changed in version ``0.13.0``

Define proxy parameters and pass them to ``Telegram``:

.. code-block:: python

    from telegram.client import Telegram
    from telegram.proxy import SOCKS5Proxy

    proxy = SOCKS5Proxy(
        server='localhost',
        port=1080,
        username='user',
        password='secret-password',
    )

    tg = Telegram(
        api_id='api_id',
        api_hash='api_hash',
        phone='+31611111111',
        database_encryption_key='changeme1234',
        proxy=proxy,
    )

There are three proxy classes: ``SOCKS5Proxy``, ``MTProtoProxy`` and ``HTTPProxy``.


MTProto proxy doesn't accept ``username`` and ``password`` and expects ``secret``:

.. code-block:: python

    from telegram.proxy import MTProtoProxy

    proxy = MTProtoProxy(
        server='localhost',
        port=1234,
        secret='secret',
    )

