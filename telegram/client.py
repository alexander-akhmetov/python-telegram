import time
import queue
import signal
import typing
import getpass
import logging
import threading
from typing import Dict, List, Callable, Any, Optional, Type

from telegram.utils import AsyncResult
from telegram.tdjson import TDJson
from telegram.worker import BaseWorker, SimpleWorker

logger = logging.getLogger(__name__)


class Telegram(object):
    def __init__(self,
                 api_id: int,
                 api_hash: str,
                 phone: str,
                 library_path: str = None,
                 worker: Optional[Type[BaseWorker]] = None) -> None:
        """
        Args:
            api_id - ID of your app (https://my.telegram.org/apps/)
            api_hash - api_hash of your app (https://my.telegram.org/apps/)
            phone - your phone number
            library_path - you can change path to the compiled libtdjson library
            worker - worker to process updates
        """
        self.api_id = api_id
        self.api_hash = api_hash
        self.library_path = library_path
        self.phone = phone
        self._authorized = False
        self._is_enabled = False
        self._queue: queue.Queue = queue.Queue()

        self._workers_queue: queue.Queue = queue.Queue()
        if not worker:
            worker = SimpleWorker
        self.worker = worker(queue=self._workers_queue)

        self._results: Dict[str, AsyncResult] = {}
        self._message_handlers: List[Callable] = []
        self._update_handlers: List[Callable] = []

        self._tdjson = TDJson(library_path=library_path)
        self._run()

    def __del__(self):
        if hasattr(self, '_tdjson'):
            self._tdjson.stop()

    def send_message(self, chat_id: int, text: str) -> AsyncResult:
        """
        Sends a message to a chat

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
                'text': {
                    '@type': 'formattedText',
                    'text': text,
                },
            },
        }
        return self._send_data(data)

    def get_chat(self, chat_id: int) -> AsyncResult:
        """This is offline request, if there is no chat in your database it will not be found"""
        data = {
            '@type': 'getChat',
            'chat_id': chat_id,
        }
        return self._send_data(data)

    def get_chats(self,
                  offset_order: int = 0,
                  offset_chat_id: int = 0,
                  limit: int = 100) -> AsyncResult:
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

    def get_chat_history(self,
                         chat_id: int,
                         limit: int = 1000,
                         from_message_id: int = 0,
                         offset: int = 0,
                         only_local: bool = False):
        data = {
            '@type': 'getChatHistory',
            'chat_id': chat_id,
            'limit': limit,
            'from_message_id': from_message_id,
            'offset': offset,
            'only_local': only_local,
        }
        return self._send_data(data)

    def _run(self):
        self._is_enabled = True

        self._td_listener = threading.Thread(target=self._listen_to_td)
        self._td_listener.daemon = True
        self._td_listener.start()

        self.worker.run()

    def _listen_to_td(self):
        logger.info('[Telegram.td_listener] started')
        while self._is_enabled:
            update = self._tdjson.receive()
            if update:
                self._queue.put(update)
                self._update_async_result(update)
                self._run_handlers(update)

    def _update_async_result(self, update: dict) -> typing.Optional[AsyncResult]:
        async_result = None

        _special_types = ('updateAuthorizationState', )  # for authorizationProcess @extra.request_id doesn't work
        if update.get('@type') in _special_types:
            request_id = update['@type']
        else:
            request_id = update.get('@extra', {}).get('request_id')

        if not request_id:
            logger.debug('request_id has not been found in the update')
        else:
            async_result = self._results.get(request_id)

        if not async_result:
            logger.debug(f'async_result has not been found in by request_id={request_id}')
        else:
            async_result._parse_update(update)

        return async_result

    def _run_handlers(self, update: Dict[Any, Any]) -> None:
        if update.get('@type') == 'updateNewMessage':
            for handler in self._message_handlers:
                self._workers_queue.put((handler, update))

    def add_message_handler(self, func: Callable) -> None:
        if func not in self._message_handlers:
            self._message_handlers.append(func)

    def _send_data(self, data: dict, result_id: str = None) -> AsyncResult:
        if '@extra' not in data:
            data['@extra'] = {}

        if not result_id and 'request_id' in data['@extra']:
            result_id = data['@extra']['request_id']

        async_result = AsyncResult(
            client=self,
            result_id=result_id,
        )
        data['@extra']['request_id'] = async_result.id

        self._tdjson.send(data)
        self._results[async_result.id] = async_result
        async_result.request = data
        return async_result

    def idle(self, stop_signals=(signal.SIGINT, signal.SIGTERM, signal.SIGABRT)):
        """Blocks until one of the signals are received and stops"""
        for sig in stop_signals:
            signal.signal(sig, self._signal_handler)

        self._is_enabled = True

        while self._is_enabled:
            time.sleep(1)

    def _signal_handler(self, signum, frame):
        self._is_enabled = False

    def login(self):
        """Login process (blocking)"""
        authorization_state = None
        actions = {
            None: self._set_initial_params,
            'authorizationStateWaitTdlibParameters': self._set_initial_params,
            'authorizationStateWaitEncryptionKey': self._send_encryption_key,
            'authorizationStateWaitPhoneNumber': self._send_phone_number,
            'authorizationStateWaitCode': self._send_telegram_code,
            'authorizationStateWaitPassword': self._send_password,
            'authorizationStateReady': self._complete_authorization,
        }

        while not self._authorized:
            logger.info(f'Current state: {authorization_state}')
            result = actions[authorization_state]()
            if result:
                result.wait(raise_exc=True)
                authorization_state = result.update['authorization_state']['@type']

    def _set_initial_params(self) -> AsyncResult:
        data = {
            # todo: params
            '@type': 'setTdlibParameters',
            'parameters': {
                'use_test_dc': False,
                'api_id': self.api_id,
                'api_hash': self.api_hash,
                'device_model': 'pytd',
                'system_version': 'Unknown',
                'application_version': '0.0.1',
                'system_language_code': 'en',
                'database_directory': f'.tdlib_files_{self.phone}/database/',
                'use_message_database': True,
                'files_directory': f'.tdlib_files_{self.phone}/files',
            }
        }
        return self._send_data(data, result_id='updateAuthorizationState')

    def _send_encryption_key(self) -> AsyncResult:
        data = {
            '@type': 'checkDatabaseEncryptionKey',
            'encryption_key': 'changeme1234',
        }
        return self._send_data(data, result_id='updateAuthorizationState')

    def _send_phone_number(self) -> AsyncResult:
        data = {
            '@type': 'setAuthenticationPhoneNumber',
            'phone_number': self.phone,
            'allow_flash_call': False,
            'is_current_phone_number': True,
        }
        return self._send_data(data, result_id='updateAuthorizationState')

    def _send_telegram_code(self) -> AsyncResult:
        code = input('Enter code:')
        data = {
            '@type': 'checkAuthenticationCode',
            'code': str(code),
        }
        return self._send_data(data, result_id='updateAuthorizationState')

    def _send_password(self) -> AsyncResult:
        password = getpass.getpass('Password:')
        data = {
            '@type': 'checkAuthenticationPassword',
            'password': password,
        }
        return self._send_data(data, result_id='updateAuthorizationState')

    def _complete_authorization(self) -> None:
        self._authorized = True
