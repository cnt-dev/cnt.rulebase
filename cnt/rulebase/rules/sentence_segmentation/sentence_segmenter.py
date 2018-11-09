"""
Chinese sentence segmentation.
"""
from typing import Union, Optional, List, cast

from cnt.rulebase import workflow, const
from cnt.rulebase.rules.sentence_segmentation import const as sentseg_const


class SentenceSegementationConfig(workflow.BasicConfig):

    def __init__(
            self,
            enable_strict_sentence_charset: bool,
            enable_comma_ending: bool,
            extend_ending_with_delimiters: bool,
            dynamic_endings: List[str],
    ):
        self.enable_strict_sentence_charset = enable_strict_sentence_charset
        self.enable_comma_ending = enable_comma_ending
        self.extend_ending_with_delimiters = extend_ending_with_delimiters
        self.dynamic_endings = dynamic_endings


class SentenceEndingLabeler(workflow.ExactMatchLabeler):
    """
    Mark sentence endings based on
    :py:const:`cnt.rulebase.const.sentence_endings.EM_SENTENCE_ENDINGS`
    """


SentenceEndingLabeler.build_and_bind_ac_automation_from_strings(sentseg_const.EM_SENTENCE_ENDINGS)


class DynamicSentenceEndingLabeler(workflow.ExactMatchLabeler):
    """
    Support dynamic sentence endings that will be built in runtime.
    """

    def __init__(self, input_sequence: str, config: Optional[SentenceSegementationConfig]):
        # Inject ``AC_AUTOMATION`` before __init__().
        if config and config.dynamic_endings:
            # pylint: disable=C0103
            self.AC_AUTOMATION = self.build_ac_automation_from_strings(config.dynamic_endings)

        super().__init__(input_sequence, config)

    def intervals_generator(self) -> workflow.IntervalGeneratorType:

        def mocker_generator() -> workflow.IntervalGeneratorType:
            empty_tuple = cast(workflow.IntervalListType, ())
            yield from empty_tuple

        if self.config:
            config = cast(SentenceSegementationConfig, self.config)
            if not config.dynamic_endings:
                return mocker_generator()

        return super().intervals_generator()


class CommaLabeler(workflow.BasicSequentialLabeler):
    """
    Mark comma.
    """

    COMMAS = (chr(0xFF0C), chr(0x201A), ',')

    def label(self, index: int) -> bool:
        return self.input_sequence[index] in self.COMMAS


class WhitespaceLabeler(workflow.IntervalLabeler):
    """
    Mark unicode whitespace.
    """


WhitespaceLabeler.initialize_by_regular_expression(r'\s+')


class SentenceValidCharacterLabeler(workflow.IntervalLabeler):
    """
    Mark valid character of chinese sentence.
    """


SentenceValidCharacterLabeler.initialize_by_intervals(sentseg_const.ITV_SENTENCE_VALID_CHARS)


class DelimitersLabeler(workflow.IntervalLabeler):
    """
    Mark dilimiters for sentence ending extension.
    """


DelimitersLabeler.initialize_by_intervals(const.ITV_DELIMITERS)


class SentenceSegementationLabelProcessor(workflow.BasicLabelProcessor):

    def _labels_indicate_sentence_ending(self, labels: workflow.LabelsType) -> bool:
        config = cast(SentenceSegementationConfig, self.config)
        return bool(labels[SentenceEndingLabeler] or
                    (config.dynamic_endings and labels[DynamicSentenceEndingLabeler]) or
                    (config.enable_comma_ending and labels[CommaLabeler]))

    def result(self) -> workflow.IntervalGeneratorType:
        """
        Generate intervals indicating the valid sentences.
        """
        config = cast(SentenceSegementationConfig, self.config)

        index = -1
        labels = None

        while True:

            # 1. Find the start of the sentence.
            start = -1
            while True:
                # Check the ``labels`` generated from step (2).
                if labels is None:
                    # https://www.python.org/dev/peps/pep-0479/
                    try:
                        index, labels = next(self.index_labels_generator)
                    except StopIteration:
                        return
                # Check if we found a valid sentence char.
                if labels[SentenceValidCharacterLabeler]:
                    start = index
                    break
                # Trigger next(...) action.
                labels = None
                index = -1

            # 2. Find the ending.
            end = -1
            try:
                while True:
                    index, labels = next(self.index_labels_generator)

                    # Detected invalid char.
                    if config.enable_strict_sentence_charset and \
                            not labels[SentenceValidCharacterLabeler] and \
                            not labels[WhitespaceLabeler]:
                        end = index
                        break

                    # Detected sentence ending.
                    if self._labels_indicate_sentence_ending(labels):
                        # Consume the ending span.
                        while True:
                            index, labels = next(self.index_labels_generator)
                            is_ending = (self._labels_indicate_sentence_ending(labels) or
                                         (config.extend_ending_with_delimiters and
                                          labels[DelimitersLabeler]))

                            if not is_ending:
                                end = index
                                break
                        # yeah we found the ending.
                        break
            except StopIteration:
                end = len(self.input_sequence)
                # Trigger next(...) action.
                labels = None
                index = -1

            yield start, end


#pylint: disable=W0223
class _SentenceSegementationOutputGeneratorLazy(workflow.BasicOutputGenerator):

    def _result(self) -> workflow.SegmentGeneratorType:
        return ((self.input_sequence[start:end], (start, end))
                for start, end in self.label_processor_result)


class SentenceSegementationOutputGeneratorLazy(_SentenceSegementationOutputGeneratorLazy):

    def result(self) -> workflow.SegmentGeneratorType:
        return self._result()


class SentenceSegementationOutputGenerator(_SentenceSegementationOutputGeneratorLazy):

    def result(self) -> workflow.SegmentListType:
        return list(self._result())


def _generate_sentseg_workflow(lazy: bool) -> workflow.BasicWorkflow:
    return workflow.BasicWorkflow(
            sequential_labeler_classes=[
                    SentenceEndingLabeler,
                    DynamicSentenceEndingLabeler,
                    DelimitersLabeler,
                    CommaLabeler,
                    WhitespaceLabeler,
                    SentenceValidCharacterLabeler,
            ],
            label_processor_class=SentenceSegementationLabelProcessor,
            output_generator_class=(SentenceSegementationOutputGeneratorLazy
                                    if lazy else SentenceSegementationOutputGenerator),
    )


SENTSEG_WORKFLOW_LAZY = _generate_sentseg_workflow(lazy=True)
SENTSEG_WORKFLOW = _generate_sentseg_workflow(lazy=False)


def _sentseg(
        sentseg_workflow: workflow.BasicWorkflow,
        text: str,
        enable_strict_sentence_charset: bool,
        enable_comma_ending: bool,
        extend_ending_with_delimiters: bool,
        dynamic_endings: List[str],
) -> Union[workflow.SegmentGeneratorType, workflow.SegmentListType]:
    config = SentenceSegementationConfig(
            enable_strict_sentence_charset=enable_strict_sentence_charset,
            enable_comma_ending=enable_comma_ending,
            extend_ending_with_delimiters=extend_ending_with_delimiters,
            dynamic_endings=dynamic_endings,
    )
    return cast(Union[workflow.SegmentGeneratorType, workflow.SegmentListType],
                sentseg_workflow.result(text, config))


def sentseg(
        text: str,
        enable_strict_sentence_charset: bool = False,
        enable_comma_ending: bool = False,
        extend_ending_with_delimiters: bool = False,
        dynamic_endings: Optional[List[str]] = None,
) -> workflow.SegmentListType:
    return cast(
            workflow.SegmentListType,
            _sentseg(
                    SENTSEG_WORKFLOW,
                    text,
                    enable_strict_sentence_charset,
                    enable_comma_ending,
                    extend_ending_with_delimiters,
                    dynamic_endings or [],
            ))


def sentseg_lazy(
        text: str,
        enable_strict_sentence_charset: bool = False,
        enable_comma_ending: bool = False,
        extend_ending_with_delimiters: bool = False,
        dynamic_endings: Optional[List[str]] = None,
) -> workflow.SegmentGeneratorType:
    return cast(
            workflow.SegmentGeneratorType,
            _sentseg(
                    SENTSEG_WORKFLOW_LAZY,
                    text,
                    enable_strict_sentence_charset,
                    enable_comma_ending,
                    extend_ending_with_delimiters,
                    dynamic_endings or [],
            ))
