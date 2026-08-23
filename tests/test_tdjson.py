from unittest.mock import patch

import pytest

from telegram.tdjson import TDLIB_PATH_ENV_VAR, TDJson, TDLibNotFoundError, _resolve_tdjson_library


@pytest.fixture
def no_library(monkeypatch):
    """Nothing is discoverable: no env override and no system tdjson."""
    monkeypatch.delenv(TDLIB_PATH_ENV_VAR, raising=False)
    monkeypatch.setattr("ctypes.util.find_library", lambda name: None)


@pytest.fixture
def bundled(tmp_path, monkeypatch):
    """Makes the bundled binary resolve into tmp_path instead of the installed package."""
    monkeypatch.setattr("telegram.tdjson.importlib.resources.files", lambda package: tmp_path)

    def create(name):
        path = tmp_path / "lib" / name
        path.parent.mkdir(exist_ok=True)
        path.touch()

        return path

    return create


class TestResolveTdjsonLibrary:
    @pytest.mark.parametrize(
        ("system", "lib_name"),
        [
            ("Darwin", "libtdjson.dylib"),
            ("Linux", "libtdjson.so"),
            # anything that is not macOS gets the ELF name, so the failure
            # names a real path
            ("Windows", "libtdjson.so"),
        ],
    )
    def test_bundled_name_per_platform(self, system, lib_name, no_library, bundled, monkeypatch):
        monkeypatch.setattr("telegram.tdjson.platform.system", lambda: system)
        expected = bundled(lib_name)

        assert _resolve_tdjson_library() == (str(expected), "bundled")

    def test_system_library_wins_over_bundled(self, no_library, bundled, monkeypatch):
        bundled("libtdjson.so")
        bundled("libtdjson.dylib")
        monkeypatch.setattr("ctypes.util.find_library", lambda name: "/usr/lib/libtdjson.so")

        assert _resolve_tdjson_library() == ("/usr/lib/libtdjson.so", "system")

    def test_env_override_wins_over_system_library(self, no_library, monkeypatch):
        monkeypatch.setattr("ctypes.util.find_library", lambda name: "/usr/lib/libtdjson.so")
        monkeypatch.setenv(TDLIB_PATH_ENV_VAR, "/custom/libtdjson.so")

        assert _resolve_tdjson_library() == ("/custom/libtdjson.so", "env")

    def test_raises_when_nothing_is_found(self, no_library, tmp_path, monkeypatch):
        monkeypatch.setattr("telegram.tdjson.importlib.resources.files", lambda package: tmp_path)

        with pytest.raises(TDLibNotFoundError) as error:
            _resolve_tdjson_library()

        assert isinstance(error.value, OSError)
        assert str(tmp_path) in str(error.value)
        assert TDLIB_PATH_ENV_VAR in str(error.value)


class TestTDJson:
    def _make_tdjson(self):
        with patch("telegram.tdjson.CDLL") as mocked_cdll:
            mocked_cdll.return_value.td_json_client_create.return_value = 12345
            tdjson = TDJson(library_path="/fake/lib.so", verbosity=0)
        return tdjson

    def test_del_calls_stop(self):
        tdjson = self._make_tdjson()
        with patch.object(tdjson, "stop") as mocked_stop:
            tdjson.__del__()
        mocked_stop.assert_called_once()

    def test_del_skips_stop_if_build_incomplete(self):
        tdjson = TDJson.__new__(TDJson)
        with patch.object(TDJson, "stop") as mocked_stop:
            tdjson.__del__()
        mocked_stop.assert_not_called()

    def test_stop_nulls_client_handle(self):
        tdjson = self._make_tdjson()
        assert tdjson.td_json_client is not None
        tdjson.stop()
        assert tdjson.td_json_client is None

    def test_stop_is_idempotent(self):
        tdjson = self._make_tdjson()
        tdjson.stop()
        tdjson.stop()
        tdjson._td_json_client_destroy.assert_called_once()

    @pytest.mark.parametrize(
        ("method", "args"),
        [
            ("send", ({"@type": "getAuthorizationState"},)),
            ("receive", ()),
            ("td_execute", ({"@type": "getAuthorizationState"},)),
        ],
    )
    def test_methods_raise_after_stop(self, method, args):
        tdjson = self._make_tdjson()
        tdjson.stop()

        with pytest.raises(RuntimeError, match="stopped"):
            getattr(tdjson, method)(*args)

        tdjson._td_json_client_send.assert_not_called()
        tdjson._td_json_client_receive.assert_not_called()
        tdjson._td_json_client_execute.assert_not_called()

    def test_load_failure_names_the_path_and_the_platform(self):
        with (
            patch("telegram.tdjson.CDLL", side_effect=OSError("incompatible architecture")),
            pytest.raises(TDLibNotFoundError) as error,
        ):
            TDJson(library_path="/fake/lib.so", verbosity=0)

        message = str(error.value)
        assert "/fake/lib.so" in message
        assert "incompatible architecture" in message
        assert TDLIB_PATH_ENV_VAR in message

    def test_fatal_error_callback_stored_on_instance(self):
        tdjson = self._make_tdjson()
        assert hasattr(tdjson, "_c_on_fatal_error_callback")
        assert tdjson._c_on_fatal_error_callback is not None
