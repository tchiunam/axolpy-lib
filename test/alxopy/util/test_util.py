import threading
import time

import pytest
from axolpy.util import synchronous, timeout


def test_synchronous() -> None:
    """
    Test to synchronize a function.
    """

    class Counter:
        """
        A counter that counts down.
        """

        _tlock = threading.Lock()

        def __init__(self):
            self.count = 0

        @synchronous("_tlock")
        def count_down(self) -> None:
            """
            Count down.
            """

            for i in range(10):
                time.sleep(0.1)
                self.count += 1

    counter = Counter()
    # Run counter.count_down twice in parallel
    threads = [threading.Thread(target=counter.count_down) for _ in range(2)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    assert counter.count == 20, "Count is not 20"


def test_timeout() -> None:
    """
    Test to timeout a function.
    """

    @timeout(seconds=1)
    def timeout_function(seconds: int) -> None:
        """
        Timeout function.
        """

        time.sleep(seconds)

    with pytest.raises(Exception) as e:
        timeout_function(seconds=2)
    assert e.type == TimeoutError, "Timeout exception not raised"
