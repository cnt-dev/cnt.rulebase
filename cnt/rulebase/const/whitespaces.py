"""
Consts for detecting whitespace chars.
"""
from cnt.rulebase.const import utils

#: Whitespace Chars.
#: Pulled from https://en.wikipedia.org/wiki/Whitespace_character
#:
#: Table 1.
#:
#: 0X9
#: 0XA
#: 0XB
#: 0XC
#: 0XD
#: 0X20
#: 0X85
#: 0XA0
#: 0X1680
#: 0X2000
#: 0X2001
#: 0X2002
#: 0X2003
#: 0X2004
#: 0X2005
#: 0X2006
#: 0X2007
#: 0X2008
#: 0X2009
#: 0X200A
#: 0X2028
#: 0X2029
#: 0X202F
#: 0X205F
#: 0X3000
#:
#: Table 2.
#:
#: 0X180E
#: 0X200B
#: 0X200C
#: 0X200D
#: 0X2060
#: 0XFEFF
#:
#: Table 3.
#:
#: 0XB7
#: 0X237D
#: 0X2420
#: 0X2422
#: 0X2423
#:
ITV_WHITESPACE_CHARS = utils.sorted_chain([
        (0X9, 0XD),
        (0X20, 0X20),
        (0X85, 0X85),
        (0XA0, 0XA0),
        (0XB7, 0XB7),
        (0X1680, 0X1680),
        (0X180E, 0X180E),
        (0X2000, 0X200D),
        (0X2028, 0X2029),
        (0X202F, 0X202F),
        (0X205F, 0X2060),
        (0X237D, 0X237D),
        (0X2420, 0X2420),
        (0X2422, 0X2423),
        (0X3000, 0X3000),
        (0XFEFF, 0XFEFF),
])
