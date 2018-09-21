from cnt.rulebase import replace


def test_replacers():
    assert '12' == replace.replace_chinese_chars('1测试2')
    assert '1 2' == replace.replace_chinese_chars('1测试2', ' ')

    assert '12' == replace.replace_english_chars('1english2')
    assert 'abc' == replace.replace_digits('a1b2c3')
    assert '12' == replace.replace_delimiters('1,2,')
