import threading


class ThreadSafeDict(dict):
    """
    Thread-safe dictionary.
    """

    def __init__(self, seq=None, **kwargs):
        super().__init__(self, seq=seq, **kwargs)
        self._lock = threading.Lock()

    def __enter__(self) -> 'ThreadSafeDict':
        self._lock.acquire()
        return self

    # noinspection PyUnusedLocal
    def __exit__(self, type_, value, traceback) -> None:
        self._lock.release()
