import re

import pytest
from axolpy.util import helper


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
