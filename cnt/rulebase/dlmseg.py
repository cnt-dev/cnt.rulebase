"""Delimiter segmenter."""
from typing import Tuple

from cnt.rulebase import const, common, utils

SEGMENT_RANGES = utils.sorted_chain(
    const.CHINESE_CHARS,
    const.ENGLISH_CHARS,
    const.DIGITS,
)


def _dlmseg_start_cond_fn(start: int,
                          marks_group: common.MarkGroupType) -> bool:
    segments, = marks_group
    return segments[start]


def _dlmseg_end_cond_fn(end: int,
                        marks_group: common.MarkGroupType) -> Tuple[bool, int]:
    segments, = marks_group
    if segments[end]:
        return False, end + 1
    return True, end


dlmseg = common.generate_segmenter(  # pylint: disable=invalid-name
    [
        common.generate_ranges_marker(SEGMENT_RANGES),
    ],
    _dlmseg_start_cond_fn,
    _dlmseg_end_cond_fn,
)
