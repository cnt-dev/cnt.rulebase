import re

from .const import (
    SENTENCE_ENDS,
    SENTSEG_RANGES,
    generate_range_checker,
)


_sentseg_ranges_checker = generate_range_checker(SENTSEG_RANGES)


def _char_is_valid(
    c, allow_non_newline=True,
    _whitespace_pattern=re.compile(r'[^\S\n]'),
):
    if c.isspace():
        return allow_non_newline and bool(_whitespace_pattern.match(c))
    else:
        return _sentseg_ranges_checker(c)


def sentseg(text):
    '''
    text -> List( (text, [start, end)) )
    text should have been decoded.
    '''
    assert isinstance(text, str)

    sentences = []
    start, end = 0, 0

    def _push_to_sentence(start, end):
        sentences.append((
            text[start:end],
            (start, end),
        ))

    while end < len(text):
        # skip if text[start] is invalid.
        if end == start and \
                not _char_is_valid(text[start], allow_non_newline=False):
            start += 1
            end = start
            continue

        # 1. end != start and end might be invalid.
        # 2. end == start and end must not be invalid.
        if end != start and not _char_is_valid(text[end]):
            _push_to_sentence(start, end)
            start = end
            continue

        # match sentence endings.
        found_ending = False
        for sent_end in SENTENCE_ENDS:
            if end + len(sent_end) > len(text):
                continue
            if text[end:end + len(sent_end)] == sent_end:
                end += len(sent_end)
                if len(sent_end) == 1:
                    # in case of size 1 ending,
                    # duplication of sent_end should also be considered.
                    while end < len(text) and text[end] == text[end - 1]:
                        end += 1

                # stop processing.
                found_ending = True
                break

        if found_ending:
            _push_to_sentence(start, end)
            start = end
            continue
        else:
            end += 1

    # last sentence.
    if start < len(text):
        _push_to_sentence(start, len(text))

    return sentences
