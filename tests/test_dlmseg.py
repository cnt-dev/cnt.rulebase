from cnt_ruleseg.dlmseg import dlmseg


def test_dlmseg():
    text = 'a(b)c'
    assert 3 == len(dlmseg(text))

    text = '测试1，测试2“(测试3)”。'
    assert 3 == len(dlmseg(text))
