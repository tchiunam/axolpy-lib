import logging
import logging.config
import sys
from pathlib import Path

import yaml
from axolpy.configuration import AxolpyConfigManager

__all__ = ["CRITICAL", "FATAL", "ERROR",
           "WARNING", "WARN", "INFO", "DEBUG", "NOTSET",
           "load_config", "get_logger"]

CRITICAL = logging.CRITICAL
FATAL = logging.FATAL
ERROR = logging.ERROR
WARNING = logging.WARNING
WARN = logging.WARN
INFO = logging.INFO
DEBUG = logging.DEBUG
NOTSET = logging.NOTSET


def load_config(filename: str = "logging.yaml") -> None:
    """
    Load the logging configuration.

    :param filename: Name of the configuration file. Default is "logging.yaml".
    :type filename: str
    """

    logging_config_file = Path(
        AxolpyConfigManager.get_config_path(), filename)
    if logging_config_file.exists():
        config = yaml.load(logging_config_file.read_text(),
                           Loader=yaml.FullLoader)
        logging.config.dictConfig(config=config)
    else:
        raise FileNotFoundError(
            "Logging configuration file 'logging.yaml' not found $AXOLPY_PATH/conf")


def get_logger(name: str = None, level: int = None) -> logging.Logger:
    """
    Return a logger with the specified *name*. A new logger will
    be it doesn't exist. Root logger is returned if *name* is None.

    :param name: Name of the logger.
    :type name: str
    :param level: Level of the logger.
    :type level: int

    :return: A logger class.
    :rtype: :class:`logging.Logger`
    """

    default_level = None
    default_name = "root"
    try:
        config = AxolpyConfigManager.get_context()
        if "logging" in config:
            if "logger.default.level" in config["logging"]:
                default_level = getattr(
                    sys.modules[__name__],
                    config["logging"]["logger.default.level"], None)
            if "logger.default.name" in config["logging"]:
                default_name = config["logging"]["logger.default.name"]
    except FileNotFoundError:
        # Do nothing if config of default context is not set
        pass

    if name is None:
        name = default_name
    # Replace spaces with hyphens in the name
    # so that parsing of log is easier
    logger = logging.getLogger(name=name.replace(" ", "-"))
    if level is None:
        if default_level is not None:
            logger.setLevel(default_level)
    else:
        logger.setLevel(level)
    return logger
