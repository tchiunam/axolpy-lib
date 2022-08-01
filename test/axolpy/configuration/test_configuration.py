import os
from pathlib import Path

import pytest
from axolpy.configuration import AxolpyConfigManager


class TestAxolpyConfigManager(object):
    """
    Test Axolpy configuration manager.
    """

    def test_get_basepath(self, axolpy_path) -> None:
        """
        Test getting the base path.

        :param axolpy_path: *axolpy_path* fixture.
        :type axolpy_path: :class:`pathlib.Path`
        """

        basepath = AxolpyConfigManager.get_basepath()
        assert basepath == axolpy_path

        del os.environ["AXOLPY_PATH"]
        basepath = AxolpyConfigManager.get_basepath()
        assert basepath == Path("~/axolpy")

        os.environ["AXOLPY_PATH"] = str(axolpy_path)

    def test_config_path(self) -> None:
        """
        Test getting the configuration path.
        """

        basepath = AxolpyConfigManager.get_basepath()
        config_path = AxolpyConfigManager.get_config_path()
        assert config_path == Path(basepath, "conf")

    def test_get_context(self, axolpy_path) -> None:
        """
        Test getting the context configuration.

        :param axolpy_path: *axolpy_path* fixture.
        :type axolpy_path: :class:`pathlib.Path`
        """

        # Test with exsiting config file
        config = AxolpyConfigManager.get_context("library")
        assert config.get("main", "basepath") == str(axolpy_path)
        assert config["borrow_list"]["book"] == "The Book of John Doe"

        # Test with non-exsiting config file
        with pytest.raises(FileNotFoundError):
            AxolpyConfigManager.get_context("notexists")
