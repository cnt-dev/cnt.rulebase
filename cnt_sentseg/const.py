import itertools


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
    '：',

    # size 1 ending. en.
    '!',
    '?',
    ';',
]


# basic.
ASCII_ALPHA_RANGES = [
    (0x0041, 0x005A),
    (0x0061, 0x007A),
]

ASCII_DIGIT_RANGES = [
    (0x0030, 0x0039),
]

ASCII_SYMBOLS_AND_PUNCTUATION_RANGES = [
    (0x0021, 0x002F),
    (0x003A, 0x0040),
    (0x005B, 0x0060),
    (0x007B, 0x007E),
]


# extension.
ALPHA_EXTENSION_RANGES = [
    (0xFF21, 0xFF3A),
    (0xFF41, 0xFF5A),
]

DIGIT_EXTENSION_RANGES = [
    (0xFF10, 0xFF19),
]

SYMBOLS_AND_PUNCTUATION_EXTENSION_RANGES = [
    (0xFF00, 0xFF0F),
    (0xFF1A, 0xFF20),
    (0xFF3B, 0xFF40),
    (0xFF5B, 0xFF64),
    (0xFFE0, 0xFFEE),
]

GENERAL_PUNCTUATION_RAGES = [
    (0x2000, 0x206F),
]

# https://en.wikipedia.org/wiki/CJK_Unified_Ideographs
CJK_COMMON_RANGES = [
    (0x4E00, 0x9FFF),
]

CJK_EXTENSION_RANGES = [
    (0x3400, 0x4DFF),
    (0x20000, 0x2A6DF),
    (0x2A700, 0x2B73F),
    (0x2B740, 0x2B81F),
    (0x2B820, 0x2CEAF),
]

CJK_COMPATIBILITY_RANGES = [
    (0x3300, 0x33FF),
    (0xFE30, 0xFE4F),
    (0xF900, 0xFAFF),
    (0x2F800, 0x2FA1F),
]

# https://gist.github.com/shingchi/64c04e0dd2cbbfbc1350
CJK_SYMBOLS_AND_PUNCTUATION_RANGES = [
    # http://www.unicode.org/charts/PDF/U3000.pdf
    (0x3000, 0x303F),
    # http://www.unicode.org/charts/PDF/UFF00.pdf
    (0xFF00, 0xFFEF),
    # http://www.unicode.org/charts/PDF/UFE30.pdf
    (0xFE30, 0xFE4F),
]

CHINESE_ALL = list(itertools.chain(
    ASCII_ALPHA_RANGES,
    ASCII_DIGIT_RANGES,
    ASCII_SYMBOLS_AND_PUNCTUATION_RANGES,
    ALPHA_EXTENSION_RANGES,
    DIGIT_EXTENSION_RANGES,
    SYMBOLS_AND_PUNCTUATION_EXTENSION_RANGES,
    GENERAL_PUNCTUATION_RAGES,
    CJK_COMMON_RANGES,
    CJK_EXTENSION_RANGES,
    CJK_COMPATIBILITY_RANGES,
    CJK_SYMBOLS_AND_PUNCTUATION_RANGES,
))

CHINESE_ALL = sorted(CHINESE_ALL)
CHINESE_ALL_START = [p[0] for p in CHINESE_ALL]
