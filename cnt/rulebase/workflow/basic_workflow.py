"""
Basic Workflow.
"""
from typing import Type, Generator, Any, Optional, Dict, Tuple, Iterable


class BasicConfig:
    """
    Configuration could be accessed by LabelProcessor and OutputGenerator.
    """


class BasicSequentialLabeler:
    """
    Define the interface of SequentialLabeler.

    :param input_sequence: The input sequence.
    """

    def __init__(self, input_sequence: str, config: Optional[BasicConfig]):
        self.input_sequence = input_sequence
        self.config = config

    def label(self, index: int) -> bool:
        """
        Return boolean label for ``self.input_sequence[index]``.
        Derived class must override this method.

        :param index: The index of ``self.input_sequence``.
        """
        raise NotImplementedError()


LabelsType = Dict[Type[BasicSequentialLabeler], bool]
IndexLabelsType = Tuple[int, LabelsType]
IndexLabelsGeneratorType = Generator[IndexLabelsType, None, None]


class BasicLabelProcessor:
    """
    Define the interface of LabelProcessor.

    :param input_sequence: The input sequence.
    :param index_labels_generator: ``(index, labels)`` generated from
        one or more :class:`BasicSequentialLabeler`.
    """

    def __init__(self, input_sequence: str, index_labels_generator: IndexLabelsGeneratorType,
                 config: Optional[BasicConfig]):
        self.input_sequence = input_sequence
        self.index_labels_generator = index_labels_generator
        self.config = config

    def result(self) -> Any:
        """
        Label processor could generate any return type.
        Derived class must override this method.
        """
        raise NotImplementedError()


class BasicOutputGenerator:
    """
    Define the interface of OutputGenerator.

    :param input_sequence: The input sequence.
    :param label_processor_result: The result of :class:`BasicLabelProcessor`.
    """

    def __init__(self, input_sequence: str, label_processor_result: Any,
                 config: Optional[BasicConfig]):
        self.input_sequence = input_sequence
        self.label_processor_result = label_processor_result
        self.config = config

    def result(self) -> Any:
        """
        Output generator could generate any return type.
        Derived class must override this method.
        """
        raise NotImplementedError()


class BasicWorkflow:
    """
    Define the basic workflow.
    Use composite pattern to organize the steps of rule-based processing.

    :param sequential_labeler_classes: For char-level sequential labeling.
    :param label_processor_class: Label post-processing.
        Commonly this step will generate new labels based on
        the result of ``sequential_labeler_classes``.
    :param output_generator_class: Generate output based on input sequence & labels.
    """

    def __init__(self, sequential_labeler_classes: Iterable[Type[BasicSequentialLabeler]],
                 label_processor_class: Type[BasicLabelProcessor],
                 output_generator_class: Type[BasicOutputGenerator]):
        self.sequential_labeler_classes = tuple(sequential_labeler_classes)
        self.label_processor_class = label_processor_class
        self.output_generator_class = output_generator_class

    def result(self, input_sequence: str, config: Optional[BasicConfig] = None) -> Any:
        """
        Execute the workflow.

        :param input_sequence: The input sequence.
        """
        # Step 1.
        sequential_labelers = [
                sl_cls(input_sequence, config) for sl_cls in self.sequential_labeler_classes
        ]
        index_labels_generator = ((index, {
                type(labeler): labeler.label(index) for labeler in sequential_labelers
        }) for index in range(len(input_sequence)))

        # Step 2.
        label_processor = self.label_processor_class(input_sequence, index_labels_generator, config)
        label_processor_result = label_processor.result()

        # Step 3.
        output_generator = self.output_generator_class(input_sequence, label_processor_result,
                                                       config)
        return output_generator.result()
