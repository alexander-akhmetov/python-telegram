from unittest.mock import Mock, patch

from telegram.tdjson import TDJson, _get_tdjson_lib_path


class TestGetTdjsonTdlibPath:
    def test_for_darwin(self):
        mocked_system = Mock(return_value="Darwin")
        mocked_files = Mock()
        mocked_joinpath = Mock()

        with patch("telegram.tdjson.platform.system", mocked_system):
            with patch("importlib.resources.files", mocked_files):
                mocked_files.return_value.joinpath = mocked_joinpath
                _get_tdjson_lib_path()

        mocked_files.assert_called_once_with("telegram")
        mocked_joinpath.assert_called_once_with("lib/darwin/libtdjson.dylib")

    def test_for_linux(self):
        mocked_system = Mock(return_value="Linux")
        mocked_files = Mock()
        mocked_joinpath = Mock()

        with patch("telegram.tdjson.platform.system", mocked_system):
            with patch("importlib.resources.files", mocked_files):
                mocked_files.return_value.joinpath = mocked_joinpath
                _get_tdjson_lib_path()

        mocked_files.assert_called_once_with("telegram")
        mocked_joinpath.assert_called_once_with("lib/linux/libtdjson.so")

    def test_unknown(self):
        mocked_system = Mock(return_value="Unknown")
        mocked_files = Mock()
        mocked_joinpath = Mock()

        with patch("telegram.tdjson.platform.system", mocked_system):
            with patch("importlib.resources.files", mocked_files):
                mocked_files.return_value.joinpath = mocked_joinpath
                _get_tdjson_lib_path()

        mocked_files.assert_called_once_with("telegram")
        mocked_joinpath.assert_called_once_with("lib/linux/libtdjson.so")


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

    def test_fatal_error_callback_stored_on_instance(self):
        tdjson = self._make_tdjson()
        assert hasattr(tdjson, "_c_on_fatal_error_callback")
        assert tdjson._c_on_fatal_error_callback is not None
