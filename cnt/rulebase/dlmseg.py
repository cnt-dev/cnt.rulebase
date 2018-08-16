from .const import (
    CHINESE_CHARS,
    ENGLISH_CHARS,
    DIGITS,
    sorted_chain,
)
from .common import (
    generate_ranges_marker,
    generate_segmenter,
)


SEGMENT_RANGES = sorted_chain(
    CHINESE_CHARS,
    ENGLISH_CHARS,
    DIGITS,
)


def dlmseg_start_cond_fn(start, segments):
    return segments[start]


def dlmseg_end_cond_fn(end, segments):
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
