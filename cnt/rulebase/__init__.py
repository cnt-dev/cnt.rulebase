# -*- coding: utf-8 -*-
"""Top-level package for cnt.rulebase."""

__author__ = """Hunt Zhan"""
__email__ = 'huntzhan.dev@gmail.com'
__version__ = '0.10.1'

__all__ = [
        'sentseg',
        'sentseg_lazy',
        'collector',
        'replacer',
]

from cnt.rulebase.rules import (
        sentseg,
        sentseg_lazy,
        built_in_collector as collector,
        built_in_replacer as replacer,
)
