.. _proxy:

=====
Proxy
=====

How to use a proxy with tdlib
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To use a proxy with ``tdlib``, define the proxy parameters and pass them to the ``Telegram`` class:

.. code-block:: python

    from telegram.client import Telegram

    proxy_type = {
        '@type': 'proxyTypeMtproto',  # or 'proxyTypeSocks5', or 'proxyTypeHttp'
    }
    proxy_port = 1234
    proxy_server = 'localhost'

    tg = Telegram(
        api_id=123456,
        api_hash='api_hash',
        phone='+31611111111',
        database_encryption_key='changeme1234',
        proxy_server=proxy_server,
        proxy_port=proxy_port,
        proxy_type=proxy_type,
    )

