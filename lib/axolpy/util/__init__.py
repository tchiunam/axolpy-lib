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
