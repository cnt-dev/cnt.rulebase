"""
Consts for detecting chinese chars.
"""
from cnt.rulebase.const import utils

#: English Chars.
ITV_ENGLISH_CHARS = utils.sorted_chain(
        # ASCII_ALPHA_RANGES
        [
                (0x0041, 0x005A),
                (0x0061, 0x007A),
        ],
        # ALPHA_EXTENSION_RANGES
        [
                (0xFF21, 0xFF3A),
                (0xFF41, 0xFF5A),
        ],
)
