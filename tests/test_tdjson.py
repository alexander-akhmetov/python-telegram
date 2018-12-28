from telegram.tdjson import _get_tdjson_lib_path


class Test_get_tdjson_lib_path(object):
    def test_for_darwin(self, mocker):
        mocked_system = mocker.Mock(return_value='Darwin')
        mocked_resource = mocker.Mock()

        with mocker.mock_module.patch('telegram.tdjson.platform.system', mocked_system):
            with mocker.mock_module.patch('telegram.tdjson.pkg_resources.resource_filename',
                                          mocked_resource):
                _get_tdjson_lib_path()

        mocked_resource.assert_called_once_with(
            'telegram',
            'lib/darwin/libtdjson.dylib',
        )

    def test_for_linux(self, mocker):
        mocked_system = mocker.Mock(return_value='Linux')
        mocked_resource = mocker.Mock(return_value='/tmp/')

        with mocker.mock_module.patch('telegram.tdjson.platform.system', mocked_system):
            with mocker.mock_module.patch('telegram.tdjson.pkg_resources.resource_filename',
                                          mocked_resource):
                _get_tdjson_lib_path()

        mocked_resource.assert_called_once_with(
            'telegram',
            'lib/linux/libtdjson.so',
        )

    def test_for_windows(self, mocker):
        mocked_system = mocker.Mock(return_value='Windows')
        mocked_resource = mocker.Mock(return_value='/tmp/')

        with mocker.mock_module.patch('telegram.tdjson.platform.system', mocked_system):
            with mocker.mock_module.patch('telegram.tdjson.pkg_resources.resource_filename',
                                          mocked_resource):
                _get_tdjson_lib_path()

        mocked_resource.assert_called_once_with(
            'telegram',
            'lib/linux/libtdjson.so',
        )

    def test_unknown(self, mocker):
        mocked_system = mocker.Mock(return_value='Unknown')
        mocked_resource = mocker.Mock(return_value='/tmp/')

        with mocker.mock_module.patch('telegram.tdjson.platform.system', mocked_system):
            with mocker.mock_module.patch('telegram.tdjson.pkg_resources.resource_filename',
                                          mocked_resource):
                _get_tdjson_lib_path()

        mocked_resource.assert_called_once_with(
            'telegram',
            'lib/linux/libtdjson.so',
        )
