import os
from configparser import ConfigParser


class AxolpyConfigManager(object):
    """
    Manage configurations to be loaded and used.
    """

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
        base_path = os.getenv(
            "AXOLPY_PATH", os.path.expanduser("~/axolpy"))
        config.read(
            os.path.sep.join([base_path, "conf", name + ".ini"]))
        config["main"]["base_path"] = base_path

        return config
