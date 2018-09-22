import cnt.rulebase.utils as utils


def test_fullwidth_to_halfwidth():
    assert '123' == utils.fullwidth_to_halfwidth('１２３')
    assert '123' == utils.fullwidth_to_halfwidth('123')

    assert '()' == utils.fullwidth_to_halfwidth('（）')
