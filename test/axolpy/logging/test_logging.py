import pytest
from axolpy import logging


def test_load_config() -> None:
    """
    Test if logging configuration can be loaded.
    """

    logging.load_config()

    assert logging.get_logger(
        name="console").level == logging.INFO, "Logger level is incorrect"

    # Test with non-existing configuration file
    with pytest.raises(FileNotFoundError):
        logging.load_config(filename="nosuchfile.txt")


def test_get_logger() -> None:
    """
    Test to get a logger.
    """

    logger = logging.get_logger(name="Test Logger")
    assert logger is not None, "Logger obtained is None"
    assert logger.name == "Test-Logger", "Name of the logger obtained is incorrect"
    assert logger.level == logging.INFO, "Level of the logger obtained is incorrect"

    logger = logging.get_logger(level=logging.DEBUG)
    assert logger is not None, "Logger obtained is None"
    assert logger.name == "console", "Name of the logger obtained is incorrect"
    assert logger.level == logging.DEBUG, "Level of the logger obtained is incorrect"
