import uuid
import threading
import logging
from typing import TYPE_CHECKING, Any, Dict, Optional

if TYPE_CHECKING:
    from telegram.client import Telegram  # noqa  pylint: disable=cyclic-import


logger = logging.getLogger(__name__)


class AsyncResult:
    """
    tdlib is asynchronous, and this class helps you get results back.
    After each API call, you receive AsyncResult object, which you can use to get results back.
    """

    def __init__(self, client: 'Telegram', result_id: Optional[str] = None) -> None:
        self.client = client

        if result_id:
            self.id = result_id
        else:
            self.id = uuid.uuid4().hex

        self.request: Optional[Dict[Any, Any]] = None
        self.ok_received = False
        self.error = False
        self.error_info: Optional[Dict[Any, Any]] = None
        self.update: Optional[Dict[Any, Any]] = None
        self._ready = threading.Event()

    def __str__(self) -> str:
        return f'AsyncResult <{self.id}>'

    def wait(self, timeout: Optional[int] = None, raise_exc: bool = False) -> None:
        """
        Blocking method to wait for the result
        """
        result = self._ready.wait(timeout=timeout)
        if result is False:
            raise TimeoutError()
        if raise_exc and self.error:
            raise RuntimeError(f'Telegram error: {self.error_info}')

    def parse_update(self, update: Dict[Any, Any]) -> bool:
        update_type = update.get('@type')

        logger.debug('update id=%s type=%s received', self.id, update_type)

        if update_type == 'ok':
            self.ok_received = True
            if self.id == 'updateAuthorizationState':
                # For updateAuthorizationState commands tdlib sends
                # @type: ok responses
                # but we want to wait longer to receive the new authorization state
                return False
        elif update_type == 'error':
            self.error = True
            self.error_info = update
        else:
            self.update = update

        self._ready.set()

        return True
