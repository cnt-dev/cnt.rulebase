from cnt.rulebase import const, sentseg


def test_sentseg_ends():
    assert len(const.SENTENCE_ENDS) == len(set(const.SENTENCE_ENDS))


def test_sentseg():
    text = ('测试句子一， 测试。  测试 句子二。 测试句子三！！！')
    sents = sentseg.sentseg(text)

    assert 3 == len(sents)

    sent1_text, sent1_range = sents[0]
    assert '测试句子一， 测试。' == sent1_text
    assert '测试句子一， 测试。' == text[sent1_range[0]:sent1_range[1]]

    sent2_text, sent2_range = sents[1]
    assert '测试 句子二。' == sent2_text
    assert '测试 句子二。' == text[sent2_range[0]:sent2_range[1]]

    sent3_text, sent3_range = sents[2]
    assert '测试句子三！！！' == sent3_text
    assert '测试句子三！！！' == text[sent3_range[0]:sent3_range[1]]

    text = ('a,b，c‚d')
    assert 4 == len(sentseg.sentseg(text, enable_comma=True))


def test_no_overlapping_char_ranges():
    pre_end = -1
    for start, end in sentseg.SENTSEG_RANGES:
        assert end >= start
        assert start > pre_end
        pre_end = end


def test_mark_whitespaces():
    text = 'aa  \n a\ta '
    assert [
        False,
        False,
        True,
        True,
        True,
        True,
        False,
        True,
        False,
        True,
    ] == sentseg._mark_whitespaces(text)


def test_mark_extended_chinese_chars():
    text = '  测试。 \tabc '
    assert [
        False,
        False,
        True,
        True,
        True,
        False,
        False,
        True,
        True,
        True,
        False,
    ] == sentseg._mark_extended_chinese_chars(text)


def test_mark_sentence_endings():
    text = 'a。"b，c!？！”d!！!'
    assert [
        False,
        True,
        True,
        False,
        False,
        False,
        True,
        True,
        True,
        True,
        False,
        True,
        True,
        True,
    ] == sentseg._mark_sentence_endings(text)
