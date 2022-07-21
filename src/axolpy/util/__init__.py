import errno
import os
import signal
from functools import wraps


def synchronous(tlockname: str):
    """
    A decorator to place an instance based lock around a method.

    :param tlockname: Name of the thread lock.
    :type tlockname: str

    :return: Wrapper of the associated function.
    """

    def _synched(func):
        """
        Synchronization with a lock on specified *func*.

        :return: Synchronous function.
        """

        @wraps(func)
        def _synchronizer(self, *args, **kwargs):
            """
            Wrapper of *func* that acquires a lock before processing.

            :return: Return value the associated function.
            """

            tlock = self.__getattribute__(tlockname)
            with tlock:
                return func(self, *args, **kwargs)

        return _synchronizer

    return _synched


def timeout(seconds=10, error_message=os.strerror(errno.ETIME)):
    """
    Timeout a function.

    :param seconds: Number of seconds. Default is 10.
    :type seconds: int
    :param error_message: Error message to be raised.
    :type error_message: str

    :return: Wrapper of the associated function.
    """

    def decorator(func):
        """
        Decorator.

        :return: Function with the enforcement.
        """

        # noinspection PyUnusedLocal
        def _handle_timeout(signum, frame):
            raise TimeoutError(error_message)

        def wrapper(*args, **kwargs):
            """
            Wrapper.

            :return: Return value of the associated function.
            """

            signal.signal(signal.SIGALRM, _handle_timeout)
            signal.alarm(seconds)
            try:
                result = func(*args, **kwargs)
            finally:
                signal.alarm(0)
            return result

        return wraps(func)(wrapper)

    return decorator
