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
    labeler = SentenceEndingLabeler(text)
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
    labeler = WhitespaceLabeler(text)
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
    labeler = SentenceValidCharacterLabeler(text)
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


def test_sentseg_lazy():
    text = ''
    assert isinstance(sentseg_lazy(text), Generator)
