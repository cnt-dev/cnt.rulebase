from typing import Callable, List, Tuple
from .utils import generate_range_checker


MARKER_TYPE = Callable[
    [str],
    List[bool],
]

MARKS_GROUP_TYPE = List[List[bool]]
START_COND_FN_TYPE = Callable[
    [int, MARKS_GROUP_TYPE],
    bool,
]
END_COND_FN_TYPE = Callable[
    [int, MARKS_GROUP_TYPE],
    Tuple[bool, int],
]

SEGMENTER_RET_TYPE = List[Tuple[str, Tuple[int, int]]]
SEGMENTER_TYPE = Callable[[str], SEGMENTER_RET_TYPE]


def generate_ranges_marker(
    ranges: List[Tuple[int, int]],
) -> MARKER_TYPE:

    _ranges_checker = generate_range_checker(ranges)

    def ranges_marker(text: str) -> List[bool]:

        marks = [False] * len(text)
        for idx, c in enumerate(text):
            if _ranges_checker(c):
                marks[idx] = True
        return marks

    return ranges_marker


def generate_segmenter(
    markers: List[MARKER_TYPE],
    start_cond_fn: START_COND_FN_TYPE,
    end_cond_fn: END_COND_FN_TYPE,
) -> SEGMENTER_TYPE:

    def segmenter(text: str) -> List[Tuple[str, Tuple[int, int]]]:
        marks_group = [
            m(text) for m in markers
        ]

        # two pointers move.
        sentences = []

        def _push_to_sentence(start: int, end: int) -> int:
            sentences.append((
                text[start:end],
                (start, end),
            ))
            return end

        TEXTLEN = len(text)
        start, end = 0, 0
        while start < TEXTLEN:
            if not start_cond_fn(start, marks_group):
                start += 1
                continue

            end = start + 1
            while end < TEXTLEN:
                should_break, end = end_cond_fn(end, marks_group)
                if should_break:
                    break

            start = _push_to_sentence(start, end)

        if start < TEXTLEN:
            _push_to_sentence(start, TEXTLEN)

        return sentences

    return segmenter
