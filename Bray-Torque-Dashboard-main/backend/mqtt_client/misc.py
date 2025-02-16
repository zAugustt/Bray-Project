"""
Miscellaneous Function Module

Contains miscellaneous functions that did not fit the structure of the rest of the program.

Authors:
    Aidan Queng (jaidanqueng@gmail.com), Texas A&M University

Date:
    November 2024
"""

from collections.abc import Iterable
from typing import List


def cstr_to_str(data: Iterable[bytes]) -> str:
    """
    Converts a c-style string to a python string

    Args:
        data (Iterable[bytes]): Iterable containing bytes of c-style string

    Returns:
        str: python string
    """
    result: str = ""

    for b in data:
        if b == b"\x00":
            break

        result += b.decode()

    return result
