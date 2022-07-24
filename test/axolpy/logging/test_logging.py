from axolpy import logging


def test_show_milliseconds() -> None:
    """
    Test to enable logger to show milliseconds.
    """

    try:
        logging.show_milliseconds()
    except Exception as exc:
        assert False, f"show_milliseconds raised an exception {exc}"


def test_get_logger() -> None:
    """
    Test to get a logger.
    """

    logger = logging.get_logger(name="TestLogger")
    assert logger is not None, "Logger obtained is None"
    assert logger.name == "TestLogger", "Name of the logger obtained is incorrect"


def test_set_level() -> None:
    """
    Test if logging level can be configured.
    """

    logger = logging.get_logger(name="TestLogger")
    for level in [logging.logging.CRITICAL,
                  logging.FATAL,
                  logging.ERROR,
                  logging.WARNING,
                  logging.WARN,
                  logging.INFO,
                  logging.DEBUG,
                  logging.NOTSET]:
        logging.set_level(level=level)
        assert logging.get_level() == level
