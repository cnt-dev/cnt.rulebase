import re

from .const import (
    CHINESE_CHARS,
    ENGLISH_CHARS,
    DIGITS,
    DELIMITERS,
)


def generate_replacer(sorted_ranges):

    def ranges_to_pattern(sorted_ranges):
        inner = [
            rf'{chr(lb)}-{chr(ub)}'
            for lb, ub in sorted_ranges
        ]
        inner = ''.join(inner)
        return rf'[{inner}]+'

    pattern = re.compile(ranges_to_pattern(sorted_ranges), re.UNICODE)

    def replacer(text, repl=''):
        return pattern.sub(repl, text)

    return replacer


replace_chinese_chars = generate_replacer(CHINESE_CHARS)
replace_english_chars = generate_replacer(ENGLISH_CHARS)
replace_digits = generate_replacer(DIGITS)
replace_delimiters = generate_replacer(DELIMITERS)
