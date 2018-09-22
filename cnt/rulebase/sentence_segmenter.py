"""Sentence segmenter."""
import re
from typing import List, Tuple, Any

import ahocorasick

from cnt.rulebase import const, utils, segmenter_common

SENTSEG_RANGES = utils.sorted_chain(
        const.CHINESE_CHARS,
        const.ENGLISH_CHARS,
        const.DIGITS,
        const.DELIMITERS,
)

_WHITESPACE_PATTERN = re.compile(r'\s+')


def _mark_whitespaces(text: str) -> List[bool]:
    '''
    return a list of marks for identifying whitespaces.
    '''
    marks = [False] * len(text)
    for match in _WHITESPACE_PATTERN.finditer(text):
        start, end = match.span()
        marks[start:end] = (True,) * (end - start)
    return marks


def _build_ac_automation(keys: List[str]) -> Any:
    atm = ahocorasick.Automaton()  # pylint: disable=c-extension-no-member
    for idx, key in enumerate(keys):
        atm.add_word(key, (idx, key))
    atm.make_automaton()
    return atm


def _meta_mark_sentence_endings(
        text: str,
        ac_automation: Any,
) -> List[bool]:

    marks = [False] * len(text)
    for end, (_, key) in ac_automation.iter(text):
        end += 1
        start = end - len(key)
        marks[start:end] = (True,) * (end - start)
    return marks


AC_AUTOMATION = _build_ac_automation(const.SENTENCE_ENDS)


def _mark_sentence_endings(text: str) -> List[bool]:
    return _meta_mark_sentence_endings(text, AC_AUTOMATION)


AC_AUTOMATION_WITH_COMMA = _build_ac_automation(const.SENTENCE_ENDS +
                                                [chr(0xFF0C), chr(0x201A), ','])


def _mark_sentence_endings_with_comma(text: str) -> List[bool]:
    return _meta_mark_sentence_endings(text, AC_AUTOMATION_WITH_COMMA)


def _sentseg_start_cond_fn(start: int, marks_group: segmenter_common.MarksGroupType) -> bool:
    extended_chinese_chars: List[bool] = marks_group[1]
    return extended_chinese_chars[start]


def _sentseg_end_cond_fn(end: int,
                         marks_group: segmenter_common.MarksGroupType) -> Tuple[bool, int]:
    whitespaces, extended_chinese_chars, sentence_endings = marks_group
    if not (extended_chinese_chars[end] or whitespaces[end]):
        return True, end
    if sentence_endings[end]:
        while end < len(sentence_endings) and sentence_endings[end]:
            end += 1
        return True, end
    return False, end + 1


# pylint: disable=invalid-name
_mark_extended_chinese_chars = segmenter_common.generate_ranges_marker(SENTSEG_RANGES)

_sentseg = segmenter_common.generate_segmenter(
        [
                _mark_whitespaces,
                _mark_extended_chinese_chars,
                _mark_sentence_endings,
        ],
        _sentseg_start_cond_fn,
        _sentseg_end_cond_fn,
)
_sentseg_with_comma = segmenter_common.generate_segmenter(
        [
                _mark_whitespaces,
                _mark_extended_chinese_chars,
                _mark_sentence_endings_with_comma,
        ],
        _sentseg_start_cond_fn,
        _sentseg_end_cond_fn,
)


def sentseg(text: str, enable_comma: bool = False) -> segmenter_common.SegmenterRetType:
    """2 modes."""
    if enable_comma:
        return _sentseg_with_comma(text)
    return _sentseg(text)
