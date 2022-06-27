import random
import time

__all__ = ["get_random_bits", "get_timestamp_string"]


def get_random_bits(bits: int = 128) -> str:
    """
    Get random bits in hex.

    :param bits: Number of bits.
    :type bits: int

    :return: Random bits.
    :rtype: str
    """

    assert bits % 8 == 0
    required_length = bits / 8 * 2
    s = hex(random.getrandbits(bits)).lstrip("0x").rstrip("L")
    if len(s) < required_length:
        return get_random_bits(bits)
    else:
        return s


def get_timestamp_string(date_separator: str = "", time_separator: str = "", component_separator: str = "") -> str:
    """
    Get timestamp in a compact string format.

    :param date_separator: Separator within date components.
    :type date_separator: str
    :param time_separator: Separator within time components.
    :type time_separator: str
    :param component_separator: Separator between date / time components.
    :type component_separator: str

    :return: Current timestamp string in "%Y%m%d%H%M%S" format.
    :rtype: str
    """

    return time.strftime("%Y{0}%m{0}%d{1}%H{2}%M{2}%S".format(date_separator,
                                                              component_separator,
                                                              time_separator), time.localtime())
