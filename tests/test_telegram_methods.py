import pytest

from unittest.mock import patch

from telegram import VERSION
from telegram.utils import AsyncResult
from telegram.client import Telegram, MESSAGE_HANDLER_TYPE, AuthorizationState

API_ID = 1
API_HASH = 'hash'
PHONE = '+71234567890'
LIBRARY_PATH = '/lib/'
DATABASE_ENCRYPTION_KEY = 'changeme1234'


@pytest.fixture
def telegram():
    with patch('telegram.client.TDJson'):
        with patch('telegram.client.threading'):
            return _get_telegram_instance()


def _get_telegram_instance(**kwargs):
    kwargs.setdefault('api_id', API_ID)
    kwargs.setdefault('api_hash', API_HASH)
    kwargs.setdefault('phone', PHONE)
    kwargs.setdefault('library_path', LIBRARY_PATH)
    kwargs.setdefault('database_encryption_key', DATABASE_ENCRYPTION_KEY)

    with patch('telegram.client.TDJson'):
        with patch('telegram.client.threading'):
            tg = Telegram(**kwargs)

    return tg


class TestTelegram:
    def test_phone_bot_token_init(self):
        with pytest.raises(ValueError) as excinfo:
            Telegram(
                api_id=API_ID,
                api_hash=API_HASH,
                library_path=LIBRARY_PATH,
                database_encryption_key=DATABASE_ENCRYPTION_KEY,
            )
            assert 'You must provide bot_token or phone' in str(excinfo.value)

    def test_send_message(self, telegram):
        chat_id = 1
        text = 'Hello world'

        async_result = telegram.send_message(chat_id=chat_id, text=text)

        exp_data = {
            '@type': 'sendMessage',
            'chat_id': chat_id,
            'input_message_content': {
                '@type': 'inputMessageText',
                'text': {'@type': 'formattedText', 'text': text},
            },
            '@extra': {'request_id': async_result.id},
        }

        telegram._tdjson.send.assert_called_once_with(exp_data)

    def test_send_phone_number_or_bot_token(self, telegram):
        # check that the dunction calls _send_phone_number or _send_bot_token
        with patch.object(telegram, '_send_phone_number'), patch.object(
            telegram, '_send_bot_token'
        ):

            telegram.phone = '123'
            telegram.bot_token = None

            telegram._send_phone_number_or_bot_token()

            telegram._send_phone_number.assert_called_once()
            assert telegram._send_bot_token.call_count == 0

            telegram.phone = None
            telegram.bot_token = 'some-token'

            telegram._send_phone_number_or_bot_token()
            telegram._send_bot_token.assert_called_once()

    def test_send_bot_token(self, telegram):
        telegram.bot_token = 'some-token'

        with patch.object(telegram, '_send_data'):
            telegram._send_bot_token()

            exp_data = {'@type': 'checkAuthenticationBotToken', 'token': 'some-token'}
            telegram._send_data.assert_called_once_with(
                exp_data, result_id='updateAuthorizationState'
            )

    def test_add_message_handler(self, telegram):
        # check that add_message_handler
        # appends passed function to _update_handlers[MESSAGE_HANDLER_TYPE] list
        assert telegram._update_handlers[MESSAGE_HANDLER_TYPE] == []

        def my_handler():
            pass

        telegram.add_message_handler(my_handler)

        assert telegram._update_handlers[MESSAGE_HANDLER_TYPE] == [my_handler]

    def test_remove_update_handler(self, telegram):
        # check remove_update_handler
        assert telegram._update_handlers[MESSAGE_HANDLER_TYPE] == []

        def my_handler():
            pass

        telegram.add_message_handler(my_handler)

        telegram.remove_update_handler(MESSAGE_HANDLER_TYPE, my_handler)

        assert telegram._update_handlers[MESSAGE_HANDLER_TYPE] == []

    def test_remove_update_handler_empty_handlers_list(self, telegram):
        telegram._update_handlers = {}

        def my_handler():
            pass

        telegram.remove_update_handler(MESSAGE_HANDLER_TYPE, my_handler)

        assert telegram._update_handlers == {}

    def test_add_update_handler(self, telegram):
        # check that add_update_handler function
        # appends passsed func to _update_handlers[type] list
        my_update_type = 'update'
        assert telegram._update_handlers[my_update_type] == []

        def my_handler():
            pass

        telegram.add_update_handler(my_update_type, my_handler)

        assert telegram._update_handlers[my_update_type] == [my_handler]

    def test_run_handlers(self, telegram):
        def my_handler():
            pass

        telegram.add_message_handler(my_handler)

        with patch.object(telegram._workers_queue, 'put') as mocked_put:
            update = {'@type': MESSAGE_HANDLER_TYPE}
            telegram._run_handlers(update)

            mocked_put.assert_called_once_with((my_handler, update), timeout=10)

    def test_run_handlers_should_not_be_called_for_another_update_type(self, telegram):
        def my_handler():
            pass

        telegram.add_message_handler(my_handler)

        with patch.object(telegram._workers_queue, 'put') as mocked_put:
            update = {'@type': 'some-type'}
            telegram._run_handlers(update)

            assert mocked_put.call_count == 0

    def test_call_method(self, telegram):
        method_name = 'someMethod'
        params = {'param_1': 'value_1', 'param_2': 2}

        async_result = telegram.call_method(method_name=method_name, params=params)

        exp_data = {'@type': method_name, '@extra': {'request_id': async_result.id}}
        exp_data.update(params)

        telegram._tdjson.send.assert_called_once_with(exp_data)

    def test_get_web_page_instant_view(self, telegram):
        url = 'https://yandex.ru/'
        force_full = False

        async_result = telegram.get_web_page_instant_view(
            url=url, force_full=force_full
        )

        exp_data = {
            '@type': 'getWebPageInstantView',
            'url': url,
            'force_full': force_full,
            '@extra': {'request_id': async_result.id},
        }

        telegram._tdjson.send.assert_called_once_with(exp_data)

    def test_get_me(self, telegram):
        async_result = telegram.get_me()

        exp_data = {'@type': 'getMe', '@extra': {'request_id': async_result.id}}

        telegram._tdjson.send.assert_called_once_with(exp_data)

    def test_get_user(self, telegram):
        user_id = 1

        async_result = telegram.get_user(user_id=user_id)

        exp_data = {
            '@type': 'getUser',
            'user_id': user_id,
            '@extra': {'request_id': async_result.id},
        }

        telegram._tdjson.send.assert_called_once_with(exp_data)

    def test_get_user_full_info(self, telegram):
        user_id = 1

        async_result = telegram.get_user_full_info(user_id=user_id)

        exp_data = {
            '@type': 'getUserFullInfo',
            'user_id': user_id,
            '@extra': {'request_id': async_result.id},
        }

        telegram._tdjson.send.assert_called_once_with(exp_data)

    def test_get_chat(self, telegram):
        chat_id = 1

        async_result = telegram.get_chat(chat_id=chat_id)

        exp_data = {
            '@type': 'getChat',
            'chat_id': chat_id,
            '@extra': {'request_id': async_result.id},
        }

        telegram._tdjson.send.assert_called_once_with(exp_data)

    def test_get_chats(self, telegram):
        offset_order = 1
        offset_chat_id = 1
        limit = 100

        async_result = telegram.get_chats(
            offset_order=offset_order, offset_chat_id=offset_chat_id, limit=limit
        )

        exp_data = {
            '@type': 'getChats',
            'offset_order': offset_order,
            'offset_chat_id': offset_chat_id,
            'limit': limit,
            '@extra': {'request_id': async_result.id},
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
            '@extra': {'request_id': async_result.id},
        }

        telegram._tdjson.send.assert_called_once_with(exp_data)

    def test_set_initial_params(self, telegram):
        async_result = telegram._set_initial_params()
        phone_md5 = '69560384b84c896952ef20352fbce705'

        exp_data = {
            '@type': 'setTdlibParameters',
            'parameters': {
                'use_test_dc': False,
                'api_id': API_ID,
                'api_hash': API_HASH,
                'device_model': 'python-telegram',
                'system_version': 'unknown',
                'application_version': VERSION,
                'system_language_code': 'en',
                'database_directory': f'/tmp/.tdlib_files/{phone_md5}/database',
                'use_message_database': True,
                'files_directory': f'/tmp/.tdlib_files/{phone_md5}/files',
                'use_secret_chats': True,
            },
            '@extra': {'request_id': 'updateAuthorizationState'},
        }

        telegram._tdjson.send.assert_called_once_with(exp_data)
        assert async_result.id == 'updateAuthorizationState'

    @pytest.mark.parametrize(
        'key, exp_key',
        [('key', 'a2V5'), (b'byte-key', 'Ynl0ZS1rZXk='), ('', ''), (b'', '')],
    )
    def test_send_encryption_key(self, key, exp_key):
        # check that _send_encryption_key calls tdlib with
        # correct parameters encoded using base64
        tg = _get_telegram_instance(database_encryption_key=key)

        tg._send_encryption_key()

        exp_data = {
            '@type': 'checkDatabaseEncryptionKey',
            'encryption_key': exp_key,
            '@extra': {'request_id': 'updateAuthorizationState'},
        }

        tg._tdjson.send.assert_called_once_with(exp_data)


class TestTelegram__update_async_result:
    def test_update_async_result_returns_async_result_with_same_id(self, telegram):
        assert telegram._results == {}

        async_result = telegram._send_data(data={})

        assert async_result.id in telegram._results

        update = {'@extra': {'request_id': async_result.id}}
        new_async_result = telegram._update_async_result(update=update)

        assert async_result == new_async_result

    def test_result_id_should_be_replaced_if_it_is_auth_process(self, telegram):
        async_result = AsyncResult(
            client=telegram, result_id='updateAuthorizationState'
        )
        telegram._results['updateAuthorizationState'] = async_result

        update = {
            '@type': 'updateAuthorizationState',
            '@extra': {'request_id': 'blablabla'},
        }
        new_async_result = telegram._update_async_result(update=update)

        assert new_async_result.id == 'updateAuthorizationState'


class TestTelegram__login:
    def test_login_process_should_do_nothing_if_already_authorized(self, telegram):
        telegram.authorization_state = AuthorizationState.READY
        telegram.login()

        assert telegram._tdjson.send.call_count == 0

    def test_login_process_with_phone(self, telegram):
        telegram.authorization_state = AuthorizationState.NONE

        def _get_async_result(data, request_id=None):
            result = AsyncResult(client=telegram)

            result.update = data
            result._ready.set()
            result.id = request_id

            return result

        # login process chain
        telegram.get_authorization_state = lambda: _get_async_result(
            data={'@type': 'authorizationStateWaitTdlibParameters'},
            request_id='getAuthorizationState',
        )

        telegram._set_initial_params = lambda: _get_async_result(
            data={
                'authorization_state': {'@type': 'authorizationStateWaitEncryptionKey'}
            }
        )
        telegram._send_encryption_key = lambda: _get_async_result(
            data={'authorization_state': {'@type': 'authorizationStateWaitPhoneNumber'}}
        )
        telegram._send_phone_number_or_bot_token = lambda: _get_async_result(
            data={'authorization_state': {'@type': 'authorizationStateWaitCode'}}
        )
        telegram._send_telegram_code = lambda: _get_async_result(
            data={'authorization_state': {'@type': 'authorizationStateWaitPassword'}}
        )
        telegram._send_password = lambda: _get_async_result(
            data={'authorization_state': {'@type': 'authorizationStateReady'}}
        )

        telegram.login()

        assert telegram._tdjson.send.call_count == 0


class TestTelegram__login_non_blocking:
    def test_login_process_with_phone(self, telegram):
        telegram.authorization_state = AuthorizationState.NONE

        def _get_async_result(data, request_id=None):
            result = AsyncResult(client=telegram)

            result.update = data
            result._ready.set()
            result.id = request_id

            return result

        # login process chain
        telegram.get_authorization_state = lambda: _get_async_result(
            data={'@type': 'authorizationStateWaitTdlibParameters'},
            request_id='getAuthorizationState',
        )

        telegram._set_initial_params = lambda: _get_async_result(
            data={
                'authorization_state': {'@type': 'authorizationStateWaitEncryptionKey'}
            }
        )
        telegram._send_encryption_key = lambda: _get_async_result(
            data={'authorization_state': {'@type': 'authorizationStateWaitPhoneNumber'}}
        )
        telegram._send_phone_number_or_bot_token = lambda: _get_async_result(
            data={'authorization_state': {'@type': 'authorizationStateWaitCode'}}
        )
        telegram._send_telegram_code = lambda _: _get_async_result(
            data={'authorization_state': {'@type': 'authorizationStateWaitRegistration'}}
        )
        telegram._register_user = lambda _, __: _get_async_result(
            data={'authorization_state': {'@type': 'authorizationStateWaitPassword'}}
        )
        telegram._send_password = lambda _: _get_async_result(
            data={'authorization_state': {'@type': 'authorizationStateReady'}}
        )

        state = telegram.login(blocking=False)
        assert state == AuthorizationState.WAIT_CODE
        telegram.send_code('123')

        state = telegram.login(blocking=False)
        assert state == AuthorizationState.WAIT_REGISTRATION
        telegram.register_user('new', 'user')

        state = telegram.login(blocking=False)
        assert state == AuthorizationState.WAIT_PASSWORD
        telegram.send_password('456')

        state = telegram.login(blocking=False)
        assert state == telegram.authorization_state == AuthorizationState.READY

        assert telegram._tdjson.send.call_count == 0
