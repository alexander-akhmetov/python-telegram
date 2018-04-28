import pytest

from telegram.utils import AsyncResult
from telegram.client import Telegram


API_ID = 1
API_HASH = 'hash'
PHONE = '+71234567890'
LIBRARY_PATH = '/lib/'


@pytest.fixture
def telegram(mocker):
    with mocker.mock_module.patch('telegram.client.TDJson'):
        with mocker.mock_module.patch('telegram.client.threading'):
            tg = Telegram(
                api_id=API_ID,
                api_hash=API_HASH,
                phone=PHONE,
                library_path=LIBRARY_PATH,
            )
    return tg


class TestTelegram(object):
    def test_send_message(self, telegram):
        chat_id = 1
        text = 'Hello world'

        async_result = telegram.send_message(
            chat_id=chat_id,
            text=text,
        )

        exp_data = {
            '@type': 'sendMessage',
            'chat_id': chat_id,
            'input_message_content': {
                '@type': 'inputMessageText',
                'text': {
                    '@type': 'formattedText',
                    'text': text,
                },
            },
            '@extra': {
                'request_id': async_result.id,
            },
        }

        telegram._tdjson.send.assert_called_once_with(exp_data)

    def test_get_chat(self, telegram):
        chat_id = 1

        async_result = telegram.get_chat(chat_id=chat_id)

        exp_data = {
            '@type': 'getChat',
            'chat_id': chat_id,
            '@extra': {
                'request_id': async_result.id,
            },
        }

        telegram._tdjson.send.assert_called_once_with(exp_data)

    def test_get_chats(self, telegram):
        offset_order = 1
        offset_chat_id = 1
        limit = 100

        async_result = telegram.get_chats(
            offset_order=offset_order,
            offset_chat_id=offset_chat_id,
            limit=limit,
        )

        exp_data = {
            '@type': 'getChats',
            'offset_order': offset_order,
            'offset_chat_id': offset_chat_id,
            'limit': limit,
            '@extra': {
                'request_id': async_result.id,
            },
        }

        telegram._tdjson.send.assert_called_once_with(exp_data)

    def test_get_chat_history(self, telegram):
        chat_id = 1
        limit = 100
        from_message_id = 123
        offset = 0
        only_local = False

        async_result = telegram.get_chat_history(
            chat_id=chat_id,
            limit=limit,
            from_message_id=from_message_id,
            offset=offset,
            only_local=only_local,
        )

        exp_data = {
            '@type': 'getChatHistory',
            'chat_id': chat_id,
            'limit': limit,
            'from_message_id': from_message_id,
            'offset': offset,
            'only_local': only_local,
            '@extra': {
                'request_id': async_result.id,
            },
        }

        telegram._tdjson.send.assert_called_once_with(exp_data)

    def test_set_initial_params(self, telegram):
        async_result = telegram._set_initial_params()

        exp_data = {
            '@type': 'setTdlibParameters',
            'parameters': {
                'use_test_dc': False,
                'api_id': API_ID,
                'api_hash': API_HASH,
                'device_model': 'pytd',
                'system_version': 'Unknown',
                'application_version': '0.0.1',
                'system_language_code': 'en',
                'database_directory': f'/tmp/.tdlib_files_{PHONE}/database/',
                'use_message_database': True,
                'files_directory': f'/tmp/.tdlib_files_{PHONE}/files',
            },
            '@extra': {
                'request_id': 'updateAuthorizationState',
            },
        }

        telegram._tdjson.send.assert_called_once_with(exp_data)
        assert async_result.id == 'updateAuthorizationState'


class TestTelegram__update_async_result(object):
    def test_update_async_result_returns_async_result_with_same_id(self, telegram):
        assert telegram._results == {}

        async_result = telegram._send_data(data={})

        assert async_result.id in telegram._results

        update = {
            '@extra': {
                'request_id': async_result.id,
            }
        }
        new_async_result = telegram._update_async_result(update=update)

        assert async_result == new_async_result

    def test_result_id_should_be_replaced_if_it_is_auth_process(self, telegram):
        async_result = AsyncResult(client=telegram, result_id='updateAuthorizationState')
        telegram._results['updateAuthorizationState'] = async_result

        update = {
            '@type': 'updateAuthorizationState',
            '@extra': {
                'request_id': 'blablabla',
            }
        }
        new_async_result = telegram._update_async_result(update=update)

        assert new_async_result.id == 'updateAuthorizationState'


class TestTelegram__login(object):
    def test_login_process_should_do_nothing_if_already_authorized(self, telegram):
        telegram._authorized = True
        telegram.login()

        assert telegram._tdjson.send.call_count == 0

    def test_login_process(self, telegram):
        telegram._authorized = False

        def _get_ar(data):
            ar = AsyncResult(client=telegram)

            ar.update = data

            return ar

        # login process chain
        telegram._set_initial_params = lambda: _get_ar(
            data={'authorization_state': {'@type': 'authorizationStateWaitEncryptionKey'}}
        )
        telegram._send_encryption_key = lambda: _get_ar(
            data={'authorization_state': {'@type': 'authorizationStateWaitPhoneNumber'}}
        )
        telegram._send_phone_number = lambda: _get_ar(
            data={'authorization_state': {'@type': 'authorizationStateWaitCode'}}
        )
        telegram._send_telegram_code = lambda: _get_ar(
            data={'authorization_state': {'@type': 'authorizationStateWaitPassword'}}
        )
        telegram._send_password = lambda: _get_ar(
            data={'authorization_state': {'@type': 'authorizationStateReady'}}
        )

        telegram.login()

        assert telegram._tdjson.send.call_count == 0
