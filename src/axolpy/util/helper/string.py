import hashlib
import re
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
