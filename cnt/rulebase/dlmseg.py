from typing import Tuple
from .const import (
    CHINESE_CHARS,
    ENGLISH_CHARS,
    DIGITS,
    sorted_chain,
)
from .common import (
    generate_ranges_marker,
    generate_segmenter,
    MARKS_GROUP_TYPE,
)


SEGMENT_RANGES = sorted_chain(
    CHINESE_CHARS,
    ENGLISH_CHARS,
    DIGITS,
)


def dlmseg_start_cond_fn(
    start: int,
    marks_group: MARKS_GROUP_TYPE,
) -> bool:

    segments, = marks_group
    return segments[start]


def dlmseg_end_cond_fn(
    end: int,
    marks_group: MARKS_GROUP_TYPE,
) -> Tuple[bool, int]:

    segments, = marks_group
    if segments[end]:
        return False, end + 1
    else:
        return True, end


dlmseg = generate_segmenter(
    [
        generate_ranges_marker(SEGMENT_RANGES),
    ],
    dlmseg_start_cond_fn,
    dlmseg_end_cond_fn,
)
