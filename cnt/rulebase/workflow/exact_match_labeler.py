from typing import Any, List

import ahocorasick

from cnt.rulebase.workflow.type_annotations import IntervalGeneratorType
from cnt.rulebase.workflow.interval_labeler import IntervalLabeler


def _ac_automation_match(text: str, ac_automation: Any) -> IntervalGeneratorType:
    prev_start, prev_end = -1, -1

    # ``iter``` will return ``end`` in accending order, see
    # https://github.com/WojciechMula/pyahocorasick/blob/484b1f13549fc9bdeb9868d8a1711d1861f804c3/py/pyahocorasick.py#L229-L252
    # Also note the ``[start, end]`` generated by ``iter`` are closed interval.
    for end, (_, key) in ac_automation.iter(text):
        start = end + 1 - len(key)

        if prev_start < 0:
            # init.
            prev_start, prev_end = start, end
        elif start <= prev_end + 1:
            # check the interleaved case.
            prev_end = end
        else:
            # should return the previous interval. Note we yield half-opened interval here.
            yield (prev_start, prev_end + 1)
            prev_start, prev_end = start, end

    # yield the last interval.
    if prev_start >= 0:
        yield (prev_start, prev_end + 1)


class ExactMatchLabeler(IntervalLabeler):
    """
    Helper to label exact match strings.
    """

    AC_AUTOMATION: Any = None

    @classmethod
    def build_ac_automation_from_strings(cls, keys: List[str]) -> Any:
        atm = ahocorasick.Automaton()  # pylint: disable=c-extension-no-member
        for idx, key in enumerate(keys):
            atm.add_word(key, (idx, key))
        atm.make_automaton()
        return atm

    @classmethod
    def build_and_bind_ac_automation_from_strings(cls, keys: List[str]) -> None:
        cls.AC_AUTOMATION = cls.build_ac_automation_from_strings(keys)

    def intervals_generator(self) -> IntervalGeneratorType:
        if self.AC_AUTOMATION is None:
            raise RuntimeError('AC_AUTOMATION is not initialized.')
        return _ac_automation_match(self.input_sequence, self.AC_AUTOMATION)
