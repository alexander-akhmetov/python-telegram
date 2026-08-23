from __future__ import annotations

import ctypes.util
import importlib.resources
import json
import logging
import os
import platform
from ctypes import CDLL, CFUNCTYPE, c_char_p, c_double, c_int, c_longlong, c_void_p
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)

TDLIB_PATH_ENV_VAR = "PYTHON_TELEGRAM_TDLIB_PATH"

_OVERRIDES_HINT = (
    "Only the linux x86_64, linux aarch64, macOS arm64 and macOS x86_64 wheels bundle a "
    "libtdjson; the sdist never does. Install tdlib system-wide so ctypes can find it, or "
    f"point python-telegram at your own build with the {TDLIB_PATH_ENV_VAR} environment "
    "variable or the TDJson(library_path=...) argument."
)


class ClientDestroyedError(RuntimeError):
    """Raised when a TDJson client is used after it has been stopped"""


class TDLibNotFoundError(OSError):
    """
    Raised when no libtdjson can be found or loaded.

    Subclasses OSError because that is what ctypes.CDLL raises, so callers that
    already handle a failed load keep working.
    """


def _bundled_lib_path() -> Path:
    name = "libtdjson.dylib" if platform.system().lower() == "darwin" else "libtdjson.so"

    return Path(str(importlib.resources.files("telegram").joinpath(f"lib/{name}")))


def _resolve_tdjson_library() -> tuple[str, str]:
    """Returns the path of the libtdjson to load and the name of the source it came from."""
    env_path = os.environ.get(TDLIB_PATH_ENV_VAR)

    if env_path:
        return env_path, "env"

    system_library = ctypes.util.find_library("tdjson")

    if system_library is not None:
        return system_library, "system"

    bundled = _bundled_lib_path()

    if bundled.is_file():
        return str(bundled), "bundled"

    raise TDLibNotFoundError(
        f"No libtdjson found for {platform.system()} {platform.machine()}. "
        f"{TDLIB_PATH_ENV_VAR} is not set, ctypes.util.find_library('tdjson') found nothing, "
        f"and there is no bundled binary at {bundled}. {_OVERRIDES_HINT}"
    )


class TDJson:
    def __init__(self, library_path: str | None = None, verbosity: int = 2) -> None:
        if library_path is None:
            library_path, source = _resolve_tdjson_library()
        else:
            source = "library_path"

        logger.info('Using shared library "%s" (found via: %s)', library_path, source)

        self._build_client(library_path, verbosity)

    def __del__(self) -> None:
        if hasattr(self, "_td_json_client_destroy"):
            self.stop()

    def _build_client(self, library_path: str, verbosity: int) -> None:
        try:
            self._tdjson = CDLL(library_path)
        except OSError as error:
            raise TDLibNotFoundError(
                f"Failed to load libtdjson from {library_path} on "
                f"{platform.system()} {platform.machine()}: {error}. {_OVERRIDES_HINT}"
            ) from error

        # load TDLib functions from shared library
        self._td_json_client_create = self._tdjson.td_json_client_create
        self._td_json_client_create.restype = c_void_p
        self._td_json_client_create.argtypes = []

        self.td_json_client: int | None = self._td_json_client_create()

        self._td_json_client_receive = self._tdjson.td_json_client_receive
        self._td_json_client_receive.restype = c_char_p
        self._td_json_client_receive.argtypes = [c_void_p, c_double]

        self._td_json_client_send = self._tdjson.td_json_client_send
        self._td_json_client_send.restype = None
        self._td_json_client_send.argtypes = [c_void_p, c_char_p]

        self._td_json_client_execute = self._tdjson.td_json_client_execute
        self._td_json_client_execute.restype = c_char_p
        self._td_json_client_execute.argtypes = [c_void_p, c_char_p]

        self._td_json_client_destroy = self._tdjson.td_json_client_destroy
        self._td_json_client_destroy.restype = None
        self._td_json_client_destroy.argtypes = [c_void_p]

        self._td_set_log_file_path = self._tdjson.td_set_log_file_path
        self._td_set_log_file_path.restype = c_int
        self._td_set_log_file_path.argtypes = [c_char_p]

        self._td_set_log_max_file_size = self._tdjson.td_set_log_max_file_size
        self._td_set_log_max_file_size.restype = None
        self._td_set_log_max_file_size.argtypes = [c_longlong]

        self._td_set_log_verbosity_level = self._tdjson.td_set_log_verbosity_level
        self._td_set_log_verbosity_level.restype = None
        self._td_set_log_verbosity_level.argtypes = [c_int]

        self._td_set_log_verbosity_level(verbosity)

        fatal_error_callback_type = CFUNCTYPE(None, c_char_p)

        self._td_set_log_fatal_error_callback = self._tdjson.td_set_log_fatal_error_callback
        self._td_set_log_fatal_error_callback.restype = None
        self._td_set_log_fatal_error_callback.argtypes = [fatal_error_callback_type]

        # initialize TDLib log with desired parameters
        def on_fatal_error_callback(error_message: str) -> None:
            logger.error("TDLib fatal error: %s", error_message)

        self._c_on_fatal_error_callback = fatal_error_callback_type(on_fatal_error_callback)
        self._td_set_log_fatal_error_callback(self._c_on_fatal_error_callback)

    def _get_client(self) -> int:
        """
        Returns the client handle, or raises if the client has been destroyed.

        tdlib dereferences this handle, so passing a destroyed (NULL) one
        crashes the whole process instead of raising.
        """
        if self.td_json_client is None:
            raise ClientDestroyedError("The tdlib client is stopped and cannot be used anymore")

        return self.td_json_client

    def send(self, query: dict[Any, Any]) -> None:
        dumped_query = json.dumps(query).encode("utf-8")
        self._td_json_client_send(self._get_client(), dumped_query)
        logger.debug("[me ==>] Sent %s", dumped_query)

    def receive(self) -> None | dict[Any, Any]:
        result_str = self._td_json_client_receive(self._get_client(), 1.0)

        if result_str:
            result: dict[Any, Any] = json.loads(result_str.decode("utf-8"))
            logger.debug("[me <==] Received %s", result)

            return result

        return None

    def td_execute(self, query: dict[Any, Any]) -> dict[Any, Any] | Any:
        dumped_query = json.dumps(query).encode("utf-8")
        result_str = self._td_json_client_execute(self._get_client(), dumped_query)

        if result_str:
            result: dict[Any, Any] = json.loads(result_str.decode("utf-8"))

            return result

        return None

    def stop(self) -> None:
        if self.td_json_client is None:
            return
        self._td_json_client_destroy(self.td_json_client)
        self.td_json_client = None
