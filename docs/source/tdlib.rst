.. _tdlib:

=====
tdlib
=====

How to build tdlib
~~~~~~~~~~~~~~~~~~

You don't need to build ``tdlib`` yourself, it's already built and in the package.
But if you want, you can rebuild it and defile path to the shared library in the ``telegram.client.Telegram`` class constructor (``library_path``).

`Official documentation <https://github.com/tdlib/td#building>`_

Do not forget install the library after:

.. code-block:: bash

    make install


------------

Also, you can use it with Docker:
    * `tdlib-docker <https://hub.docker.com/r/akhmetov/tdlib/>`_
    * `python-telegram-docker <https://hub.docker.com/r/akhmetov/python-telegram/>`_

