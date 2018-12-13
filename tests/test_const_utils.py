from cnt.rulebase.const import utils


def test_normalize_cjk_fullwidth_ascii():
    assert '123' == utils.normalize_cjk_fullwidth_ascii('１２３')
    assert '123' == utils.normalize_cjk_fullwidth_ascii('123')

    assert '()' == utils.normalize_cjk_fullwidth_ascii('（）')


def test_normalize_cjk_compatibility_ideographs():
    from_char = '北'
    to_char = '北'
    assert from_char != to_char

    assert to_char == utils.normalize_cjk_compatibility_ideographs(from_char)
    assert '测试' == utils.normalize_cjk_compatibility_ideographs('测试')
