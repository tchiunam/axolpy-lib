import re
from pathlib import Path

import pytest
from axolpy.util import helper


def test_is_text_file():
    """
    Test to check if a file is a text file.
    """

    # Test with a text file
    with Path(__file__).parent.joinpath("testdata", "textfile.txt").open("rb") as f:
        assert helper.is_text_file(f), "File is not a text file"

    # Test with a binary file
    with Path(__file__).parent.joinpath("testdata", "axolpy-logo-small.png").open("rb") as f:
        assert not helper.is_text_file(f), "File is a text file"

    # Test with an empty file
    with Path(__file__).parent.joinpath("testdata", "emptyfile.txt").open("rb") as f:
        assert helper.is_text_file(f), "File is not a text file"


def test_get_random_bits() -> None:
    """
    Test to get random bits.
    """

    assert len(helper.get_random_bits(bits=64)
               ) == 16, "Random bits are not 64 bits"
    assert len(helper.get_random_bits()) == 32, "Random bits are not 32 bits"


def test_get_timestamp_string() -> None:
    """
    Test to get timestamp string.
    """

    s = helper.get_timestamp_string(
        date_separator="/",
        time_separator=":",
        component_separator="-")
    assert re.match(
        r"^\d{4}/\d{2}/\d{2}-\d{2}:\d{2}:\d{2}", s), "Timestamp string is not correct"


@pytest.fixture
def animal_tree() -> dict:
    return {"animal": {"reptile": {"lizard": "salamander",
                                   "bird": {"canary": "tweetle"}},
                       "mammal": {"dog": "poodle",
                                  "cat": "tabby",
                                  "horse": "filly",
                                  "bovine": {"cow": "bessie"}}}}


def test_set_leaf(animal_tree) -> None:
    """
    Test to set a leaf within a nested dictionary.
    """

    helper.set_leaf(animal_tree, ["animal", "mammal", "horse"], {
                    "stallion": "buck"})
    assert animal_tree["animal"]["mammal"]["horse"]["stallion"] == "buck", "Leaf not set"
