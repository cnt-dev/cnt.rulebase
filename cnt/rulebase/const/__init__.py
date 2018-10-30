"""
All consts for rule-based tasks.

Naming patterns:

* `EM_*`: List of exact match strings.
* `ITV_*`: List of closed intervals.
* `RE_*`: List of regular expressions.
"""

from cnt.rulebase.const.chinese_chars import ITV_CHINESE_CHARS
from cnt.rulebase.const.english_chars import ITV_ENGLISH_CHARS
from cnt.rulebase.const.digits import ITV_DIGITS
from cnt.rulebase.const.delimiters import ITV_DELIMITERS

from cnt.rulebase.const.utils import sorted_chain, fullwidth_to_halfwidth
