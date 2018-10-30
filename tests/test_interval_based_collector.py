from typing import Generator

from cnt.rulebase import const
from cnt.rulebase.rules.interval_based_operations.interval_based_collector import (
        IntervalBasedCollector,
        IntervalBasedCollectorLazy,
)
from cnt.rulebase.rules.interval_based_operations.builtin_application import BuiltInCollector


def test_interval_based_collector():
    intervals = const.sorted_chain(
            const.ITV_CHINESE_CHARS,
            const.ITV_ENGLISH_CHARS,
            const.ITV_DIGITS,
    )

    collector = IntervalBasedCollector(intervals)

    text = 'a(b)c'
    assert 3 == len(collector.result(text))

    text = '测试1，测试2“(测试3)”。'
    assert 3 == len(collector.result(text))

    collector_lazy = IntervalBasedCollectorLazy(intervals)
    assert isinstance(collector_lazy.result(text), Generator)


#pylint: disable=E1101
def test_chinese_sentence_chars_collector():
    text = 'a(b)c'
    assert 3 == len(BuiltInCollector.chinese_sentence_chars.result(text))

    text = '测试1，测试2“(测试3)”。'
    assert 3 == len(BuiltInCollector.chinese_sentence_chars.result(text))
