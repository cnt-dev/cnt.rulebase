"""
TODO
"""
from typing import Union, Tuple, List
from cnt.rulebase import const, workflow
from cnt.rulebase.rules.interval_based_operations import (
        interval_based_collector as itb_coll,
        interval_based_replacer as itb_repl,
)


# Built-in collectors.
class BuiltInCollector:

    @classmethod
    def generate_collector(
            cls,
            intervals_collection: List[workflow.IntervalListType],
    ) -> Tuple[itb_coll.IntervalBasedCollectorLazy, itb_coll.IntervalBasedCollector]:
        intervals = const.sorted_chain(*intervals_collection)

        collector_lazy = itb_coll.IntervalBasedCollectorLazy(intervals)
        collector = itb_coll.IntervalBasedCollector(intervals)

        return collector_lazy, collector

    @classmethod
    def setup_collector(cls, name: str,
                        intervals_collection: List[workflow.IntervalListType]) -> None:
        if hasattr(cls, name):
            raise RuntimeError(f'Duplicated name: {name}')

        collector_lazy, collector = cls.generate_collector(intervals_collection)

        setattr(cls, f'{name}_lazy', collector_lazy)
        setattr(cls, name, collector)


BuiltInCollector.setup_collector('chinese_chars', [const.ITV_CHINESE_CHARS])
BuiltInCollector.setup_collector('english_chars', [const.ITV_ENGLISH_CHARS])
BuiltInCollector.setup_collector('digits', [const.ITV_DIGITS])
BuiltInCollector.setup_collector('delimiters', [const.ITV_DELIMITERS])

BuiltInCollector.setup_collector(
        'chinese_sentence_chars',
        [const.ITV_CHINESE_CHARS, const.ITV_ENGLISH_CHARS, const.ITV_DIGITS],
)


# Built-in replacers.
class BuiltInReplacer:

    REGISTERED_REPL = {
            'empty': lambda x: '',
            'space': lambda x: ' ',
            'tab': lambda x: '/t',
    }

    @classmethod
    def generate_replacer(
            cls,
            repl: Union[str, itb_repl.ReplacerFunctionType],
            intervals_collection: List[workflow.IntervalListType],
    ) -> Tuple[itb_repl.IntervalBasedReplacerLazy, itb_repl.IntervalBasedReplacer, itb_repl.
               IntervalBasedReplacerToString]:

        if isinstance(repl, str):
            if repl not in cls.REGISTERED_REPL:
                raise RuntimeError(f'Cannot find {repl}')
            replacer_function: itb_repl.ReplacerFunctionType = cls.REGISTERED_REPL[repl]
        else:
            replacer_function = repl

        intervals = const.sorted_chain(*intervals_collection)

        replacer_lazy = itb_repl.IntervalBasedReplacerLazy(intervals, replacer_function)
        replacer = itb_repl.IntervalBasedReplacer(intervals, replacer_function)
        replacer_to_string = itb_repl.IntervalBasedReplacerToString(intervals, replacer_function)

        return replacer_lazy, replacer, replacer_to_string

    @classmethod
    def setup_replacer(cls, name: str, repl: Union[str, itb_repl.ReplacerFunctionType],
                       intervals_collection: List[workflow.IntervalListType]) -> None:
        replacer_lazy, replacer, replacer_to_string = cls.generate_replacer(
                repl, intervals_collection)

        if hasattr(cls, name):
            raise RuntimeError(f'Duplicated name: {name}')

        setattr(cls, f'{name}_lazy', replacer_lazy)
        setattr(cls, name, replacer)
        setattr(cls, f'{name}_to_string', replacer_to_string)


BuiltInReplacer.setup_replacer('chinese_chars', 'empty', [const.ITV_CHINESE_CHARS])
BuiltInReplacer.setup_replacer('english_chars', 'empty', [const.ITV_ENGLISH_CHARS])
BuiltInReplacer.setup_replacer('digits', 'empty', [const.ITV_DIGITS])
BuiltInReplacer.setup_replacer('delimiters', 'empty', [const.ITV_DELIMITERS])

BuiltInReplacer.setup_replacer('chinese_chars_spaced', 'space', [const.ITV_CHINESE_CHARS])
BuiltInReplacer.setup_replacer('english_chars_spaced', 'space', [const.ITV_ENGLISH_CHARS])
BuiltInReplacer.setup_replacer('digits_spaced', 'space', [const.ITV_DIGITS])
BuiltInReplacer.setup_replacer('delimiters_spaced', 'space', [const.ITV_DELIMITERS])
