.. _tdlib:

=====
tdlib
=====

How to build tdlib
~~~~~~~~~~~~~~~~~~

`Official documentation <https://github.com/tdlib/td#building>`_

Do not forget to install the library after you have built it:

.. code-block:: bash

    make install


------------

Also, you can use it with Docker:
    * this package + tdlib `python-telegram-docker <https://hub.docker.com/r/akhmetov/python-telegram/>`_


------------

You can call any method of ``tdlib`` with ``python-telegram`` using ``call_method``:

.. code-block:: python

    tg = Telegram(...)
    params = {'user_id': 1}
    result = tg.call_method('getUser', params)
