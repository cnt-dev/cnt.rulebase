"""Replacers"""
import re
from typing import List, Tuple, Callable

from cnt.rulebase import const


def _generate_replacer(sorted_ranges: List[Tuple[int, int]]) -> Callable[[str, str], str]:

    def ranges_to_pattern(sorted_ranges: List[Tuple[int, int]]) -> str:
        inner = [f'{chr(lb)}-{chr(ub)}' for lb, ub in sorted_ranges]
        joined_inner = ''.join(inner)
        return f'[{joined_inner}]+'

    pattern = re.compile(ranges_to_pattern(sorted_ranges), re.UNICODE)

    def replacer(text: str, repl: str = '') -> str:
        return pattern.sub(repl, text)

    return replacer


# pylint: disable=invalid-name
replace_chinese_chars = _generate_replacer(const.CHINESE_CHARS)
replace_english_chars = _generate_replacer(const.ENGLISH_CHARS)
replace_digits = _generate_replacer(const.DIGITS)
replace_delimiters = _generate_replacer(const.DELIMITERS)
