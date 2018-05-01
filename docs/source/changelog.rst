=========
Changelog
=========

[0.4.0] - 2018-04-29
--------------------

Added two new methods:

-  ``get_instant_view`` - get instant view of a web page
-  ``call_method`` - call any method with any params

New example: `get_instant_view.py`_

.. _section-1:

[0.3.1] - 2018-04-29
--------------------

-  Logging level in the examples changed to ``INFO``.
-  Added new ``Makefile`` command: ``docker-echo-bot``.
-  All ``docker-`` commands in the ``Makefile`` now mount ``/tmp/`` from
   a host machine to store tdlib’s files.

.. _section-2:

[0.3.0] - 2018-04-28
--------------------

-  Added ``Dockerfile`` and ``Makefile`` with some examples.
-  Changed directory for tdlib files to
   ``/tmp/.tdlib_files_{self.phone}/``.

.. _get_instant_view.py: examples/get_instant_view.py
