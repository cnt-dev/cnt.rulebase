from cnt.rulebase import fullwidth_to_halfwidth


def test_fullwidth_to_halfwidth():
    assert '123' == fullwidth_to_halfwidth('１２３')
    assert '123' == fullwidth_to_halfwidth('123')

    assert '()' == fullwidth_to_halfwidth('（）')
