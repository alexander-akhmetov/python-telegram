import logging
import threading
from queue import Empty, Queue

logger = logging.getLogger(__name__)

# a handler that never returns must not hold up the shutdown, and at interpreter
# exit it would hold up the interpreter itself
JOIN_TIMEOUT: float = 5.0


class BaseWorker:
    """
    Base worker class.
    Each worker must implement the run method to start listening to the queue
    and calling handler functions
    """

    def __init__(self, queue: Queue):
        self._is_enabled = True
        self._queue = queue

    def run(self) -> None:
        raise NotImplementedError()

    def stop(self) -> None:
        raise NotImplementedError()


class SimpleWorker(BaseWorker):
    """Simple one-thread worker"""

    def run(self) -> None:
        thread = threading.Thread(target=self._run_thread)
        thread.daemon = True
        thread.start()

        # a thread that failed to start must stay invisible to `stop`: joining it raises
        self._thread = thread

    def _run_thread(self) -> None:
        logger.info("[SimpleWorker] started")

        while self._is_enabled:
            try:
                handler, update = self._queue.get(timeout=0.5)
            except Empty:
                continue

            try:
                handler(update)
            except Exception:
                logger.exception("Error in update handler %s", handler)
            self._queue.task_done()

    def stop(self) -> None:
        self._is_enabled = False

        # `_thread` only exists after `run`
        thread = getattr(self, "_thread", None)
        if thread is None:
            return

        if threading.current_thread() is thread:
            # a handler calling stop() runs on this thread, and joining it raises
            return

        thread.join(timeout=JOIN_TIMEOUT)

        if thread.is_alive():
            logger.warning("[SimpleWorker] an update handler is still running after %s seconds", JOIN_TIMEOUT)
