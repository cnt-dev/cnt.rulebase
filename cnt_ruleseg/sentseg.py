import re

from .const import (
    SENTENCE_ENDS,
    CHINESE_CHARS,
    ENGLISH_CHARS,
    DIGITS,
    DELIMITER,
    sorted_chain,
    generate_range_checker,
)

import ahocorasick


SENTSEG_RANGES = sorted_chain(
    CHINESE_CHARS,
    ENGLISH_CHARS,
    DIGITS,
    DELIMITER,
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


def mark_extended_chinese_chars(
    text,
    _sentseg_ranges_checker=generate_range_checker(SENTSEG_RANGES),
):
    marks = [False] * len(text)
    for idx, c in enumerate(text):
        if _sentseg_ranges_checker(c):
            marks[idx] = True
    return marks


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


def sentseg(text):
    # features.
    whitespaces = mark_whitespaces(text)
    extended_chinese_chars = mark_extended_chinese_chars(text)
    sentence_endings = mark_sentence_endings(text)

    # two pointers move.
    sentences = []

    def _push_to_sentence(start, end):
        sentences.append((
            text[start:end],
            (start, end),
        ))
        return end

    TEXTLEN = len(text)
    start, end = 0, 0
    while start < TEXTLEN:
        # skip if it isn't chinese char.
        if not extended_chinese_chars[start]:
            start += 1
            continue

        # to capture a new sentence.
        end = start + 1
        while end < TEXTLEN:
            # keep going if zh chars or whitespace. stop otherwise.
            if not (extended_chinese_chars[end] or whitespaces[end]):
                break

            # reach the end of sentence.
            if sentence_endings[end]:
                while end < TEXTLEN and sentence_endings[end]:
                    end += 1
                break

            # everything is good.
            end += 1

        start = _push_to_sentence(start, end)

    if start < TEXTLEN:
        _push_to_sentence(start, TEXTLEN)

    return sentences
