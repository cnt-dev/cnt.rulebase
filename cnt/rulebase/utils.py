"""Utils functions"""
import itertools
import bisect
from typing import Iterable, List, Tuple, Callable


def sorted_chain(*ranges: Iterable[Tuple[int, int]]) -> List[Tuple[int, int]]:
    """Chain & sort ranges."""
    return sorted(itertools.chain(*ranges))


def generate_range_checker(sorted_ranges: List[Tuple[int, int]]) -> Callable[[str], bool]:
    """To check if a char is in ranges."""
    ranges_start = [t[0] for t in sorted_ranges]

    def _char_in_range(char: str) -> bool:
        code_point = ord(char)

        # 1. find a range such that (start, end), start <= code_point.
        idx = bisect.bisect_left(ranges_start, code_point)
        if idx == len(ranges_start) or \
                (idx != 0 and code_point != ranges_start[idx]):
            idx -= 1

        # 2. check if start <= code_point <= end.
        # (to deal with the coner case when idx == 0).
        return sorted_ranges[idx][0] <= code_point <= sorted_ranges[idx][1]

    return _char_in_range


def fullwidth_to_halfwidth(seq: str) -> str:
    """Conver fullwith chars to halfwidth."""

    def convert(char: str) -> str:
        code_point = ord(char)
        if not 0xFF01 <= code_point <= 0xFF5E:
            return char
        return chr(code_point - 0xFEE0)

    return ''.join(map(convert, seq))
