import re
from typing import List, Tuple, Callable

from .const import (
    CHINESE_CHARS,
    ENGLISH_CHARS,
    DIGITS,
    DELIMITERS,
)


def generate_replacer(
    sorted_ranges: List[Tuple[int, int]],
) -> Callable[[str, str], str]:

    def ranges_to_pattern(sorted_ranges: List[Tuple[int, int]]) -> str:
        inner = [
            rf'{chr(lb)}-{chr(ub)}'
            for lb, ub in sorted_ranges
        ]
        joined_inner = ''.join(inner)
        return rf'[{joined_inner}]+'

    pattern = re.compile(ranges_to_pattern(sorted_ranges), re.UNICODE)

    def replacer(text: str, repl: str = '') -> str:
        return pattern.sub(repl, text)

    return replacer


replace_chinese_chars = generate_replacer(CHINESE_CHARS)
replace_english_chars = generate_replacer(ENGLISH_CHARS)
replace_digits = generate_replacer(DIGITS)
replace_delimiters = generate_replacer(DELIMITERS)
