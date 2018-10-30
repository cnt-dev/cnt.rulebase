# -*- coding: utf-8 -*-
"""Top-level package for cnt.rulebase."""

__author__ = """Hunt Zhan"""
__email__ = 'huntzhan.dev@gmail.com'
__version__ = '0.6.4'

__all__ = [
        'sentseg',
        'sentseg_lazy',
        'built_in_collector',
        'built_in_replacer',
]

from cnt.rulebase.rules import (
        sentseg,
        sentseg_lazy,
        built_in_collector,
        built_in_replacer,
)
