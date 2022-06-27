import io
import random
import time

__all__ = ["is_text_file", "get_random_bits", "get_timestamp_string"]


def is_text_file(cls, file_: io.FileIO, blocksize: int = 512) -> bool:
    """
    Uses heuristics to guess whether the given file is text or binary,
    by reading a single block of bytes from the file.
    If more than 30% of the chars in the block are non-text, or there
    are NUL ('\x00') bytes in the block, assume this is a binary file.

    :param file_: This is a file to check.
    :type file_: io.FileIO
    :param blocksize: Block size to read.
    :type blocksize: int

    :return: True if *file_* is a text file.
    :rtype: bool
    """

    # A function that takes an integer in the 8-bit range and returns
    # a single-character byte object in py3 / a single-character string
    # in py2.
    int2byte = (lambda x: bytes((x,))) if cls.is_py3() else chr

    _text_characters = (
        b''.join(int2byte(i) for i in range(32, 127)) +
        b'\n\r\t\f\b')

    block = file_.read(blocksize)
    if b'\x00' in block:
        # Files with null bytes are binary
        return False
    elif not block:
        # An empty file is considered a valid text file
        return True

    # Use translate's 'deletechars' argument to efficiently remove all
    # occurrences of _text_characters from the block
    non_text = block.translate(None, _text_characters)
    return float(len(non_text)) / len(block) <= 0.30


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
