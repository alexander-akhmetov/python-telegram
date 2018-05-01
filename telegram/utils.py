import uuid
import time


class AsyncResult(object):
    """
    tdlib is asynchronous, and this class helps you get results back.
    After each API call, you receive AsyncResult object, which you can use to get results back.
    """
    def __init__(self, client, result_id=None):
        self.client = client

        if result_id:
            self.id = result_id
        else:
            self.id = uuid.uuid4().hex

        self.request = None
        self.ok_received = False
        self.error = False
        self.error_info = None
        self.update = None

    def __str__(self):
        return f'AsyncResult <{self.id}>'

    def wait(self, timeout: int = None, raise_exc: bool = False) -> None:
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

    def _parse_update(self, update: dict) -> None:
        if update.get('@type') == 'ok':
            self.ok_received = True
        elif update.get('@type') == 'error':
            self.error = True
            self.error_info = update
        else:
            self.update = update
