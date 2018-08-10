import re

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
)

import ahocorasick


SENTSEG_RANGES = sorted_chain(
    CHINESE_CHARS,
    ENGLISH_CHARS,
    DIGITS,
    DELIMITERS,
)


def mark_whitespaces(
    text,
    _whitespace_pattern=re.compile(r'\s+'),
):
    '''
    return a list of marks for identifying whitespaces.
    '''
    marks = [False] * len(text)
    for match in _whitespace_pattern.finditer(text):
        start, end = match.span()
        marks[start:end] = (True,) * (end - start)
    return marks


mark_extended_chinese_chars = generate_ranges_marker(SENTSEG_RANGES)


def _build_ac_automation(keys):
    ac = ahocorasick.Automaton()
    for idx, key in enumerate(keys):
        ac.add_word(key, (idx, key))
    ac.make_automaton()
    return ac


def mark_sentence_endings(
    text,
    _ac_automation=_build_ac_automation(SENTENCE_ENDS),
):
    marks = [False] * len(text)
    for end, (_, key) in _ac_automation.iter(text):
        end += 1
        start = end - len(key)
        marks[start:end] = (True,) * (end - start)
    return marks


def mark_sentence_endings_with_comma(
    text,
    _ac_automation=_build_ac_automation(
        SENTENCE_ENDS + [chr(0xFF0C), chr(0x201A), ','],
    ),
):
    return mark_sentence_endings(text, _ac_automation=_ac_automation)


def sentseg_start_cond_fn(
    start,
    whitespaces, extended_chinese_chars, sentence_endings,
):
    return extended_chinese_chars[start]


def sentseg_end_cond_fn(
    end,
    whitespaces, extended_chinese_chars, sentence_endings,
):
    if not (extended_chinese_chars[end] or whitespaces[end]):
        return True, end
    elif sentence_endings[end]:
        while end < len(sentence_endings) and sentence_endings[end]:
            end += 1
        return True, end
    else:
        return False, end + 1


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


def sentseg(text, enable_comma=False):
    if enable_comma:
        return _sentseg_with_comma(text)
    else:
        return _sentseg(text)
