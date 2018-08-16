from cnt.rulebase.replace import (
    replace_chinese_chars,
    replace_english_chars,
    replace_digits,
    replace_delimiters,
)


def test_replacers():
    assert '12' == replace_chinese_chars('1测试2')
    assert '1 2' == replace_chinese_chars('1测试2', ' ')

    assert '12' == replace_english_chars('1english2')
    assert 'abc' == replace_digits('a1b2c3')
    assert '12' == replace_delimiters('1,2,')
