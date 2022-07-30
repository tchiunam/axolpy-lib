from axolpy import logging


def test_load_config() -> None:
    """
    Test if logging configuration can be loaded.
    """

    logging.load_config()
    assert logging.get_level() == logging.DEBUG


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
