Welcome to python-telegram's documentation
===========================================

|build-status| |docker-hub| |pypi|

.. toctree::
   :maxdepth: 1

   tutorial
   non_blocking_login
   telegram
   tdlib
   proxy
   changelog

Client for the `tdlib <https://github.com/tdlib/td>`_ library (at very early stage :) ).

Installation
------------

At first you must install ``tdlib``.

How to build tdlib
~~~~~~~~~~~~~~~~~~

`Official documentation <https://github.com/tdlib/td#building>`_

Do not forget install it after:

.. code-block:: bash

    make install


Library installation
~~~~~~~~~~~~~~~~~~~~

This library works with Python 3.6+ only.

.. code-block:: bash

     python3 -m pip install python-telegram

After you must `register <http://my.telegram.org/apps/>`_ a new Telegram application.

Now you can start using the library: :ref:`tutorial`.

.. note::
    You can find more examples `here <https://github.com/alexander-akhmetov/python-telegram/tree/master/examples>`_.

.. note::
    The ``tdlib`` binary for Linux provided by ``python-shortcuts`` is built on Ubuntu with libc since version ``0.10.0``. Before ``0.10.0``, Alpine Linux was used with ``musl``.

Docker
------

This library has a `docker image <https://hub.docker.com/r/akhmetov/python-telegram/>`_

.. code-block:: bash

    docker run -i -t --rm \
                -v /tmp/docker-python-telegram/:/tmp/ \
                akhmetov/python-telegram \
                python3 /app/examples/send_message.py $(API_ID) $(API_HASH) $(PHONE) $(CHAT_ID) $(TEXT)


.. |build-status| image:: https://github.com/alexander-akhmetov/python-telegram/workflows/python-telegram%20tests/badge.svg    :alt: build status
    :target: https://github.com/alexander-akhmetov/python-telegram/actions

.. |docker-hub| image:: https://img.shields.io/docker/automated/akhmetov/python-telegram.svg
    :alt: Documentation Status
    :target: https://hub.docker.com/r/akhmetov/python-telegram/

.. |pypi| image:: https://img.shields.io/pypi/v/python-telegram.svg
    :alt: pypi package
    :target: http://pypi.org/project/python-telegram/
