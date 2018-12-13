"""
Replace the unicode codepoint specified by intervals with arbitary strings.
"""
from typing import Callable, Generator, List, Tuple, Dict, Type, cast, Optional

from cnt.rulebase import workflow
from cnt.rulebase.rules.interval_based_operations.basic_operation import (
        IntervalBasedOperationOutputGenerator,
        IntervalsCollectionBasedOperation,
)

IntervalsWithLabelType = Tuple[workflow.IntervalType, workflow.IntervalType, bool]
ReplacerSegmentType = Tuple[str, IntervalsWithLabelType]

ResultLazyType = Generator[ReplacerSegmentType, None, None]
ResultType = List[ReplacerSegmentType]

ReplacerFunctionType = Callable[[str], str]


class IntervalsCollectionBasedReplacerConfig(workflow.BasicConfig):

    def __init__(self, labeler2repl: Dict[Type[workflow.IntervalLabeler], ReplacerFunctionType]):
        self.labeler2repl = labeler2repl


class IntervalsCollectionBasedReplacerLabelProcessor(workflow.BasicLabelProcessor):

    def result(self) -> Generator[Tuple[int, Optional[Type[workflow.IntervalLabeler]]], None, None]:
        while True:
            try:
                index, labels = next(self.index_labels_generator)
            except StopIteration:
                return

            labeler_cls = [lcls for lcls, marked in labels.items() if marked]
            if len(labeler_cls) > 1:
                raise RuntimeError('Labeler conflict!')

            aggregated_mark = cast(Type[workflow.IntervalLabeler],
                                   labeler_cls[0]) if labeler_cls else None
            yield index, aggregated_mark


#pylint: disable=W0223
class _IntervalsCollectionBasedReplacerOutputGenerator(IntervalBasedOperationOutputGenerator):

    def _result(self) -> ResultLazyType:
        """
        ``self.config.replacer_function``(``Callable[[str], str]``) must exists.
        """
        config = cast(IntervalsCollectionBasedReplacerConfig, self.config)

        diff_acc = 0
        for interval, aggregated_mark in self.continuous_intervals():
            start, end = interval
            processed_start = start + diff_acc
            processed_end = end + diff_acc

            segment = self.input_sequence[start:end]

            if aggregated_mark is not None:
                processed_segment = config.labeler2repl[cast(Type[workflow.IntervalLabeler],
                                                             aggregated_mark)](segment)

                if not processed_segment:
                    # segment is removed.
                    processed_end = processed_start
                else:
                    processed_end = processed_start + len(processed_segment)

                diff_acc += len(processed_segment) - len(segment)
                segment = processed_segment

            yield segment, (interval, (processed_start, processed_end), aggregated_mark is not None)


class IntervalsCollectionBasedReplacerOutputGeneratorLazy(
        _IntervalsCollectionBasedReplacerOutputGenerator):

    def result(self) -> ResultLazyType:
        return self._result()


class IntervalsCollectionBasedReplacerOutputGenerator(
        _IntervalsCollectionBasedReplacerOutputGenerator):

    def result(self) -> ResultType:
        return list(self._result())


#pylint: disable=W0223
class IntervalsCollectionBasedReplacerOperation(IntervalsCollectionBasedOperation):

    def __init__(self,
                 replacer_intervals: Dict[ReplacerFunctionType, workflow.IntervalListType]) -> None:
        replacer_functions = []
        interval_collections = []
        for func, intervals in replacer_intervals.items():
            replacer_functions.append(func)
            interval_collections.append(intervals)

        super().__init__(interval_collections)

        labeler2repl = {
                labeler_cls: replacer_function for labeler_cls, replacer_function in zip(
                        self.sequential_labeler_classes, replacer_functions)
        }
        self.config = IntervalsCollectionBasedReplacerConfig(labeler2repl=labeler2repl)

    def initialize_label_processor_class(self) -> None:
        self._label_processor_class = IntervalsCollectionBasedReplacerLabelProcessor


class IntervalsCollectionBasedReplacerLazy(IntervalsCollectionBasedReplacerOperation):

    def initialize_output_generator_class(self) -> None:
        self._output_generator_class = IntervalsCollectionBasedReplacerOutputGeneratorLazy

    def result(self, text: str) -> ResultLazyType:
        return cast(ResultLazyType, self.interval_based_workflow.result(text, self.config))


class IntervalsCollectionBasedReplacer(IntervalsCollectionBasedReplacerOperation):

    def initialize_output_generator_class(self) -> None:
        self._output_generator_class = IntervalsCollectionBasedReplacerOutputGenerator

    def result(self, text: str) -> ResultType:
        return cast(ResultType, self.interval_based_workflow.result(text, self.config))


class IntervalsCollectionBasedReplacerToString(IntervalsCollectionBasedReplacerOperation):

    def initialize_output_generator_class(self) -> None:
        self._output_generator_class = IntervalsCollectionBasedReplacerOutputGeneratorLazy

    def result(self, text: str) -> str:
        return ''.join(
                segment for segment, _ in self.interval_based_workflow.result(text, self.config))
