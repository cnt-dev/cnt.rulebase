from cnt.rulebase import const
from cnt.rulebase.rules.interval_based_operations.interval_based_replacer import IntervalsCollectionBasedReplacerToString
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


#pylint: disable=E1101
def test_built_in_replacer():
    assert '12' == BuiltInReplacer.chinese_chars_to_string.result('1测试2')
