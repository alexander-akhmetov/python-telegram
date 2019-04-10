=========
Changelog
=========

[0.10.0] - 2019-04-10

- **Incompatible** Linux library has been changed, now it's compiled on Ubuntu with libc.

[0.9.0] - 2019-04-05

- **Incompatible** default path for files is changed. Now the library uses an md5 hash of the phone number or bot token instead of just a phone number.
  It should not be noticeable for most cases, but if you rely on locally saved files or database, you need to pass the ``files_directory`` parameter to the ``telegram.client.Telegram``.
- Fixed problem with randomly raised "Database encryption key is needed" errors during login process. (#12)
- Fixed `stop` method execution. (#8)
- Added ``examples/bot_login.py`` example.

[0.8.0] - 2019-03-17

- ``telegram.client.Telegram`` now supports any update type with a new method ``add_update_handler(handler_type, func)``
- ``tdlib v 1.3.0``
- Fixed problem with openssl in Dockerfile (#4)

[0.7.0]

- New method ``getMe`` with an example.

[0.6.1] - 2018-05-01

- Fixes for the Linux pre-compiled tdlib library.

[0.6.0] - 2018-05-01

- Fixes for the Linux pre-compiled tdlib library.

[0.5.0] - 2018-05-01
--------------------

- New **required** parameter in the ``telegram.client.Telegram``: ``database_encryption_key``.

- Compiled ``tdlib`` files now are in the pypi package (Linux and MacOS).

- Default location of the tdlib's files changed to ``/tmp/.tdlib_files/{phone_number}``.

- Now you can define additional optional params:

    * use_test_dc (default False)
    * device_model
    * system_version
    * system_language_code
    * application_version
    * use_message_database (default True)

- Added new example: `chat_stats.py`.

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
