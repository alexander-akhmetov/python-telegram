from unittest.mock import Mock, patch

from telegram.tdjson import _get_tdjson_lib_path


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
