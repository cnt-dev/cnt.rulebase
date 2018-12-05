from invoke import task

@task
def variant_mapping(c, unihan_variant_path, output):
    # unihan_variant_path: from https://www.unicode.org/Public/UCD/latest/ucd/UCD.zip
    print(f'Loading {unihan_variant_path}')

    with open(unihan_variant_path) as fin:
        # Format:
        # <from> <type> <to>
        items = [
            line.strip().split('\t')
            for line in fin
            if not line.startswith('#') and line.strip() and line.strip() != 'EOF'
        ]

    # Only consider <from> in
    # CJK Compatibility Ideographs
    # http://unicode.org/charts/PDF/UF900.pdf
    mapping = []
    for from_char, variant_type, to_chars in items:
        assert from_char.startswith('U+')
        from_char_codepoint = int(from_char[2:], 16)
        if from_char_codepoint < 0xF900 or from_char_codepoint > 0xFAD9:
            continue

        from_char = chr(from_char_codepoint)
        to_chars = [
            int(to_char.split('<')[0][2:], 16)
            for to_char in to_chars.split()
        ]
        to_char = chr(min(to_chars))
        assert from_char != to_char

        # print(from_char)
        # print(to_char)
        # print('-')

        mapping.append([from_char, to_char])

    with open(output, 'w') as fout:
        for from_char, to_char in mapping:
            fout.write(f'{hex(ord(from_char))}: {hex(ord(to_char))},\n')
