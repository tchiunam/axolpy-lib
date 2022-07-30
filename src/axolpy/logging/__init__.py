import logging
from pathlib import Path

import yaml
from axolpy.configuration import AxolpyConfigManager

__all__ = ["CRITICAL", "FATAL", "ERROR",
           "WARNING", "WARN", "INFO", "DEBUG", "NOTSET",
           "get_logger", "set_level"]

CRITICAL = logging.CRITICAL
FATAL = logging.FATAL
ERROR = logging.ERROR
WARNING = logging.WARNING
WARN = logging.WARN
INFO = logging.INFO
DEBUG = logging.DEBUG
NOTSET = logging.NOTSET


def load_config() -> None:
    """
    Load the logging configuration.
    """

    logging_config_file = Path(
        AxolpyConfigManager.get_config_path(), "logging.yaml")
    if logging_config_file.exists():
        logging.config.dictConfig(yaml.load(logging_config_file))
    else:
        raise FileNotFoundError(
            "Logging configuration file 'logging.yaml' not found $AXOLPY_PATH/conf")


class AxolpyLogger(logging.Logger):
    """
    An Axolpy logger class.
    """

    def __init__(self, name: str = None) -> None:
        """
        Initialize the logger.

        :param name: Name of the logger.
        :type name: str
        """

        super().__init__(name)


def get_logger(name: str = None) -> AxolpyLogger:
    """
    Return a logger with the specified *name*.

    :param name: Name of the logger.
    :type name: str

    :return: A logger class.
    :rtype: :class:`AxolpyLogger`
    """

    return AxolpyLogger(name=name)
