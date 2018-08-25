import re
from typing import List, Tuple, Any

from .const import (
    SENTENCE_ENDS,
    CHINESE_CHARS,
    ENGLISH_CHARS,
    DIGITS,
    DELIMITERS,
    sorted_chain,
)
from .common import (
    generate_ranges_marker,
    generate_segmenter,
    MARKS_GROUP_TYPE,
    SEGMENTER_RET_TYPE,
)

import ahocorasick


SENTSEG_RANGES = sorted_chain(
    CHINESE_CHARS,
    ENGLISH_CHARS,
    DIGITS,
    DELIMITERS,
)


_WHITESPACE_PATTERN = re.compile(r'\s+')


def mark_whitespaces(text: str) -> List[bool]:
    '''
    return a list of marks for identifying whitespaces.
    '''
    marks = [False] * len(text)
    for match in _WHITESPACE_PATTERN.finditer(text):
        start, end = match.span()
        marks[start:end] = (True,) * (end - start)
    return marks


def _build_ac_automation(keys: List[str]) -> Any:
    ac = ahocorasick.Automaton()
    for idx, key in enumerate(keys):
        ac.add_word(key, (idx, key))
    ac.make_automaton()
    return ac


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


AC_AUTOMATION = _build_ac_automation(SENTENCE_ENDS)


def mark_sentence_endings(text: str) -> List[bool]:
    return _meta_mark_sentence_endings(text, AC_AUTOMATION)


AC_AUTOMATION_WITH_COMMA = _build_ac_automation(
    SENTENCE_ENDS + [chr(0xFF0C), chr(0x201A), ','],
)


def mark_sentence_endings_with_comma(text: str) -> List[bool]:
    return _meta_mark_sentence_endings(text, AC_AUTOMATION_WITH_COMMA)


def sentseg_start_cond_fn(
    start: int,
    marks_group: MARKS_GROUP_TYPE,
) -> bool:

    whitespaces, extended_chinese_chars, sentence_endings = marks_group
    return extended_chinese_chars[start]


def sentseg_end_cond_fn(
    end: int,
    marks_group: MARKS_GROUP_TYPE,
) -> Tuple[bool, int]:

    whitespaces, extended_chinese_chars, sentence_endings = marks_group
    if not (extended_chinese_chars[end] or whitespaces[end]):
        return True, end
    elif sentence_endings[end]:
        while end < len(sentence_endings) and sentence_endings[end]:
            end += 1
        return True, end
    else:
        return False, end + 1


mark_extended_chinese_chars = generate_ranges_marker(SENTSEG_RANGES)


_sentseg = generate_segmenter(
    [
        mark_whitespaces,
        mark_extended_chinese_chars,
        mark_sentence_endings,
    ],
    sentseg_start_cond_fn,
    sentseg_end_cond_fn,
)
_sentseg_with_comma = generate_segmenter(
    [
        mark_whitespaces,
        mark_extended_chinese_chars,
        mark_sentence_endings_with_comma,
    ],
    sentseg_start_cond_fn,
    sentseg_end_cond_fn,
)


def sentseg(text: str, enable_comma: bool = False) -> SEGMENTER_RET_TYPE:
    if enable_comma:
        return _sentseg_with_comma(text)
    else:
        return _sentseg(text)
