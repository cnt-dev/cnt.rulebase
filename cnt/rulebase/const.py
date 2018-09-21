"""Constants."""
from typing import Union, Iterable, List, Any, Optional

from cnt.rulebase import utils


def _flatten_nested(seq: Iterable[Any], ret: Optional[List[Any]] = None) -> List[Any]:
    if ret is None:
        ret = []
    for item in seq:
        if not isinstance(item, (list, tuple, set)):
            ret.append(item)
        else:
            _flatten_nested(item, ret)
    return ret


def _append_code_points_to_text(text: str, *code_points: int) -> List[str]:
    return [text + chr(cp) for cp in code_points]


def _append_code_points_to_seq(seq: Union[str, List[str]], *code_points: int) -> List[str]:
    if isinstance(seq, str):
        seq = [seq]
    return _flatten_nested([_append_code_points_to_text(text, *code_points) for text in seq])


def _single_quotation(seq: Union[str, List[str]]) -> List[str]:
    return _append_code_points_to_seq(seq, 0xFF07, 0x2019, 0x2032)


def _double_quotation(seq: Union[str, List[str]]) -> List[str]:
    return _append_code_points_to_seq(seq, 0xFF02, 0x201D, 0x2033)


SENTENCE_ENDS = _flatten_nested([
        # size 3.
        _double_quotation('？！'),
        _double_quotation('……'),
        _double_quotation(_single_quotation('。')),
        _double_quotation(_single_quotation('！')),

        # size 2.
        _double_quotation('。'),
        _double_quotation('！'),
        _double_quotation('？'),
        _double_quotation('；'),
        '？！',

        # size 1.
        '…',
        '。',
        '！',
        '？',
        '；',
])
# add normalized endings.
SENTENCE_ENDS = _flatten_nested(
        [set((
                end,
                utils.fullwidth_to_halfwidth(end),
        )) for end in SENTENCE_ENDS])

# English Chars.
ENGLISH_CHARS = utils.sorted_chain(
        # ASCII_ALPHA_RANGES
        [
                (0x0041, 0x005A),
                (0x0061, 0x007A),
        ],
        # ALPHA_EXTENSION_RANGES
        [
                (0xFF21, 0xFF3A),
                (0xFF41, 0xFF5A),
        ])

# Digits.
DIGITS = utils.sorted_chain(
        # ASCII_DIGIT_RANGES
        [
                (0x0030, 0x0039),
        ],
        # DIGIT_EXTENSION_RANGES
        [
                (0xFF10, 0xFF19),
        ],
)

# Delimiters.
DELIMITERS = utils.sorted_chain(
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

# Chinese Chars.
# pull from https://www.qqxiuzi.cn/zh/hanzi-unicode-bianma.php
# notice 3007 a delimiter, hence should not be included.
#
# lines = '''copy paste'''
# [l.split('\t') for l in lines.strip().split('\n')]
#
CHINESE_CHARS = utils.sorted_chain([
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
])
