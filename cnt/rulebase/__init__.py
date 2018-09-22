# -*- coding: utf-8 -*-
"""Top-level package for cnt.rulebase."""

__author__ = """Hunt Zhan"""
__email__ = 'huntzhan.dev@gmail.com'
__version__ = '0.6.3'

from cnt.rulebase.sentence_segmenter import sentseg
from cnt.rulebase.delimiter_segmenter import dlmseg
from cnt.rulebase.char_replacer import (
        replace_chinese_chars,
        replace_english_chars,
        replace_digits,
        replace_delimiters,
)
