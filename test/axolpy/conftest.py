import os
from pathlib import Path

import pytest


@pytest.fixture(scope="session")
def axolpy_path() -> Path:
    """
    Return the path to the Axolpy directory.

    :return: Path to the Axolpy directory.
    :rtype: :class:`pathlib.Path`
    """

    return Path(__file__).parent.joinpath("testdata", "axolpy_path")


@pytest.fixture(scope="session", autouse=True)
def set_axolpy_path(axolpy_path) -> None:
    """
    Set the AXOLPY_PATH environment variable.

    :param axolpy_path: *axolpy_path* fixture.
    :type axolpy_path: :class:`pathlib.Path`
    """

    env_axolpy_path = None
    env_axolpy_path_configured = True if "AXOLPY_PATH" in os.environ else False
    if env_axolpy_path_configured:
        env_axolpy_path = os.environ["AXOLPY_PATH"]
    os.environ["AXOLPY_PATH"] = str(axolpy_path)

    yield

    if env_axolpy_path_configured:
        os.environ["AXOLPY_PATH"] = env_axolpy_path
    else:
        del os.environ["AXOLPY_PATH"]
