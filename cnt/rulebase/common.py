"""Common operations"""
from typing import Callable, List, Tuple
from .utils import generate_range_checker

MarkerType = Callable[[str], List[bool]]

MarksGroupType = List[List[bool]]
StartCondFnType = Callable[[int, MarksGroupType], bool]
EndCondFnType = Callable[[int, MarksGroupType], Tuple[bool, int]]

SegmenterRetType = List[Tuple[str, Tuple[int, int]]]
SegmenterType = Callable[[str], SegmenterRetType]


def generate_ranges_marker(ranges: List[Tuple[int, int]]) -> MarkerType:
    """Create range marker."""
    _ranges_checker = generate_range_checker(ranges)

    def ranges_marker(text: str) -> List[bool]:

        marks = [False] * len(text)
        for idx, char in enumerate(text):
            if _ranges_checker(char):
                marks[idx] = True
        return marks

    return ranges_marker


def generate_segmenter(markers: List[MarkerType], start_cond_fn: StartCondFnType,
                       end_cond_fn: EndCondFnType) -> SegmenterType:
    """Create segmenter."""

    def segmenter(text: str) -> List[Tuple[str, Tuple[int, int]]]:
        marks_group = [m(text) for m in markers]

        # two pointers move.
        sentences = []

        def _push_to_sentence(start: int, end: int) -> int:
            sentences.append((
                    text[start:end],
                    (start, end),
            ))
            return end

        len_text = len(text)
        start, end = 0, 0
        while start < len_text:
            if not start_cond_fn(start, marks_group):
                start += 1
                continue

            end = start + 1
            while end < len_text:
                should_break, end = end_cond_fn(end, marks_group)
                if should_break:
                    break

            start = _push_to_sentence(start, end)

        if start < len_text:
            _push_to_sentence(start, len_text)

        return sentences

    return segmenter
