"""
Consts for detecting delimiter chars.
"""
from cnt.rulebase.const import utils

#: Delimiters.
ITV_DELIMITERS = utils.sorted_chain(
        # ASCII_DELIMITERS_RANGES
        [
                (0x0021, 0x002F),
                (0x003A, 0x0040),
                (0x005B, 0x0060),
                (0x007B, 0x007E),
        ],
        # GENERAL_DELIMITERS_RAGES
        # http://www.unicode.org/charts/PDF/U2000.pdf
        [
                (0x2000, 0x206F),
        ],
        # CJK_DELIMITERS_RANGES
        # http://www.unicode.org/charts/PDF/U3000.pdf
        # http://www.unicode.org/charts/PDF/UFE30.pdf
        [
                (0x3000, 0x303F),
                (0xFE30, 0xFE4F),
        ],
        # DELIMITERS_EXTENSION_RANGES
        # http://www.unicode.org/charts/PDF/UFF00.pdf
        [
                (0xFF01, 0xFF0F),
                (0xFF1A, 0xFF20),
                (0xFF3B, 0xFF40),
                (0xFF5B, 0xFF64),
                (0xFFE0, 0xFFEE),
        ],
)
