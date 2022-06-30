import logging
from typing import Any

__all__ = ["CRITICAL", "FATAL", "ERROR",
           "WARNING", "WARN", "INFO", "DEBUG", "NOTSET",
           "show_milliseconds", "get_logger", "set_level"]

CRITICAL = logging.CRITICAL
FATAL = logging.FATAL
ERROR = logging.ERROR
WARNING = logging.WARNING
WARN = logging.WARN
INFO = logging.INFO
DEBUG = logging.DEBUG
NOTSET = logging.NOTSET


def show_milliseconds() -> None:
    """
    Show milliseconds in log.
    """

    import coloredlogs
    coloredlogs.install(milliseconds=True)


def get_logger(name: str = None) -> logging.Logger:
    """
    Return a logger with the specified *name*.

    :param name: Name of the logger.
    :type name: str

    :return: A logger class.
    :rtype: :class:`logging.Logger`
    """

    return logging.getLogger(name)


def set_level(level: int = INFO) -> None:
    """
    Set the logging level.

    :param level: Logging level to be set to.
    :type level: int
    """

    import coloredlogs
    coloredlogs.install(level=level)


def get_level() -> Any | int:
    """
    Get the current logging level.

    :return: The current logging level.
    :rtype: int
    """

    import coloredlogs
    return coloredlogs.get_level()
