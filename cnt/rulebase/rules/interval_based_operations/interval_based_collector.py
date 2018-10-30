"""
Collect the unicode codepoint specified by intervals.
"""
from cnt.rulebase import workflow
from cnt.rulebase.rules.interval_based_operations.basic_operation import (
        IntervalBasedOperationOutputGenerator,
        BasicIntervalBasedOperation,
)


#pylint: disable=W0223
class _IntervalBasedCollectorOutputGenerator(IntervalBasedOperationOutputGenerator):

    def _result(self) -> workflow.CommonOutputLazyType:
        for interval, label in self.continuous_intervals():
            if label:
                start, end = interval
                yield self.input_sequence[start:end], interval


class IntervalBasedCollectorOutputGeneratorLazy(_IntervalBasedCollectorOutputGenerator):

    def result(self) -> workflow.CommonOutputLazyType:
        return self._result()


class IntervalBasedCollectorOutputGenerator(_IntervalBasedCollectorOutputGenerator):

    def result(self) -> workflow.CommonOutputType:
        return list(self._result())


class IntervalBasedCollectorLazy(BasicIntervalBasedOperation):

    def initialize_output_generator_class(self) -> None:
        self._output_generator_class = IntervalBasedCollectorOutputGeneratorLazy

    def result(self, text: str) -> workflow.CommonOutputLazyType:
        return self.interval_based_workflow.result(text)


class IntervalBasedCollector(BasicIntervalBasedOperation):

    def initialize_output_generator_class(self) -> None:
        self._output_generator_class = IntervalBasedCollectorOutputGenerator

    def result(self, text: str) -> workflow.CommonOutputType:
        return self.interval_based_workflow.result(text)
