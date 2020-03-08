import pytest

from unittest.mock import Mock, patch

from telegram.utils import AsyncResult


class TestAsyncResult:
    def test_initial_params(self):
        mocked_uuid = Mock()
        mocked_uuid.uuid4().hex = 'some-id'
        with patch('telegram.utils.uuid', mocked_uuid):
            async_result = AsyncResult(client='123')

        assert async_result.client == '123'
        assert async_result.id == 'some-id'

    def test_str(self):
        mocked_uuid = Mock()
        mocked_uuid.uuid4().hex = 'some-id'
        with patch('telegram.utils.uuid', mocked_uuid):
            async_result = AsyncResult(client=None)

        assert async_result.__str__() == f'AsyncResult <some-id>'

    def test_parse_update_with_error(self):
        async_result = AsyncResult(client=None)
        update = {'@type': 'error', 'some': 'data'}

        assert async_result.error is False
        assert async_result.error_info is None

        async_result.parse_update(update)

        assert async_result.error is True
        assert async_result.error_info == update
        assert async_result.update is None
        assert async_result.ok_received is False
        assert async_result._ready.is_set() is True

    def test_parse_update_ok(self):
        async_result = AsyncResult(client=None)
        update = {'@type': 'ok', 'some': 'data'}

        async_result.parse_update(update)

        assert async_result.error is False
        assert async_result.error_info is None
        assert async_result.update is None
        assert async_result.ok_received is True
        assert async_result._ready.is_set() is True

    def test_parse_update_authorization_state_ok(self):
        # when id=updateAuthorizationState
        # and @type=ok
        # it should not set async_result._ready
        # because for updateAuthorizationState we want to wait for the
        # next message with result_id=updateAuthorizationState
        async_result = AsyncResult(
            client=None,
            result_id='updateAuthorizationState',
        )
        update = {'@type': 'ok', 'some': 'data'}

        async_result.parse_update(update)

        assert async_result.error is False
        assert async_result.error_info is None
        assert async_result.update is None
        assert async_result.ok_received is True
        assert async_result._ready.is_set() is False

    def test_parse_update(self):
        async_result = AsyncResult(client=None)
        update = {'@type': 'some_type', 'some': 'data'}

        async_result.parse_update(update)

        assert async_result.error is False
        assert async_result.error_info is None
        assert async_result.update == update
        assert async_result.ok_received is False
        assert async_result._ready.is_set() is True

    def test_wait_with_timeout(self):
        async_result = AsyncResult(client=None)

        with pytest.raises(TimeoutError):
            async_result.wait(timeout=0.01)

    def test_wait_with_update(self):
        async_result = AsyncResult(client=None)
        async_result.update = '123'
        async_result._ready.set()
        async_result.wait(timeout=0.01)

    def test_wait_with_error_and_raise_exc(self):
        async_result = AsyncResult(client=None)
        async_result.error = True
        async_result.error_info = 'some_error'
        async_result._ready.set()

        with pytest.raises(RuntimeError):
            async_result.wait(timeout=0.1, raise_exc=True)

    def test_wait_with_error_and_without_raise_exc(self):
        async_result = AsyncResult(client=None)
        async_result.error = True
        async_result.error_info = 'some_error'
        async_result._ready.set()
        async_result.wait(timeout=0.01)
