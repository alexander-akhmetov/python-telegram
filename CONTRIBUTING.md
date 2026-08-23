# Contributing

Pull requests are welcome!

Feel free to open an issue if you find a bug, have new ideas, suggestions,
or spot a mistake in the [documentation](https://python-telegram.readthedocs.io/latest/).

## Reporting bugs

We use [GitHub
Issues](https://github.com/alexander-akhmetov/python-telegram/issues) to track
bugs. If you find a bug, please open a new issue.

Try to include steps to reproduce the bug, a detailed description, and some sample code if possible.

## Pull request process

1. Fork the repository and create a new branch from `main`.
2. Make your changes and don't forget to add new tests :)
3. Ensure the tests pass with your changes.
4. Create a new PR!

## Coding style

The project uses [ruff](https://docs.astral.sh/ruff/) as an autoformatter and linter.

## Tests

To run tests you need to install [tox](https://tox.wiki/).

Run tests:

```shell
tox
```

Run a specific test using python 3.12:

```shell
tox -e py312 -- -k test_add_message_handler
```

`tests/test_tdlib_binary.py` loads a real `tdlib` and skips when it cannot find one, so a
checkout with no system `tdlib` still runs a green suite.

## tdlib binaries

The binaries are not in this repository. They are built in
[tdlib-compiled](https://github.com/alexander-akhmetov/tdlib-compiled), which publishes one
per platform as a release with a `SHA256SUMS` and a `BUILD-INFO.json`.

`tdlib.lock` pins that release tag, the asset names, the wheel platform tags and the sha256
of each asset. Bumping tdlib is a PR that changes only that file: copy the tag, the digests
and the `wheel_platform` values out of the new release's `BUILD-INFO.json`, so the lock
always describes bytes that exist.

To build one platform wheel yourself, download the asset for your target and run:

```shell
PYTHON_TELEGRAM_TDLIB_TARGET=macos-arm64 PYTHON_TELEGRAM_TDLIB_DIR=tdlib python -m build --wheel
```

With no `PYTHON_TELEGRAM_TDLIB_TARGET` the build produces a binary-free pure wheel, which is
what `pip install -e .` needs.

`make docker/build` installs the released PyPI version, not your working tree.

## Release checklist

1. Bump `__version__` in `telegram/__init__.py` and write the changelog entry.
2. Tag a release candidate first, for example `1.1.0rc1`. The tag pattern matches it and
   PyPI does not serve a prerelease by default, so it exercises all four wheels, the four
   verification runners, the attestation and trusted publishing with a version nobody
   installs by accident.
3. Install the release candidate wheel and run `examples/echo_bot.py` against a bot token,
   on macOS arm64 and on Linux. Watch the full
   `NONE -> WAIT_TDLIB_PARAMETERS -> WAIT_PHONE_NUMBER -> READY` sequence. This is the only
   check that covers the login request payloads; the smoke test cannot, because they need a
   live session.
4. Tag the final version.
