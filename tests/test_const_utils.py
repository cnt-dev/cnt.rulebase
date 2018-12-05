from cnt.rulebase.const import utils


def test_fullwidth_to_halfwidth():
    assert '123' == utils.fullwidth_to_halfwidth('１２３')
    assert '123' == utils.fullwidth_to_halfwidth('123')

    assert '()' == utils.fullwidth_to_halfwidth('（）')


def test_replace_cjk_compatibility_ideographs():
    from_char = '北'
    to_char = '北'
    assert from_char != to_char

    assert to_char == utils.replace_cjk_compatibility_ideographs(from_char)
    assert '测试' == utils.replace_cjk_compatibility_ideographs('测试')
