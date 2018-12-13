"""Utils functions"""
import itertools
from typing import Iterable, List, Tuple
from cnt.rulebase.const.cjk_compatibility_ideographs import CJK_COMPATIBILITY_IDEOGRAPHS


def sorted_chain(*ranges: Iterable[Tuple[int, int]]) -> List[Tuple[int, int]]:
    """Chain & sort ranges."""
    return sorted(itertools.chain(*ranges))


def normalize_cjk_fullwidth_ascii(seq: str) -> str:
    """
    Conver fullwith ASCII to halfwidth ASCII.
    See https://en.wikipedia.org/wiki/Halfwidth_and_fullwidth_forms
    """

    def convert(char: str) -> str:
        code_point = ord(char)
        if not 0xFF01 <= code_point <= 0xFF5E:
            return char
        return chr(code_point - 0xFEE0)

    return ''.join(map(convert, seq))


def normalize_cjk_compatibility_ideographs(seq: str) -> str:
    return ''.join(chr(CJK_COMPATIBILITY_IDEOGRAPHS.get(ord(char), ord(char))) for char in seq)
