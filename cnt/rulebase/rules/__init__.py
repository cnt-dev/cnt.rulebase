"""
Define all rule-based actions.
"""

from cnt.rulebase.rules.sentence_segmentation.sentence_segmenter import sentseg, sentseg_lazy

from cnt.rulebase.rules.interval_based_operations.builtin_application import (
        BuiltInCollector as built_in_collector,
        BuiltInReplacer as built_in_replacer,
)
