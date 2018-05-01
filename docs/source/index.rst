Welcome to python-telegram's documentation
===========================================

|build-status| |docker-hub| |pypi|

.. toctree::
   :maxdepth: 1

   tutorial
   telegram
   tdlib
   changelog

Client for the `tdlib <https://github.com/tdlib/td>`_ library (at very early stage :) ).

Installation
------------

.. code-block:: bash

     python3 -m pip install python-telegram

After you must `register <http://my.telegram.org/apps/>`_ a new Telegram application.

Now you can start using the library: :ref:`tutorial`.

.. note::
    You can find more examples `here <https://github.com/alexander-akhmetov/python-telegram/tree/master/examples>`_.

This package contains pre-built ``tdlib`` library, so you don't need build it (Linux + MacOS).
But if you want, you can find more information about building tdlib here: :ref:`tdlib`.

Docker
------

This library has a `docker image <https://hub.docker.com/r/akhmetov/python-telegram/>`_

.. code-block:: bash

    docker run -i -t --rm \
                -v /tmp/docker-python-telegram/:/tmp/ \
                akhmetov/python-telegram \
                python3 /app/examples/send_message.py $(API_ID) $(API_HASH) $(PHONE) $(CHAT_ID) $(TEXT)


.. |build-status| image:: https://travis-ci.org/alexander-akhmetov/python-telegram.svg?branch=master
    :alt: build status
    :target: https://travis-ci.org/alexander-akhmetov/python-telegram

.. |docker-hub| image:: https://img.shields.io/docker/automated/akhmetov/python-telegram.svg
    :alt: Documentation Status
    :target: https://hub.docker.com/r/akhmetov/python-telegram/

.. |pypi| image:: https://img.shields.io/pypi/v/python-telegram.svg
    :alt: pypi package
    :target: http://pypi.org/project/python-telegram/

