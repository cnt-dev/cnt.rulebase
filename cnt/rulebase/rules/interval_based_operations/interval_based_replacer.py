"""
Replace the unicode codepoint specified by intervals with arbitary strings.
"""
from typing import Callable, Generator, List, Tuple, cast

from cnt.rulebase import workflow
from cnt.rulebase.rules.interval_based_operations.basic_operation import (
        IntervalBasedOperationOutputGenerator,
        BasicIntervalBasedOperation,
)

IntervalWithLabelType = Tuple[workflow.IntervalType, bool]
ReplacerSegmentType = Tuple[str, IntervalWithLabelType]

ResultLazyType = Generator[ReplacerSegmentType, None, None]
ResultType = List[ReplacerSegmentType]

ReplacerFunctionType = Callable[[str], str]


class IntervalBasedReplacerConfig(workflow.BasicConfig):

    def __init__(self, replacer_function: ReplacerFunctionType):
        self.replacer_function = replacer_function


#pylint: disable=W0223
class _IntervalBasedReplacerOutputGenerator(IntervalBasedOperationOutputGenerator):

    def _result(self) -> ResultLazyType:
        """
        ``self.config.replacer_function``(``Callable[[str], str]``) must exists.
        """
        config = cast(IntervalBasedReplacerConfig, self.config)

        for interval, label in self.continuous_intervals():
            start, end = interval
            segment = self.input_sequence[start:end]
            if label:
                segment = config.replacer_function(segment)
            yield segment, (interval, label)


class IntervalBasedReplacerOutputGeneratorLazy(_IntervalBasedReplacerOutputGenerator):

    def result(self) -> ResultLazyType:
        return self._result()


class IntervalBasedReplacerOutputGenerator(_IntervalBasedReplacerOutputGenerator):

    def result(self) -> ResultType:
        return list(self._result())


#pylint: disable=W0223
class IntervalBasedReplacerOperation(BasicIntervalBasedOperation):

    def __init__(self, intervals: workflow.IntervalListType,
                 replacer_function: ReplacerFunctionType):
        super().__init__(intervals)
        self.config = IntervalBasedReplacerConfig(replacer_function=replacer_function)


class IntervalBasedReplacerLazy(IntervalBasedReplacerOperation):

    def initialize_output_generator_class(self) -> None:
        self._output_generator_class = IntervalBasedReplacerOutputGeneratorLazy

    def result(self, text: str) -> ResultLazyType:
        return cast(ResultLazyType, self.interval_based_workflow.result(text, self.config))


class IntervalBasedReplacer(IntervalBasedReplacerOperation):

    def initialize_output_generator_class(self) -> None:
        self._output_generator_class = IntervalBasedReplacerOutputGenerator

    def result(self, text: str) -> ResultType:
        return cast(ResultType, self.interval_based_workflow.result(text, self.config))


class IntervalBasedReplacerToString(IntervalBasedReplacerOperation):

    def initialize_output_generator_class(self) -> None:
        self._output_generator_class = IntervalBasedReplacerOutputGeneratorLazy

    def result(self, text: str) -> str:
        return ''.join(
                segment for segment, _ in self.interval_based_workflow.result(text, self.config))
