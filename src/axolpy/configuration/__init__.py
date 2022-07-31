import os
from configparser import ConfigParser
from pathlib import Path


class AxolpyConfigManager(object):
    """
    Manage configurations to be loaded and used.
    """

    @staticmethod
    def get_basepath() -> Path:
        """
        Get the base path of Axolpy.

        :return: The base path of Axolpy.
        :rtype: :class:`pathlib.Path`
        """

        return Path(os.getenv("AXOLPY_PATH", "~/axolpy"))

    @staticmethod
    def get_config_path() -> Path:
        """
        Get the path to configuration files.

        :return: The path to configuration files.
        :rtype: :class:`pathlib.Path`
        """

        return Path(AxolpyConfigManager.get_basepath(), "conf")

    @staticmethod
    def get_context(name: str = "axolpy") -> ConfigParser:
        """
        Get configuration of a context *name*.

        :param name: Context name. Default is "axolpy".
        :type name: str

        :return: Context configuration.
        :rtype: :class:`ConfigParser`
        """

        config = ConfigParser()
        conf_path = AxolpyConfigManager.get_config_path()
        config_file = conf_path / f"{name}.ini"
        if config_file.exists():
            config.read(config_file)
        else:
            raise FileNotFoundError(
                f"Configuration file {config_file} not found.")

        # Add the base path to the configuration.
        if "main" not in config:
            config.add_section("main")
        config["main"]["basepath"] = str(AxolpyConfigManager.get_basepath())

        return config
