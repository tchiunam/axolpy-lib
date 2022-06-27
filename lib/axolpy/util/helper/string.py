import hashlib
import re

__all__ = ["camelcase_to_underscore", "get_string_hex", "multiple_replace"]


def camelcase_to_underscrollsep(string: str) -> str:
    """
    Convert a *string* from camelcase to underscroll sepearated.

    :param string: This is a string to be converted.
    :type string: str

    :return: Converted string.
    :rtype: str
    """

    return re.sub(r"(^|[a-z])([A-Z])", lambda m: "_".join([i.lower() for i in m.groups() if i]), string)


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
