from cnt.rulebase import const
from cnt.rulebase.rules.interval_based_operations.interval_based_replacer import IntervalBasedReplacerToString
from cnt.rulebase.rules.interval_based_operations.builtin_application import BuiltInReplacer


def test_replacer():
    replacer = IntervalBasedReplacerToString(const.ITV_CHINESE_CHARS, lambda x: '')
    assert '12' == replacer.result('1测试2')

    replacer = IntervalBasedReplacerToString(const.ITV_CHINESE_CHARS, lambda x: '-')
    assert '1-2' == replacer.result('1测试2')

    replacer = IntervalBasedReplacerToString(const.ITV_ENGLISH_CHARS, lambda x: '')
    assert '12' == replacer.result('1english2')

    replacer = IntervalBasedReplacerToString(const.ITV_DIGITS, lambda x: '')
    assert 'abc' == replacer.result('a1b2c3')

    replacer = IntervalBasedReplacerToString(const.ITV_DELIMITERS, lambda x: '')
    assert '12' == replacer.result('1,2,')


#pylint: disable=E1101
def test_built_in_replacer():
    assert '12' == BuiltInReplacer.chinese_chars_to_string.result('1测试2')
