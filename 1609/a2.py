import sys
import re
from util import findints


# def my_regex():
#     '''
#     >>> pattern = 
#     >>> bool(re.search(pattern, 'ADVENT'))
#     False
#     >>> bool(re.search(pattern, 'A(1x5)BC'))
#     True
#     >>> bool(re.search(pattern, 'A(13x52)BC'))
#     True
#     '''


def main():
    f = open(sys.argv[1] if len(sys.argv) > 1 else 'in')

    text = f.read().strip()
    text = 'ADVENT'

    answer = pipe(text, [
        strip_whitespace,
        decompress,
        # decompressed_length,
    ])

    print(answer)


def pipe(x, fns):
    for fn in fns:
        x = fn(x)
    return x


def strip_whitespace(text):
    return ''.join(ch for ch in text if not ch.isspace())


def decompress(text):
    '''
    >>> decompress('ADVENT')
    'ADVENT'
    >>> decompress('A(1x5)BC')
    'ABBBBBC'
    >>> decompress('(3x3)XYZ')
    'XYZXYZXYZ'
    >>> decompress('A(2x2)BCD(2x2)EFG')
    'ABCBCDEFEFG'
    >>> decompress('(6x1)(1x3)A')
    '(1x3)A'
    >>> decompress('X(8x2)(3x3)ABCY')
    'X(3x3)ABC(3x3)ABCY'

    # >>> decompressed_length('ADVENT')
    # 6
    # >>> decompressed_length('A(1x5)BC')
    # 7
    # >>> decompressed_length('(3x3)XYZ')
    # 9
    # >>> decompressed_length('A(2x2)BCD(2x2)EFG')
    # 11
    # >>> decompressed_length('(6x1)(1x3)A')
    # 6
    # >>> decompressed_length('X(8x2)(3x3)ABCY')
    # 18
    '''

    # State machine:
    #
    #       /[0-9]/  /[0-9]/
    #         ___      ___
    #        /   \    /   \
    #        \   /    \   /
    #         \ v      \ v
    # 0 -----> 1 -----> 2 -----> (back to 0)
    #    '('      'x'      ')'

    state_name = 0
    data_length_string = ''
    multiplier_string = ''
    output = ''

    pattern = r'\(\d+x\d\)'

    while re.search(pattern, text):
        match = re.search(pattern, text)

        prefix = text[:match.start()]
        output += prefix

        text = text[match.end():]  # Remove the marker

        data_length, multiplier = findints(match.group())
        output += text[:data_length] * multiplier

        text = text[data_length:]  # Remove the data section

    output += text

    return output
    # return len(output)


if __name__ == '__main__':
    main()
