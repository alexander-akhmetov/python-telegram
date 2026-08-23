## What This Is

Python wrapper around Telegram's TDLib C library. Provides a synchronous API over TDLib's async backend using ctypes, threads, and a promise-like `AsyncResult` pattern.

## Commands

```bash
# Run full test suite + linting + type checks
tox

# Run tests for a specific Python version
tox -e py312

# Run a single test
tox -e py312 -- -k test_send_message

# Lint
tox -e ruff

# Format check
tox -e ruff-format

# Auto-fix lint/format
ruff check --fix && ruff format

# Type check (strict mode)
tox -e mypy

# Build Docker image
make docker/build

# Build PyPI package
make build-pypi
```

## Packaging

The tdlib binaries are not in git. They are built in [tdlib-compiled](https://github.com/alexander-akhmetov/tdlib-compiled) and attached to a release there; `tdlib.lock` pins that release tag and the sha256 of every asset.

`hatch_build.py` turns the pure wheel into a platform wheel. With `PYTHON_TELEGRAM_TDLIB_TARGET` unset it does nothing, which is what `pip install -e .` and the sdist need. With a target set it verifies the asset against `tdlib.lock`, force-includes it as `telegram/lib/libtdjson.{so,dylib}` and retags the wheel `py3-none-<wheel_platform>`. An unknown target, a missing file or a bad checksum raises: falling back to a pure wheel would publish something pip installs everywhere and that raises on first use.

```bash
PYTHON_TELEGRAM_TDLIB_TARGET=macos-arm64 PYTHON_TELEGRAM_TDLIB_DIR=tdlib python -m build --wheel
```

The sdist never carries a binary, three independent ways: the hook is registered under the wheel target only, `telegram/lib` is in the sdist `exclude`, and the binary is not in git.

## Releasing

Build backend is hatchling; the version is a literal in `telegram/__init__.py`, read by `[tool.hatch.version]`. Pushing a version tag runs `.github/workflows/release.yml`: `build` makes four wheels and the sdist, `verify` installs each wheel on its real platform and loads the binary, then `release` attests and creates the GitHub release, and `publish-pypi` uploads with trusted publishing (OIDC, no API token). There is no manual upload path.

## Architecture

**TDJson** (`telegram/tdjson.py`) — ctypes binding to `libtdjson`. Handles library discovery, creation/destruction of TDLib client instances, and JSON send/receive/execute. Discovery order: the `library_path` argument, `PYTHON_TELEGRAM_TDLIB_PATH`, `ctypes.util.find_library("tdjson")`, then the bundled `telegram/lib/libtdjson.{so,dylib}`. Nothing found raises `TDLibNotFoundError`, an `OSError` subclass.

**Telegram** (`telegram/client.py`) — high-level client. Manages login flow via an `AuthorizationState` state machine (NONE → WAIT_TDLIB_PARAMETERS → ... → READY). All API calls return an `AsyncResult`; a background `_listen_to_td` thread receives TDLib responses and matches them to pending results by `@extra` request ID.

**AsyncResult** (`telegram/utils.py`) — promise-like wrapper. `wait(timeout, raise_exc)` blocks until TDLib responds. Special-cased for `updateAuthorizationState` (doesn't resolve on bare "ok" responses).

**Worker** (`telegram/worker.py`) — processes message/update handlers in a daemon thread. `add_message_handler()` and `add_update_handler()` register callbacks that the worker dispatches from a queue.
