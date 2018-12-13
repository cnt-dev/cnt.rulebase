"""
TODO
"""
from typing import Union, List, Dict, Callable
from cnt.rulebase import const, workflow
from cnt.rulebase.rules.interval_based_operations import (
        interval_based_collector as itb_coll,
        interval_based_replacer as itb_repl,
)


# Built-in collectors.
class BuiltInCollector:

    @classmethod
    def generate_collector_lazy(
            cls,
            intervals_collection: List[workflow.IntervalListType],
    ) -> itb_coll.IntervalBasedCollectorLazy:
        intervals = const.sorted_chain(*intervals_collection)
        collector_lazy = itb_coll.IntervalBasedCollectorLazy(intervals)
        return collector_lazy

    @classmethod
    def generate_collector(
            cls,
            intervals_collection: List[workflow.IntervalListType],
    ) -> itb_coll.IntervalBasedCollector:
        intervals = const.sorted_chain(*intervals_collection)
        collector = itb_coll.IntervalBasedCollector(intervals)
        return collector

    @classmethod
    def setup_collector(cls, name: str,
                        intervals_collection: List[workflow.IntervalListType]) -> None:
        if hasattr(cls, name):
            raise RuntimeError(f'Duplicated name: {name}')

        collector_lazy = cls.generate_collector_lazy(intervals_collection)
        collector = cls.generate_collector(intervals_collection)

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

    REGISTERED_REPL_KEY: Dict[str, Callable[[], itb_repl.ReplacerFunctionType]] = {
            'empty': lambda: lambda x: '',
            'space': lambda: lambda x: ' ',
            'tab': lambda: lambda x: '/t',
    }

    @classmethod
    def generate_param(
            cls,
            repl_with_intervals_collection: Dict[Union[str, itb_repl.ReplacerFunctionType], List[
                    workflow.IntervalListType]],
    ) -> Dict[itb_repl.ReplacerFunctionType, workflow.IntervalListType]:

        param: Dict[itb_repl.ReplacerFunctionType, workflow.IntervalListType] = {}
        for repl, intervals_collection in repl_with_intervals_collection.items():
            # Get replacer_function.
            if isinstance(repl, str):
                if repl not in cls.REGISTERED_REPL_KEY:
                    raise RuntimeError(f'Cannot find {repl}')
                replacer_function = cls.REGISTERED_REPL_KEY[repl]()
            else:
                replacer_function = repl
                # check if user provied functions are duplicated.
                if replacer_function in param:
                    raise RuntimeError(f'Duplicated function detected.')

            # Get in intervals.
            intervals = const.sorted_chain(*intervals_collection)

            param[replacer_function] = intervals

        return param

    @classmethod
    def generate_replacer_lazy(
            cls,
            repl_with_intervals_collection: Dict[Union[str, itb_repl.ReplacerFunctionType], List[
                    workflow.IntervalListType]],
    ) -> itb_repl.IntervalsCollectionBasedReplacerLazy:

        param = cls.generate_param(repl_with_intervals_collection)
        return itb_repl.IntervalsCollectionBasedReplacerLazy(param)

    @classmethod
    def generate_replacer(
            cls,
            repl_with_intervals_collection: Dict[Union[str, itb_repl.ReplacerFunctionType], List[
                    workflow.IntervalListType]],
    ) -> itb_repl.IntervalsCollectionBasedReplacer:

        param = cls.generate_param(repl_with_intervals_collection)
        return itb_repl.IntervalsCollectionBasedReplacer(param)

    @classmethod
    def generate_replacer_to_string(
            cls,
            repl_with_intervals_collection: Dict[Union[str, itb_repl.ReplacerFunctionType], List[
                    workflow.IntervalListType]],
    ) -> itb_repl.IntervalsCollectionBasedReplacerToString:

        param = cls.generate_param(repl_with_intervals_collection)
        return itb_repl.IntervalsCollectionBasedReplacerToString(param)

    @classmethod
    def setup_replacer(
            cls,
            name: str,
            repl: Union[str, itb_repl.ReplacerFunctionType],
            intervals_collection: List[workflow.IntervalListType],
    ) -> None:
        replacer_lazy = cls.generate_replacer_lazy({repl: intervals_collection})
        replacer = cls.generate_replacer({repl: intervals_collection})
        replacer_to_string = cls.generate_replacer_to_string({repl: intervals_collection})

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
