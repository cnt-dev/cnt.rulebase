"""
Consts for detecting sentence endings.
"""
from typing import Union, Iterable, List, Any, Optional

from cnt.rulebase import const


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


def _append_single_quotation(seq: Union[str, List[str]]) -> List[str]:
    return _append_code_points_to_seq(seq, 0xFF07, 0x2019, 0x2032)


def _append_double_quotation(seq: Union[str, List[str]]) -> List[str]:
    return _append_code_points_to_seq(seq, 0xFF02, 0x201D, 0x2033)


def _generate_sentence_ends() -> List[str]:
    # mostly fullwidth endings.
    ends = _flatten_nested([
            # size 3.
            _append_double_quotation('？！'),
            _append_double_quotation('……'),
            _append_double_quotation(_append_single_quotation('。')),
            _append_double_quotation(_append_single_quotation('！')),

            # size 2.
            _append_double_quotation('。'),
            _append_double_quotation('！'),
            _append_double_quotation('？'),
            _append_double_quotation('；'),
            '？！',

            # size 1.
            '…',
            '。',
            '！',
            '？',
            '；',
    ])
    # add corresponding halfwidth.
    ends = _flatten_nested([set((end, const.fullwidth_to_halfwidth(end))) for end in ends])

    return ends


#: For detecting valid characters of sentence.
ITV_SENTENCE_VALID_CHARS = const.sorted_chain(
        const.ITV_CHINESE_CHARS,
        const.ITV_ENGLISH_CHARS,
        const.ITV_DIGITS,
        const.ITV_DELIMITERS,
)

#: For detecting sentence endings.
EM_SENTENCE_ENDINGS = _generate_sentence_ends()
