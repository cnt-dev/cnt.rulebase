.. _usage_label:

=====
Usage
=====

To use :mod:`cnt.rulebase` in a project::

    from cnt import rulebase


Sentence segmentation (see :func:`cnt.rulebase.sentseg` and :func:`cnt.rulebase.sentseg_lazy`) ::

    text = '''
    史卡肯表示:「我今天打的和当初在温布登打的一样,除了这一次幸运之神落在我这边以外。」他说:「其
    实在温布登时最后的胜利也有可能属于我,因为当时打到了第五盘却仍然僵持在二十比十八的对峙。」菲
    利普西斯在当初的温布登比赛中,在面对史卡肯时曾经发出四十四个爱司球,但是为他搏得「重炮手」美誉
    的发球,并没有在今天的球赛中助他一臂之力。菲利普西斯在第一盘第七局以三十比四十落后时,竟然击出
    双发失误;另外在第九局他又再度犯下双发失误球,让史卡肯得以坐拥两次的破发点,并且顺利赢得第一盘
    。在这场历时六十六分钟的比赛里,史卡肯表示:「我大力主攻他的第二发球,同时我也对他的第一发球施
    压,使我取得更多的机会。」这也是史卡肯和菲利普西斯在六度对峙中的第二次获胜。
    '''


    # 1. Default option.
    rulebase.sentseg(text)

    # 1. Return. [ (str, (start_idx, end_idx)), ... ]
    [('史卡肯表示:「我今天打的和当初在温布登打的一样,除了这一次幸运之神落在我这边以外。', (1, 42)),
    ('」他说:「其\n实在温布登时最后的胜利也有可能属于我,因为当时打到了第五盘却仍然僵持在二十比十八的对峙。', (42, 93)),
    ('」菲\n利普西斯在当初的温布登比赛中,在面对史卡肯时曾经发出四十四个爱司球,但是为他搏得「重炮手」美誉\n的发球,并没有在今天的球赛中助他一臂之力。',
    (93, 165)),
    ('菲利普西斯在第一盘第七局以三十比四十落后时,竟然击出\n双发失误;', (165, 197)),
    ('另外在第九局他又再度犯下双发失误球,让史卡肯得以坐拥两次的破发点,并且顺利赢得第一盘\n。', (197, 241)),
    ('在这场历时六十六分钟的比赛里,史卡肯表示:「我大力主攻他的第二发球,同时我也对他的第一发球施\n压,使我取得更多的机会。', (241, 300)),
    ('」这也是史卡肯和菲利普西斯在六度对峙中的第二次获胜。', (300, 326))]


    # 2. Extend the sentence ending with delimiters.
    rulebase.sentseg(text, extend_ending_with_delimiters=True)

    # 2. Return.
    [('史卡肯表示:「我今天打的和当初在温布登打的一样,除了这一次幸运之神落在我这边以外。」', (1, 43)),
    ('他说:「其\n实在温布登时最后的胜利也有可能属于我,因为当时打到了第五盘却仍然僵持在二十比十八的对峙。」', (43, 94)),
    ('菲\n利普西斯在当初的温布登比赛中,在面对史卡肯时曾经发出四十四个爱司球,但是为他搏得「重炮手」美誉\n的发球,并没有在今天的球赛中助他一臂之力。',
    (94, 165)),
    ('菲利普西斯在第一盘第七局以三十比四十落后时,竟然击出\n双发失误;', (165, 197)),
    ('另外在第九局他又再度犯下双发失误球,让史卡肯得以坐拥两次的破发点,并且顺利赢得第一盘\n。', (197, 241)),
    ('在这场历时六十六分钟的比赛里,史卡肯表示:「我大力主攻他的第二发球,同时我也对他的第一发球施\n压,使我取得更多的机会。」', (241, 301)),
    ('这也是史卡肯和菲利普西斯在六度对峙中的第二次获胜。', (301, 326))]


    # 3. Include dynamic ending ``:``.
    rulebase.sentseg(text, extend_ending_with_delimiters=True, dynamic_endings=[':'])

    # 3. Return.
    [('史卡肯表示:「', (1, 8)),
    ('我今天打的和当初在温布登打的一样,除了这一次幸运之神落在我这边以外。」', (8, 43)),
    ('他说:「', (43, 47)),
    ('其\n实在温布登时最后的胜利也有可能属于我,因为当时打到了第五盘却仍然僵持在二十比十八的对峙。」', (47, 94)),
    ('菲\n利普西斯在当初的温布登比赛中,在面对史卡肯时曾经发出四十四个爱司球,但是为他搏得「重炮手」美誉\n的发球,并没有在今天的球赛中助他一臂之力。',
    (94, 165)),
    ('菲利普西斯在第一盘第七局以三十比四十落后时,竟然击出\n双发失误;', (165, 197)),
    ('另外在第九局他又再度犯下双发失误球,让史卡肯得以坐拥两次的破发点,并且顺利赢得第一盘\n。', (197, 241)),
    ('在这场历时六十六分钟的比赛里,史卡肯表示:「', (241, 263)),
    ('我大力主攻他的第二发球,同时我也对他的第一发球施\n压,使我取得更多的机会。」', (263, 301)),
    ('这也是史卡肯和菲利普西斯在六度对峙中的第二次获胜。', (301, 326))]


    # Return a generator for a better performance.
    rulebase.sentseg_lazy(text)

Pattern filtering (see :obj:`cnt.rulebase.collector`) ::

    text = '」他说:「其实在Wimbledon时最后的胜利也有可能属于我,因为当时打到了第5盘却仍然僵持在20比18的对峙。'

    # 1. Collect Chinese + English + Digits.
    rulebase.collector.chinese_sentence_chars.result(text)

    # 1. Return.
    [('他说', (1, 3)),
    ('其实在Wimbledon时最后的胜利也有可能属于我', (5, 30)),
    ('因为当时打到了第5盘却仍然僵持在20比18的对峙', (31, 55))]


    # 2. Collect only Chinese.
    rulebase.collector.chinese_chars.result(text)

    # 2. Return.
    [('他说', (1, 3)),
    ('其实在', (5, 8)),
    ('时最后的胜利也有可能属于我', (17, 30)),
    ('因为当时打到了第', (31, 39)),
    ('盘却仍然僵持在', (40, 47)),
    ('比', (49, 50)),
    ('的对峙', (52, 55))]


    # 3. Generate a new collector for any Unicode codepoint intervals.
    my_collector_lazy, my_collector = rulebase.collector.generate_collector([
            rulebase.const.ITV_CHINESE_CHARS,
            rulebase.const.ITV_ENGLISH_CHARS,
    ])

    # 3. Return.
    [('他说', (1, 3)),
    ('其实在Wimbledon时最后的胜利也有可能属于我', (5, 30)),
    ('因为当时打到了第', (31, 39)),
    ('盘却仍然僵持在', (40, 47)),
    ('比', (49, 50)),
    ('的对峙', (52, 55))]


Pattern replacement (see :obj:`cnt.rulebase.replacer`) ::

    text = '」他说:「其实在Wimbledon时最后的胜利也有可能属于我,因为当时打到了第5盘却仍然僵持在20比18的对峙。'

    # 1. Replace English characters by the empty string.
    rulebase.replacer.english_chars.result(text)

    # 1. Return. (segment, ((start_idx, end_idx), is_replaced))
    [('」他说:「其实在', ((0, 8), False)),
    ('', ((8, 17), True)),
    ('时最后的胜利也有可能属于我,因为当时打到了第5盘却仍然僵持在20比18的对峙。', ((17, 56), False))]


    # 2. Return merged string.
    rulebase.replacer.english_chars_to_string.result(text)

    # 2. Return. str.
    '」他说:「其实在时最后的胜利也有可能属于我,因为当时打到了第5盘却仍然僵持在20比18的对峙。'


    # 3. Generate a new replacer for any Unicode codepoint intervals & arbitrary replacement function.
    my_replacer_lazy, my_replacer, my_replacer_to_string = rulebase.replacer.generate_replacer(
            lambda x: '<{}>'.format(len(x)),
            [rulebase.const.ITV_ENGLISH_CHARS],
    )

    # 3. Return.
    [('」他说:「其实在', ((0, 8), False)),
    ('<9>', ((8, 17), True)),
    ('时最后的胜利也有可能属于我,因为当时打到了第5盘却仍然僵持在20比18的对峙。', ((17, 56), False))]
