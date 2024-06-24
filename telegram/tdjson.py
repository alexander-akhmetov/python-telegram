import json
import logging
import platform
import ctypes.util
from ctypes import CDLL, CFUNCTYPE, c_int, c_char_p, c_double, c_void_p, c_longlong
from typing import Any, Dict, Optional, Union
import importlib.resources

logger = logging.getLogger(__name__)


def _get_tdjson_lib_path() -> str:
    system_library = ctypes.util.find_library("tdjson")

    if system_library is not None:
        return system_library

    if platform.system().lower() == "darwin":
        platform_architecture = platform.machine()
        lib_name = f"darwin/{platform_architecture}/libtdjson.dylib"
    else:
        lib_name = "linux/libtdjson.so"

    return str(importlib.resources.files("telegram").joinpath(f"lib/{lib_name}"))


class TDJson:
    def __init__(self, library_path: Optional[str] = None, verbosity: int = 2) -> None:
        if library_path is None:
            library_path = _get_tdjson_lib_path()
        logger.info('Using shared library "%s"', library_path)

        self._build_client(library_path, verbosity)

    def __del__(self) -> None:
        if hasattr(self, "_tdjson") and hasattr(
            self._tdjson, "_td_json_client_destroy"
        ):
            self.stop()

    def _build_client(self, library_path: str, verbosity: int) -> None:
        self._tdjson = CDLL(library_path)

        # load TDLib functions from shared library
        self._td_json_client_create = self._tdjson.td_json_client_create
        self._td_json_client_create.restype = c_void_p
        self._td_json_client_create.argtypes = []

        self.td_json_client = self._td_json_client_create()

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

        self._td_set_log_fatal_error_callback = (
            self._tdjson.td_set_log_fatal_error_callback
        )
        self._td_set_log_fatal_error_callback.restype = None
        self._td_set_log_fatal_error_callback.argtypes = [fatal_error_callback_type]

        # initialize TDLib log with desired parameters
        def on_fatal_error_callback(error_message: str) -> None:
            logger.error("TDLib fatal error: %s", error_message)

        c_on_fatal_error_callback = fatal_error_callback_type(on_fatal_error_callback)
        self._td_set_log_fatal_error_callback(c_on_fatal_error_callback)

    def send(self, query: Dict[Any, Any]) -> None:
        dumped_query = json.dumps(query).encode("utf-8")
        self._td_json_client_send(self.td_json_client, dumped_query)
        logger.debug("[me ==>] Sent %s", dumped_query)

    def receive(self) -> Union[None, Dict[Any, Any]]:
        result_str = self._td_json_client_receive(self.td_json_client, 1.0)

        if result_str:
            result: Dict[Any, Any] = json.loads(result_str.decode("utf-8"))
            logger.debug("[me <==] Received %s", result)

            return result

        return None

    def td_execute(self, query: Dict[Any, Any]) -> Union[Dict[Any, Any], Any]:
        dumped_query = json.dumps(query).encode("utf-8")
        result_str = self._td_json_client_execute(self.td_json_client, dumped_query)

        if result_str:
            result: Dict[Any, Any] = json.loads(result_str.decode("utf-8"))

            return result

        return None

    def stop(self) -> None:
        self._td_json_client_destroy(self.td_json_client)
