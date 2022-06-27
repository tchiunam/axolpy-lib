import random

__all__ = ["get_timestamp_string"]


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
