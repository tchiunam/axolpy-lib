import threading
from collections import defaultdict


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


class ImmutableDict(dict):
    """
    Immutable dictionary.
    """

    def __hash__(self):
        return id(self)

    def _immutable(self, *args, **kwargs):
        raise TypeError('object is immutable')

    __setitem__ = _immutable
    __delitem__ = _immutable
    clear = _immutable
    update = _immutable
    setdefault = _immutable
    pop = _immutable
    popitem = _immutable


class KeyDefaultDict(defaultdict):
    """
    A defaultdict that passes the key to default factory.
    """

    def __missing__(self, key):
        if self.default_factory is None:
            raise KeyError(key)
        else:
            self[key] = value = self.default_factory(key)
            return value
