import time
import uuid
from typing import TYPE_CHECKING, Any, Dict, Optional

if TYPE_CHECKING:
    from telegram.client import Telegram  # noqa  pylint: disable=cyclic-import


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

    def __str__(self) -> str:
        return f'AsyncResult <{self.id}>'

    def wait(self, timeout: Optional[int] = None, raise_exc: bool = False) -> None:
        """
        Blocking method to wait for the result
        """
        started_at = time.time()
        while True:
            if self.update or self.error:
                if raise_exc and self.error:
                    raise RuntimeError(f'Telegram error: {self.error_info}')
                return
            time.sleep(0.01)
            if timeout and time.time() - started_at > timeout:
                raise TimeoutError()

    def parse_update(self, update: Dict[Any, Any]) -> None:
        if update.get('@type') == 'ok':
            self.ok_received = True
        elif update.get('@type') == 'error':
            self.error = True
            self.error_info = update
        else:
            self.update = update
