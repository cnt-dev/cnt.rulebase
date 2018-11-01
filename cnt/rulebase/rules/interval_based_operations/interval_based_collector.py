"""
Collect the unicode codepoint specified by intervals.
"""
from typing import cast

from cnt.rulebase import workflow
from cnt.rulebase.rules.interval_based_operations.basic_operation import (
        IntervalBasedOperationOutputGenerator,
        BasicIntervalBasedOperation,
)


#pylint: disable=W0223
class _IntervalBasedCollectorOutputGenerator(IntervalBasedOperationOutputGenerator):

    def _result(self) -> workflow.SegmentGeneratorType:
        for interval, label in self.continuous_intervals():
            if label:
                start, end = interval
                yield self.input_sequence[start:end], interval


class IntervalBasedCollectorOutputGeneratorLazy(_IntervalBasedCollectorOutputGenerator):

    def result(self) -> workflow.SegmentGeneratorType:
        return self._result()


class IntervalBasedCollectorOutputGenerator(_IntervalBasedCollectorOutputGenerator):

    def result(self) -> workflow.SegmentListType:
        return list(self._result())


class IntervalBasedCollectorLazy(BasicIntervalBasedOperation):

    def initialize_output_generator_class(self) -> None:
        self._output_generator_class = IntervalBasedCollectorOutputGeneratorLazy

    def result(self, text: str) -> workflow.SegmentGeneratorType:
        return cast(workflow.SegmentGeneratorType, self.interval_based_workflow.result(text))


class IntervalBasedCollector(BasicIntervalBasedOperation):

    def initialize_output_generator_class(self) -> None:
        self._output_generator_class = IntervalBasedCollectorOutputGenerator

    def result(self, text: str) -> workflow.SegmentListType:
        return cast(workflow.SegmentListType, self.interval_based_workflow.result(text))
