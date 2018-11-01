"""
Shared type annotations.
"""
from typing import Generator, Tuple, List

IntervalType = Tuple[int, int]
IntervalGeneratorType = Generator[IntervalType, None, None]
IntervalListType = List[IntervalType]

SegmentType = Tuple[str, IntervalType]
SegmentGeneratorType = Generator[SegmentType, None, None]
SegmentListType = List[SegmentType]
