import itertools
import bisect


def sorted_chain(*ranges):
    return sorted(itertools.chain(*ranges))


def generate_range_checker(sorted_ranges):

    ranges_start = [t[0] for t in sorted_ranges]

    def _char_in_range(char):
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


SENTENCE_ENDS = [
    # size 3 ending. zh.
    '？！”',
    '。’”',
    '！’”',
    '……”',

    # size 2 ending. zh.
    '。”',
    '！”',
    '？”',
    '；”',
    '？！',

    # size 1 ending. zh.
    '…',
    '。',
    '！',
    '？',
    '；',

    # size 1 ending. en.
    '!',
    '?',
    ';',
]


# English Chars.
ENGLISH_CHARS = sorted_chain(
    # ASCII_ALPHA_RANGES
    [
        (0x0041, 0x005A),
        (0x0061, 0x007A),
    ],
    # ALPHA_EXTENSION_RANGES
    [
        (0xFF21, 0xFF3A),
        (0xFF41, 0xFF5A),
    ]
)


# Digits.
DIGITS = sorted_chain(
    # ASCII_DIGIT_RANGES
    [
        (0x0030, 0x0039),
    ],
    # DIGIT_EXTENSION_RANGES
    [
        (0xFF10, 0xFF19),
    ],
)


# Delimiter.
DELIMITER = sorted_chain(
    # ASCII_DELIMITER_RANGES
    [
        (0x0021, 0x002F),
        (0x003A, 0x0040),
        (0x005B, 0x0060),
        (0x007B, 0x007E),
    ],
    # GENERAL_DELIMITER_RAGES
    # http://www.unicode.org/charts/PDF/U2000.pdf
    [
        (0x2000, 0x206F),
    ],
    # CJK_DELIMITER_RANGES
    # http://www.unicode.org/charts/PDF/U3000.pdf
    # http://www.unicode.org/charts/PDF/UFE30.pdf
    [
        (0x3000, 0x303F),
        (0xFE30, 0xFE4F),
    ],
    # DELIMITER_EXTENSION_RANGES
    # http://www.unicode.org/charts/PDF/UFF00.pdf
    [
        (0xFF01, 0xFF0F),
        (0xFF1A, 0xFF20),
        (0xFF3B, 0xFF40),
        (0xFF5B, 0xFF64),
        (0xFFE0, 0xFFEE),
    ],
)


# Chinese Chars.
# pull from https://www.qqxiuzi.cn/zh/hanzi-unicode-bianma.php
# notice 3007 a delimiter, hence should not be included.
#
# lines = '''copy paste'''
# [l.split('\t') for l in lines.strip().split('\n')]
#
CHINESE_CHARS = sorted_chain(
    [
        (0x4E00, 0x9FA5),
        (0x9FA6, 0x9FEF),
        (0x3400, 0x4DB5),
        (0x20000, 0x2A6D6),
        (0x2A700, 0x2B734),
        (0x2B740, 0x2B81D),
        (0x2B820, 0x2CEA1),
        (0x2CEB0, 0x2EBE0),
        (0x2F00, 0x2FD5),
        (0x2E80, 0x2EF3),
        (0xF900, 0xFAD9),
        (0x2F800, 0x2FA1D),
        (0xE815, 0xE86F),
        (0xE400, 0xE5E8),
        (0xE600, 0xE6CF),
        (0x31C0, 0x31E3),
        (0x2FF0, 0x2FFB),
        (0x3105, 0x312F),
        (0x31A0, 0x31BA),
    ],
)
