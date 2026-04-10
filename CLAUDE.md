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

## Architecture

**TDJson** (`telegram/tdjson.py`) — ctypes binding to `libtdjson`. Handles library discovery (system path → bundled precompiled in `telegram/lib/{darwin,linux}/`), creation/destruction of TDLib client instances, and JSON send/receive/execute.

**Telegram** (`telegram/client.py`) — high-level client. Manages login flow via an `AuthorizationState` state machine (NONE → WAIT_TDLIB_PARAMETERS → ... → READY). All API calls return an `AsyncResult`; a background `_listen_to_td` thread receives TDLib responses and matches them to pending results by `@extra` request ID.

**AsyncResult** (`telegram/utils.py`) — promise-like wrapper. `wait(timeout, raise_exc)` blocks until TDLib responds. Special-cased for `updateAuthorizationState` (doesn't resolve on bare "ok" responses).

**Worker** (`telegram/worker.py`) — processes message/update handlers in a daemon thread. `add_message_handler()` and `add_update_handler()` register callbacks that the worker dispatches from a queue.
