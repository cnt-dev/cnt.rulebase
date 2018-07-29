import re
import bisect

from .const import SENTENCE_ENDS, CHINESE_ALL, CHINESE_ALL_START


def _char_in_zh_range(char):
    code_point = ord(char)
    # 1. find a range such that (start, end), start <= code_point.
    idx = bisect.bisect_left(CHINESE_ALL_START, code_point)
    if idx == len(CHINESE_ALL_START) or code_point != CHINESE_ALL_START[idx]:
        idx -= 1
    # 2. check if code_point <= end.
    return code_point <= CHINESE_ALL[idx][1]


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

    def _char_is_valid(c, allow_non_newline=True):
        if c.isspace():
            if not allow_non_newline:
                return False
            else:
                return bool(re.match(r'[^\S\n]', c))
        else:
            # check if it's chinese char.
            return _char_in_zh_range(c)

    while end < len(text):
        # skip if text[start] is invalid.
        if end == start and not _char_is_valid(text[start], allow_non_newline=False):
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
