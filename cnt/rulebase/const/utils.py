"""Utils functions"""
import itertools
from typing import Iterable, List, Tuple


def sorted_chain(*ranges: Iterable[Tuple[int, int]]) -> List[Tuple[int, int]]:
    """Chain & sort ranges."""
    return sorted(itertools.chain(*ranges))


def fullwidth_to_halfwidth(seq: str) -> str:
    """Conver fullwith chars to halfwidth."""

    def convert(char: str) -> str:
        code_point = ord(char)
        if not 0xFF01 <= code_point <= 0xFF5E:
            return char
        return chr(code_point - 0xFEE0)

    return ''.join(map(convert, seq))
