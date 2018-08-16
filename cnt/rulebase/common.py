from .utils import generate_range_checker


def generate_ranges_marker(ranges):

    def ranges_marker(
        text,
        _ranges_checker=generate_range_checker(ranges),
    ):
        marks = [False] * len(text)
        for idx, c in enumerate(text):
            if _ranges_checker(c):
                marks[idx] = True
        return marks

    return ranges_marker


def generate_segmenter(markers, start_cond_fn, end_cond_fn):

    def segmenter(text):
        marks_group = [
            m(text) for m in markers
        ]

        # two pointers move.
        sentences = []

        def _push_to_sentence(start, end):
            sentences.append((
                text[start:end],
                (start, end),
            ))
            return end

        TEXTLEN = len(text)
        start, end = 0, 0
        while start < TEXTLEN:
            if not start_cond_fn(start, *marks_group):
                start += 1
                continue

            end = start + 1
            while end < TEXTLEN:
                should_break, end = end_cond_fn(end, *marks_group)
                if should_break:
                    break

            start = _push_to_sentence(start, end)

        if start < TEXTLEN:
            _push_to_sentence(start, TEXTLEN)

        return sentences

    return segmenter
