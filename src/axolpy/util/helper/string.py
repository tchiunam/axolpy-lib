import hashlib
import random
import re
import string
from itertools import chain
from typing import Iterable


def camelcase_to_underscrollsep(string: str) -> str:
    """
    Convert a *string* from camelcase to underscroll sepearated.

    :param string: This is a string to be converted.
    :type string: str

    :return: Converted string.
    :rtype: str
    """

    return re.sub(r"(^|[a-z])([A-Z])", lambda m: "_".join([i.lower() for i in m.groups() if i]), string)


def expand_range(string: str) -> Iterable[int]:
    """
    Expand the range in *string*.

    :param string: String of range.
    :type string: str

    :return: Expanded range.
    :rtype: Iterable[int]
    """

    spans = (element.partition("-")[::2] for element in string.split(","))
    ranges = (range(int(start), int(end) + 1 if end else int(start) + 1)
              for start, end in spans)
    return chain.from_iterable(ranges)


def increase_number_in_string(string: str, value: int) -> str:
    """
    Increase numbers in *string* by the increment *value*.

    :param string: String to be processed.
    :type string: str
    :param value: Increment value.
    :type: int

    :return: String after increment
    :rtype: str
    """

    return re.sub(r"\d+", lambda x: str(int(x.group()) + value), string)


def get_string_hex(input_string: str) -> str:
    """
    Get hashed value of *input_string*.

    :param input_string: String to be hashed.
    :type input_string: str

    :return: Hashed string.
    :rtype: str
    """

    hash_object = hashlib.md5(input_string.encode())
    return hash_object.hexdigest()


def multiple_replace(string: str, rep: dict) -> str:
    """
    Replacement of *string* with multiple patterns.

    :param string: String to be processed.
    :type string: str
    :param rep: Match and replace patterns.
    :type rep: dict

    :return: String after replacement.
    :rtype: str
    """

    pattern = re.compile("|".join([re.escape(k) for k in rep.keys()]), re.M)
    return pattern.sub(lambda x: rep[x.group(0)], string)


def generate_random_string(
        length: int,
        with_letters=True,
        with_digits=False,
        with_punctuation=False) -> str:
    """
    Generate random string with *length*. If all the options are False, then
    the string will be generated with letters only.

    :param length: Length of random string.
    :type length: int
    :param with_letters: Whether to include letters in the random string. Default is True.
    :type with_letters: bool
    :param with_digits: Whether to include digits in the random string.
    :type with_digits: bool
    :param with_punctuation: Whether to include punctuation in the random string.
    :type with_punctuation: bool

    :return: Random string.
    :rtype: str
    """

    s = string.ascii_letters if with_letters else ""
    s += string.digits if with_digits else ""
    s += string.punctuation if with_punctuation else ""

    # Must have at least letters
    if not s:
        s = string.ascii_letters

    return "".join(random.choice(s) for _ in range(length))
