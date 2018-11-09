from typing import Generator

from cnt.rulebase.rules.sentence_segmentation.sentence_segmenter import (
        SentenceEndingLabeler,
        WhitespaceLabeler,
        SentenceValidCharacterLabeler,
        sentseg,
        sentseg_lazy,
)


def test_sentence_ending_labler():
    text = "1。2。”3"
    labeler = SentenceEndingLabeler(text, None)
    result = [labeler.label(idx) for idx in range(len(text))]
    assert [
            False,
            True,
            False,
            True,
            True,
            False,
    ] == result


def test_whitespace_labeler():
    text = '1 2\t3'
    labeler = WhitespaceLabeler(text, None)
    result = [labeler.label(idx) for idx in range(len(text))]
    assert [
            False,
            True,
            False,
            True,
            False,
    ] == result


def test_sentence_valid_character_labeler():
    text = '测试 test 123 !!!'
    labeler = SentenceValidCharacterLabeler(text, None)
    result = [labeler.label(idx) for idx in range(len(text))]
    assert [
            True,
            True,
            False,
            True,
            True,
            True,
            True,
            False,
            True,
            True,
            True,
            False,
            True,
            True,
            True,
    ] == result


def test_sentseg():
    text = ('测试句子一， 测试。  测试 句子二。 测试句子三！！！')
    sents = sentseg(text)

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
    assert 4 == len(sentseg(text, enable_comma_ending=True))

    text = '史卡肯表示:「xxx。」他说:「xxx。」'
    sents = sentseg(text, extend_ending_with_delimiters=True)
    assert '史卡肯表示:「xxx。」' == sents[0][0]

    text = 'sent <end1> sent <end2>'
    sents = sentseg(text, dynamic_endings=['<end1>', '<end2>'])
    assert 2 == len(sents)
    assert 'sent <end1>' == sents[0][0]

    text = '富兰克林·德拉诺·罗斯福'
    assert 1 == len(sentseg(text))
    assert 3 == len(sentseg(text, enable_strict_sentence_charset=True))


def test_sentseg_lazy():
    text = ''
    assert isinstance(sentseg_lazy(text), Generator)
