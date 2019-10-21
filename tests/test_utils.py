from telegram.utils import AsyncResult


class TestAsyncResult(object):
    def test_initial_params(self, mocker):
        mocked_uuid = mocker.Mock()
        mocked_uuid.uuid4().hex = 'some-id'
        with mocker.mock_module.patch('telegram.utils.uuid', mocked_uuid):
            ar = AsyncResult(client='123')

        assert ar.client == '123'
        assert ar.id == 'some-id'

    def test_str(self, mocker):
        mocked_uuid = mocker.Mock()
        mocked_uuid.uuid4().hex = 'some-id'
        with mocker.mock_module.patch('telegram.utils.uuid', mocked_uuid):
            ar = AsyncResult(client=None)

        assert ar.__str__() == f'AsyncResult <some-id>'

    def test_parse_update_with_error(self):
        ar = AsyncResult(client=None)
        update = {'@type': 'error', 'some': 'data'}

        assert ar.error is False
        assert ar.error_info is None

        ar.parse_update(update)

        assert ar.error is True
        assert ar.error_info == update
        assert ar.update is None
        assert ar.ok_received is False

    def test_parse_update_ok(self):
        ar = AsyncResult(client=None)
        update = {'@type': 'ok', 'some': 'data'}

        ar.parse_update(update)

        assert ar.error is False
        assert ar.error_info is None
        assert ar.update is None
        assert ar.ok_received is True

    def test_parse_update(self):
        ar = AsyncResult(client=None)
        update = {'@type': 'some_type', 'some': 'data'}

        ar.parse_update(update)

        assert ar.error is False
        assert ar.error_info is None
        assert ar.update == update
        assert ar.ok_received is False

    def test_wait_with_timeout(self):
        ar = AsyncResult(client=None)
        try:
            ar.wait(timeout=0.01)
            raised = False
        except TimeoutError:
            raised = True

        assert raised is True

    def test_wait_with_update(self):
        ar = AsyncResult(client=None)
        ar.update = '123'
        ar._ready.set()
        ar.wait(timeout=0.01)

    def test_wait_with_error_and_raise_exc(self):
        ar = AsyncResult(client=None)
        ar.error = True
        ar.error_info = 'some_error'
        ar._ready.set()
        try:
            ar.wait(timeout=0.1, raise_exc=True)
            raised = False
        except RuntimeError:
            raised = True

        assert raised is True

    def test_wait_with_error_and_without_raise_exc(self):
        ar = AsyncResult(client=None)
        ar.error = True
        ar.error_info = 'some_error'
        ar._ready.set()
        ar.wait(timeout=0.01)
