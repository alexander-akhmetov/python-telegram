Welcome to python-telegram's documentation
===========================================

|build-status| |docker-hub|

.. toctree::
   :maxdepth: 1

   tutorial
   telegram
   changelog

Client for the `tdlib <https://github.com/tdlib/td>`_ library (at very early stage :) ).

Installation
------------

To install just run

.. code-block:: bash

     python3 -m pip install python-telegram

To use `python-telegram` you need to:

1. `Register <http://my.telegram.org/apps/>`_ a new Telegram app
2. Build `tdlib <https://github.com/tdlib/td>`_
3. Install ``python-telegram``.

The second step is the most difficult. You can read more about building tdlib `here <https://github.com/tdlib/td#building>`_.

If you don't want to build it yourself, you can use pre-built docker image with `python-telegram <https://hub.docker.com/r/akhmetov/python-telegram/>`_ or `tdlib <https://hub.docker.com/r/akhmetov/tdlib/>`_.

.. note::
    You can find the examples in the `source code <https://github.com/alexander-akhmetov/python-telegram/tree/master/examples>`_.


.. |build-status| image:: https://travis-ci.org/alexander-akhmetov/python-telegram.svg?branch=master
    :alt: build status
    :target: https://travis-ci.org/alexander-akhmetov/python-telegram

.. |docker-hub| image:: https://img.shields.io/docker/automated/akhmetov/python-telegram.svg
    :alt: Documentation Status
    :target: https://hub.docker.com/r/akhmetov/python-telegram/
