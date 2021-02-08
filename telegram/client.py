import os
import hashlib
import time
import queue
import signal
import typing
import getpass
import logging
import base64
import threading
from typing import (
    Any,
    Dict,
    List,
    Type,
    Callable,
    Optional,
    DefaultDict,
    Union,
    Tuple,
)
from types import FrameType
from collections import defaultdict
import enum

from telegram import VERSION
from telegram.utils import AsyncResult
from telegram.tdjson import TDJson
from telegram.worker import BaseWorker, SimpleWorker

logger = logging.getLogger(__name__)


MESSAGE_HANDLER_TYPE: str = 'updateNewMessage'


class AuthorizationState(enum.Enum):
    NONE = None
    WAIT_CODE = 'authorizationStateWaitCode'
    WAIT_PASSWORD = 'authorizationStateWaitPassword'
    WAIT_TDLIB_PARAMETERS = 'authorizationStateWaitTdlibParameters'
    WAIT_ENCRYPTION_KEY = 'authorizationStateWaitEncryptionKey'
    WAIT_PHONE_NUMBER = 'authorizationStateWaitPhoneNumber'
    READY = 'authorizationStateReady'
    CLOSING = 'authorizationStateClosing'
    CLOSED = 'authorizationStateClosed'


class Telegram:
    def __init__(
        self,
        api_id: int,
        api_hash: str,
        database_encryption_key: Union[str, bytes],
        phone: Optional[str] = None,
        bot_token: Optional[str] = None,
        library_path: Optional[str] = None,
        worker: Optional[Type[BaseWorker]] = None,
        files_directory: Optional[str] = None,
        use_test_dc: bool = False,
        use_message_database: bool = True,
        device_model: str = 'python-telegram',
        application_version: str = VERSION,
        system_version: str = 'unknown',
        system_language_code: str = 'en',
        login: bool = False,
        default_workers_queue_size: int = 1000,
        tdlib_verbosity: int = 2,
        proxy_server: str = '',
        proxy_port: int = 0,
        proxy_type: Optional[Dict[str, str]] = None,
        use_secret_chats: bool = True,
    ) -> None:
        """
        Args:
            api_id - ID of your app (https://my.telegram.org/apps/)
            api_hash - api_hash of your app (https://my.telegram.org/apps/)
            phone - your phone number
            library_path - you can change path to the compiled libtdjson library
            worker - worker to process updates
            files_directory - directory for the tdlib's files (database, images, etc.)
            use_test_dc - use test datacenter
            use_message_database
            use_secret_chats
            device_model
            application_version
            system_version
            system_language_code
        """
        self.api_id = api_id
        self.api_hash = api_hash
        self.library_path = library_path
        self.phone = phone
        self.bot_token = bot_token
        self.use_test_dc = use_test_dc
        self.device_model = device_model
        self.system_version = system_version
        self.system_language_code = system_language_code
        self.application_version = application_version
        self.use_message_database = use_message_database
        self._queue_put_timeout = 10
        self.proxy_server = proxy_server
        self.proxy_port = proxy_port
        self.proxy_type = proxy_type
        self.use_secret_chats = use_secret_chats
        self.authorization_state = AuthorizationState.NONE

        if not self.bot_token and not self.phone:
            raise ValueError('You must provide bot_token or phone')

        self._database_encryption_key = database_encryption_key

        if not files_directory:
            hasher = hashlib.md5()
            str_to_encode: str = self.phone or self.bot_token  # type: ignore
            hasher.update(str_to_encode.encode('utf-8'))
            directory_name = hasher.hexdigest()
            files_directory = f'/tmp/.tdlib_files/{directory_name}/'

        self.files_directory = files_directory

        self._authorized = False
        self._stopped = threading.Event()

        # todo: move to worker
        self._workers_queue: queue.Queue = queue.Queue(maxsize=default_workers_queue_size)

        if not worker:
            worker = SimpleWorker
        self.worker: BaseWorker = worker(queue=self._workers_queue)

        self._results: Dict[str, AsyncResult] = {}
        self._update_handlers: DefaultDict[str, List[Callable]] = defaultdict(list)

        self._tdjson = TDJson(library_path=library_path, verbosity=tdlib_verbosity)
        self._run()

        if login:
            self.login()

    def stop(self) -> None:
        """Stops the client"""
        if self._stopped.is_set():
            return

        logger.info('Stopping telegram client...')

        self._close()
        self.worker.stop()
        self._stopped.set()

        # wait for the tdjson listener to stop
        self._td_listener.join()

        if hasattr(self, '_tdjson'):
            self._tdjson.stop()

    def _close(self) -> None:
        """
        Calls `close` tdlib method and waits until authorization_state becomes CLOSED.
        Blocking.
        """
        self.call_method('close')

        while self.authorization_state != AuthorizationState.CLOSED:
            result = self.get_authorization_state()
            self.authorization_state = self._wait_authorization_result(result)
            logger.info('Authorization state: %s', self.authorization_state)
            time.sleep(0.5)

    def send_message(self, chat_id: int, text: str) -> AsyncResult:
        """
        Sends a message to a chat. The chat must be in the tdlib's database.
        If there is no chat in the DB, tdlib returns an error.
        Chat is being saved to the database when the client receives a message or when you call the `get_chats` method.

        Args:
            chat_id
            text

        Returns:
            AsyncResult
            The update will be:
                {
                    '@type': 'message',
                    'id': 1,
                    'sender_user_id': 2,
                    'chat_id': 3,
                    ...
                }
        """
        data = {
            '@type': 'sendMessage',
            'chat_id': chat_id,
            'input_message_content': {
                '@type': 'inputMessageText',
                'text': {'@type': 'formattedText', 'text': text},
            },
        }

        return self._send_data(data)

    def get_chat(self, chat_id: int) -> AsyncResult:
        """
        This is offline request, if there is no chat in your database it will not be found
        tdlib saves chat to the database when it receives a new message or when you call `get_chats` method.
        """
        data = {'@type': 'getChat', 'chat_id': chat_id}

        return self._send_data(data)

    def get_me(self) -> AsyncResult:
        """
        Requests information of the current user (getMe method)

        https://core.telegram.org/tdlib/docs/classtd_1_1td__api_1_1get_me.html
        """

        return self.call_method('getMe')

    def get_user(self, user_id: int) -> AsyncResult:
        """
        Requests information about a user with id = user_id.

        https://core.telegram.org/tdlib/docs/classtd_1_1td__api_1_1get_user.html
        """

        return self.call_method('getUser', params={'user_id': user_id})

    def get_chats(self, offset_order: int = 0, offset_chat_id: int = 0, limit: int = 100) -> AsyncResult:
        """
        Returns a list of chats:

        Returns:
            {
                '@type': 'chats',
                'chat_ids': [...],
                '@extra': {
                    'request_id': '...'
                }
            }
        """
        data = {
            '@type': 'getChats',
            'offset_order': offset_order,
            'offset_chat_id': offset_chat_id,
            'limit': limit,
        }

        return self._send_data(data)

    def get_chat_history(
        self,
        chat_id: int,
        limit: int = 1000,
        from_message_id: int = 0,
        offset: int = 0,
        only_local: bool = False,
    ) -> AsyncResult:
        """
        Returns history of a chat

        Args:
            chat_id
            limit
            from_message_id
            offset
            only_local
        """
        data = {
            '@type': 'getChatHistory',
            'chat_id': chat_id,
            'limit': limit,
            'from_message_id': from_message_id,
            'offset': offset,
            'only_local': only_local,
        }

        return self._send_data(data)

    def get_message(
        self,
        chat_id: int,
        message_id: int,
    ) -> AsyncResult:
        """
        Return a message via its message_id

        Args:
            chat_id
            message_id

        Returns:
            AsyncResult
            The update will be:
                {
                    '@type': 'message',
                    'id': 1,
                    'sender_user_id': 2,
                    'chat_id': 3,
                    'content': {...},
                    ...
                }
        """
        data = {
            '@type': 'getMessage',
            'chat_id': chat_id,
            'message_id': message_id,
        }
        return self._send_data(data)

    def delete_messages(self, chat_id: int, message_ids: List[int], revoke: bool = True) -> AsyncResult:
        """
        Delete a list of messages in a chat

        Args:
            chat_id
            message_ids
            revoke
        """
        return self._send_data(
            {
                '@type': 'deleteMessages',
                'chat_id': chat_id,
                'message_ids': message_ids,
                'revoke': revoke,
            }
        )

    def get_supergroup_full_info(self, supergroup_id: int) -> AsyncResult:
        """
        Get the full info of a supergroup

        Args:
            supergroup_id
        """
        return self._send_data({'@type': 'getSupergroupFullInfo', 'supergroup_id': supergroup_id})

    def create_basic_group_chat(self, basic_group_id: int) -> AsyncResult:
        """
        Create a chat from a basic group

        Args:
            basic_group_id
        """
        return self._send_data({'@type': 'createBasicGroupChat', 'basic_group_id': basic_group_id})

    def get_web_page_instant_view(self, url: str, force_full: bool = False) -> AsyncResult:
        """
        Use this method to request instant preview of a webpage.
        Returns error with 404 if there is no preview for this webpage.

        Args:
            url: URL of a webpage
            force_full: If true, the full instant view for the web page will be returned
        """
        data = {'@type': 'getWebPageInstantView', 'url': url, 'force_full': force_full}

        return self._send_data(data)

    def call_method(
        self,
        method_name: str,
        params: Optional[Dict[str, Any]] = None,
        block: bool = False,
    ) -> AsyncResult:
        """
        Use this method to call any other method of the tdlib

        Args:
            method_name: Name of the method
            params: parameters
        """
        data = {'@type': method_name}

        if params:
            data.update(params)

        return self._send_data(data, block=block)

    def _run(self) -> None:
        self._td_listener = threading.Thread(target=self._listen_to_td)
        self._td_listener.daemon = True
        self._td_listener.start()

        self.worker.run()

    def _listen_to_td(self) -> None:
        logger.info('[Telegram.td_listener] started')

        while not self._stopped.is_set():
            update = self._tdjson.receive()

            if update:
                self._update_async_result(update)
                self._run_handlers(update)

    def _update_async_result(self, update: Dict[Any, Any]) -> typing.Optional[AsyncResult]:
        async_result = None

        _special_types = ('updateAuthorizationState',)  # for authorizationProcess @extra.request_id doesn't work

        if update.get('@type') in _special_types:
            request_id = update['@type']
        else:
            request_id = update.get('@extra', {}).get('request_id')

        if not request_id:
            logger.debug('request_id has not been found in the update')
        else:
            async_result = self._results.get(request_id)

        if not async_result:
            logger.debug('async_result has not been found in by request_id=%s', request_id)
        else:
            done = async_result.parse_update(update)
            if done:
                self._results.pop(request_id, None)

        return async_result

    def _run_handlers(self, update: Dict[Any, Any]) -> None:
        update_type: str = update.get('@type', 'unknown')
        for handler in self._update_handlers[update_type]:
            self._workers_queue.put((handler, update), timeout=self._queue_put_timeout)

    def remove_update_handler(self, handler_type: str, func: Callable) -> None:
        """
        Remove a handler with the specified type
        """
        try:
            self._update_handlers[handler_type].remove(func)
        except (ValueError, KeyError):
            # not in the list
            pass

    def add_message_handler(self, func: Callable) -> None:
        self.add_update_handler(MESSAGE_HANDLER_TYPE, func)

    def add_update_handler(self, handler_type: str, func: Callable) -> None:
        if func not in self._update_handlers[handler_type]:
            self._update_handlers[handler_type].append(func)

    def _send_data(
        self,
        data: Dict[Any, Any],
        result_id: Optional[str] = None,
        block: bool = False,
    ) -> AsyncResult:
        """
        Sends data to tdlib.

        If `block`is True, waits for the result
        """
        if '@extra' not in data:
            data['@extra'] = {}

        if not result_id and 'request_id' in data['@extra']:
            result_id = data['@extra']['request_id']

        async_result = AsyncResult(client=self, result_id=result_id)
        data['@extra']['request_id'] = async_result.id
        self._results[async_result.id] = async_result
        self._tdjson.send(data)
        async_result.request = data

        if block:
            async_result.wait(raise_exc=True)

        return async_result

    def idle(
        self,
        stop_signals: Tuple = (
            signal.SIGINT,
            signal.SIGTERM,
            signal.SIGABRT,
            signal.SIGQUIT,
        ),
    ) -> None:
        """
        Blocks until one of the exit signals is received.
        When a signal is received, calls `stop`.
        """
        for sig in stop_signals:
            signal.signal(sig, self._stop_signal_handler)

        self._stopped.wait()

    def _stop_signal_handler(self, signum: int, frame: FrameType) -> None:
        logger.info('Signal %s received!', signum)
        self.stop()

    def get_authorization_state(self) -> AsyncResult:
        logger.debug('Getting authorization state')
        data = {'@type': 'getAuthorizationState'}

        return self._send_data(data, result_id='getAuthorizationState')

    def _wait_authorization_result(self, result: AsyncResult) -> AuthorizationState:
        authorization_state = None
        if result:
            result.wait(raise_exc=True)

            if result.update is None:
                raise RuntimeError('Something wrong, the result update is None')

            if result.id == 'getAuthorizationState':
                authorization_state = result.update['@type']
            else:
                authorization_state = result.update['authorization_state']['@type']

        return AuthorizationState(authorization_state)

    def login(self, blocking: bool = True) -> AuthorizationState:
        """
        Login process.

        Must be called before any other call.
        It sends initial params to the tdlib, sets database encryption key, etc.

        args:
          blocking [bool]: If True, the process is blocking and the client
                           expects password and code from stdin.
                           If False, `login` call returns next AuthorizationState and
                           the login process can be continued (with calling login(blocking=False) again)
                           after the necessary action is completed.

        Returns:
         - AuthorizationState.WAIT_CODE if a telegram code is required.
           The caller should ask the telegram code
           to the end user then call send_code(code)
         - AuthorizationState.WAIT_PASSWORD if a telegram password is required.
           The caller should ask the telegram password
           to the end user and then call send_password(password)
         - AuthorizationState.READY if the login process scceeded.
        """
        if self.proxy_server:
            self._send_add_proxy()

        actions: Dict[AuthorizationState, Callable[[], AsyncResult]] = {
            AuthorizationState.NONE: self.get_authorization_state,
            AuthorizationState.WAIT_TDLIB_PARAMETERS: self._set_initial_params,
            AuthorizationState.WAIT_ENCRYPTION_KEY: self._send_encryption_key,
            AuthorizationState.WAIT_PHONE_NUMBER: self._send_phone_number_or_bot_token,
            AuthorizationState.WAIT_CODE: self._send_telegram_code,
            AuthorizationState.WAIT_PASSWORD: self._send_password,
        }

        blocking_actions = (
            AuthorizationState.WAIT_CODE,
            AuthorizationState.WAIT_PASSWORD,
        )

        if self.phone:
            logger.info('[login] Login process has been started with phone')
        else:
            logger.info('[login] Login process has been started with bot token')

        while self.authorization_state != AuthorizationState.READY:
            logger.info('[login] current authorization state: %s', self.authorization_state)

            if not blocking and self.authorization_state in blocking_actions:
                return self.authorization_state

            result = actions[self.authorization_state]()
            if not isinstance(result, AuthorizationState):
                self.authorization_state = self._wait_authorization_result(result)
            else:
                self.authorization_state = result

        return self.authorization_state

    def _set_initial_params(self) -> AsyncResult:
        logger.info(
            'Setting tdlib initial params: files_dir=%s, test_dc=%s',
            self.files_directory,
            self.use_test_dc,
        )
        data = {
            # todo: params
            '@type': 'setTdlibParameters',
            'parameters': {
                'use_test_dc': self.use_test_dc,
                'api_id': self.api_id,
                'api_hash': self.api_hash,
                'device_model': self.device_model,
                'system_version': self.system_version,
                'application_version': self.application_version,
                'system_language_code': self.system_language_code,
                'database_directory': os.path.join(self.files_directory, 'database'),
                'use_message_database': self.use_message_database,
                'files_directory': os.path.join(self.files_directory, 'files'),
                'use_secret_chats': self.use_secret_chats,
            },
        }

        return self._send_data(data, result_id='updateAuthorizationState')

    def _send_encryption_key(self) -> AsyncResult:
        logger.info('Sending encryption key')

        key = self._database_encryption_key
        if isinstance(key, str):
            key = key.encode()

        data = {
            '@type': 'checkDatabaseEncryptionKey',
            'encryption_key': base64.b64encode(key).decode(),
        }

        return self._send_data(data, result_id='updateAuthorizationState')

    def _send_phone_number_or_bot_token(self) -> AsyncResult:
        """Sends phone number or a bot_token"""
        if self.phone:
            return self._send_phone_number()
        elif self.bot_token:
            return self._send_bot_token()
        else:
            raise RuntimeError('Unknown mode: both bot_token and phone are None')

    def _send_phone_number(self) -> AsyncResult:
        logger.info('Sending phone number')
        data = {
            '@type': 'setAuthenticationPhoneNumber',
            'phone_number': self.phone,
            'allow_flash_call': False,
            'is_current_phone_number': True,
        }

        return self._send_data(data, result_id='updateAuthorizationState')

    def _send_add_proxy(self) -> AsyncResult:
        logger.info('Sending addProxy')
        data = {
            '@type': 'addProxy',
            'server': self.proxy_server,
            'port': self.proxy_port,
            'enable': True,
            'type': self.proxy_type,
        }
        return self._send_data(data, result_id='setProxy')

    def _send_bot_token(self) -> AsyncResult:
        logger.info('Sending bot token')
        data = {'@type': 'checkAuthenticationBotToken', 'token': self.bot_token}

        return self._send_data(data, result_id='updateAuthorizationState')

    def _send_telegram_code(self, code: Optional[str] = None) -> AsyncResult:
        logger.info('Sending code')
        if code is None:
            code = input('Enter code:')
        data = {'@type': 'checkAuthenticationCode', 'code': str(code)}

        return self._send_data(data, result_id='updateAuthorizationState')

    def send_code(self, code: str) -> AuthorizationState:
        """
        Verifies a telegram code and continues the authorization process

        Args:
          code: the code to be verified. If code is None, it will be asked to the user using the input() function

        Returns
         - AuthorizationState. The called have to call `login` to continue the login process.

        Raises:
         - RuntimeError if the login failed
        """
        result = self._send_telegram_code(code)
        self.authorization_state = self._wait_authorization_result(result)

        return self.authorization_state

    def _send_password(self, password: Optional[str] = None) -> AsyncResult:
        logger.info('Sending password')
        if password is None:
            password = getpass.getpass('Password:')
        data = {'@type': 'checkAuthenticationPassword', 'password': password}

        return self._send_data(data, result_id='updateAuthorizationState')

    def send_password(self, password: str) -> AuthorizationState:
        """
        Verifies a telegram password and continues the authorization process

        Args:
          password the password to be verified.
          If password is None, it will be asked to the user using the getpass.getpass() function

        Returns
         - AuthorizationState. The called have to call `login` to continue the login process.

        Raises:
          - RuntimeError if the login failed

        """
        result = self._send_password(password)
        self.authorization_state = self._wait_authorization_result(result)

        return self.authorization_state
