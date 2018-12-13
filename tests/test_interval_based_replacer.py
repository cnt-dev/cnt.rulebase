from cnt.rulebase import const
from cnt.rulebase.rules.interval_based_operations.interval_based_replacer import (
        IntervalsCollectionBasedReplacerToString,
        IntervalsCollectionBasedReplacer,
)
from cnt.rulebase.rules.interval_based_operations.builtin_application import BuiltInReplacer


def test_replacer():
    replacer = IntervalsCollectionBasedReplacerToString({lambda x: '': const.ITV_CHINESE_CHARS})
    assert '12' == replacer.result('1测试2')

    replacer = IntervalsCollectionBasedReplacerToString({lambda x: '-': const.ITV_CHINESE_CHARS})
    assert '1-2' == replacer.result('1测试2')

    replacer = IntervalsCollectionBasedReplacerToString({lambda x: '': const.ITV_ENGLISH_CHARS})
    assert '12' == replacer.result('1english2')

    replacer = IntervalsCollectionBasedReplacerToString({lambda x: '': const.ITV_DIGITS})
    assert 'abc' == replacer.result('a1b2c3')

    replacer = IntervalsCollectionBasedReplacerToString({lambda x: '': const.ITV_DELIMITERS})
    assert '12' == replacer.result('1,2,')


def test_replacer_intervals():
    replacer = IntervalsCollectionBasedReplacer({lambda x: '': const.ITV_DIGITS})
    expected = [
            ('a', ((0, 1), (0, 1), False)),
            ('', ((1, 2), (1, 1), True)),
            ('b', ((2, 3), (1, 2), False)),
            ('', ((3, 4), (2, 2), True)),
            ('c', ((4, 5), (2, 3), False)),
            ('', ((5, 6), (3, 3), True)),
    ]
    assert expected == replacer.result('a1b2c3')

    replacer = IntervalsCollectionBasedReplacer({lambda x: '-': const.ITV_DIGITS})
    expected = [
            ('a', ((0, 1), (0, 1), False)),
            ('-', ((1, 2), (1, 2), True)),
            ('b', ((2, 3), (2, 3), False)),
            ('-', ((3, 5), (3, 4), True)),
            ('c', ((5, 6), (4, 5), False)),
            ('-', ((6, 9), (5, 6), True)),
            ('d', ((9, 10), (6, 7), False)),
    ]
    assert expected == replacer.result('a1b22c333d')


#pylint: disable=E1101
def test_built_in_replacer():
    assert '12' == BuiltInReplacer.chinese_chars_to_string.result('1测试2')
