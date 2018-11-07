from typing import Optional
from typing import re as BuiltInReType  # type: ignore

import re

from cnt.rulebase.workflow.basic_workflow import BasicSequentialLabeler, BasicConfig
from cnt.rulebase.workflow.type_annotations import IntervalType, IntervalListType, IntervalGeneratorType


def _next_interval(intervals: IntervalGeneratorType) -> Optional[IntervalType]:
    try:
        return next(intervals)
    except StopIteration:
        return None


def build_re_pattern_from_intervals(intervals: IntervalListType) -> BuiltInReType:
    """
    Convert intervals to regular expression pattern.

    :param intervals: Unicode codepoint intervals.
    """

    inner = [f'{chr(lb)}-{chr(ub)}' for lb, ub in intervals]
    joined_inner = ''.join(inner)
    pattern = f'[{joined_inner}]+'

    return re.compile(pattern, re.UNICODE)


class IntervalLabeler(BasicSequentialLabeler):
    """
    Helper to label intervals.

    :param input_sequence: The input sequence.
    """

    ITV_RE_PATTERN: Optional[BuiltInReType] = None

    @classmethod
    def initialize_by_regular_expression(cls, pattern: str) -> None:
        cls.ITV_RE_PATTERN = re.compile(pattern, re.UNICODE)

    @classmethod
    def initialize_by_intervals(cls, intervals: IntervalListType) -> None:
        """
        Convert intervals to regular expression pattern.

        :param intervals: Unicode codepoint intervals.
        """
        cls.ITV_RE_PATTERN = build_re_pattern_from_intervals(intervals)

    def __init__(self, input_sequence: str, config: Optional[BasicConfig]):
        super().__init__(input_sequence, config)

        self.intervals = self.intervals_generator()
        self.cur_interval = _next_interval(self.intervals)

    def intervals_generator(self) -> IntervalGeneratorType:
        if self.ITV_RE_PATTERN is None:
            raise RuntimeError('ITV_RE_PATTERN should be initialized.')
        return (match.span() for match in self.ITV_RE_PATTERN.finditer(self.input_sequence))

    def label(self, index: int) -> bool:
        if self.cur_interval is None or index < self.cur_interval[0]:
            return False

        if index < self.cur_interval[1]:
            return True

        self.cur_interval = _next_interval(self.intervals)
        return False
