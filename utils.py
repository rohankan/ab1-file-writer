from typing import List


def int_to_16_bit(num: int) -> bytes:
    """
    Converts Python integer to 16-bit instance.
    :param num: Python integer
    :return: 16-bit integer
    """
    return num.to_bytes(2, "big")


def int_to_32_bit(num: int) -> bytes:
    """
    Converts Python integer to 32-bit instance
    :param num: Python integer
    :return: 32-bit int
    """
    return num.to_bytes(4, "big")


def short_list(values: List[int]) -> bytearray:
    """
    Converts list of ints to a byte array of shorts, two bytes for each int.
    :param values: List of ints
    :return: Byte array of shorts
    """
    return bytearray(y for x in values for y in bytearray(x.to_bytes(2, "big")))


def pascal_string(value: str) -> bytes:
    """
    Converts string value to a pString, or Pascal string.
    :param value: Python string object
    :return: Pascal string
    """
    if len(value) > 256:
        print("{} must be below 1 byte (256 chars)!".format(value))

    length = len(value).to_bytes(1, "big")
    utf8 = value.encode()
    return length + utf8
