=========
Changelog
=========

[unreleased]

[0.19.0] 2024-06-23

- Python versions 3.7 and 3.8 are no longer supported.
- tdlib 1.8.31.

[0.18.0] - 2023-03-13

- Added support for tdlib > 1.8.5. (thanks to @JleMyP)

[0.17.0] - 2023-01-25

- Added ``import_contacts`` method. (thanks to @vlad-lf)
- Added markup support. It is now possible to send formatted text (html/markdown and telegram-specific formats, for example hidden spoiler styling)  (thanks to @SKY-ALIN)

[0.16.0] - 2022-08-18

- Search for the system library first, and fallback to the embedded one if the system was not found.
- Fixed the finding system library mechanism (thanks to @weirdo-neutrino)
- tdlib v1.8.5

[0.15.0] - 2021-12-03

- tdlib v1.7.9. Fixes ``UPDATE_APP_TO_LOGIN`` errors.

[0.14.0] - 2020-12-17

- tdlib v1.7.0

[0.13.0] - 2020-11-16

- Non-blocking login, see ``examples/get_me_non_blocking_login.py`` (thanks to @melfnt).
- Better stop. python-teleram calls `close` and waits until tdlib is closed.

[0.12.0] - 2020-03-29

- New example: ``examples/clear_group_messages.py`` (thanks to @h4x3rotab)
- Proxy support (thanks to @h4x3rotab)
- New methods: ``delete_messages``, ``get_supergroup_full_info``, ``create_basic_group_chat``. (thanks to @h4x3rotab)
- Fix #67: fixed infinite waiting for a result during login or for an `ok` result type.
- New Telegram initialization parameter: ``use_secret_chats`` (``True`` by default) (thanks to @DopeforHope)
- Fix #81: ``encryption_key`` for tdlib database encryption is now being sent to tdlib as a base64 encoded string.

[0.11.0] - 2020-02-15

- ``tdlib`` upgraded to ``v1.6.0`` (from `this repository <https://github.com/alexander-akhmetov/tdlib-compiled>`_)
- Added a new parameter to the ``call_method``: ``block=False``. If it is set to ``True``, the method waits for the result from tdlib.
- Added ``Telegram.get_message`` method (thanks to @ali-shokoohi)
- Fixed a race condition when in some cases ``AsyncResult.wait()`` could raise ``TimeoutError`` or end up in an endless loop. (thanks to @akamaus)
- Added a new method: ``get_user``.
- Added ``Telegram.remove_update_handler`` function to remove update handlers.

[0.10.0] - 2019-04-10

- **Incompatible** Linux library has been changed, now it's compiled on Ubuntu with libc.

[0.9.0] - 2019-04-05

- **Incompatible** default path for files is changed. Now the library uses an md5 hash of the phone number or bot token instead of just a phone number.
  It should not be noticeable for most cases, but if you rely on locally saved files or database, you need to pass the ``files_directory`` parameter to the ``telegram.client.Telegram``.
- Fixed problem with randomly raised "Database encryption key is needed" errors during login process. (#12)
- Fixed ``stop`` method execution. (#8)
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
