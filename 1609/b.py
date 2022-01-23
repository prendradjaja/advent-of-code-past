import sys
import re
from util import findints

pattern = r'\(\d+x\d+\)'


# def my_regex():
#     '''
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
    # text = 'ADVENT'

    print('This approach is too slow')
    answer = pipe(text, [
        strip_whitespace,
        # decompress,
        decompressed_length,
    ])

    print(answer)


def pipe(x, fns):
    for fn in fns:
        x = fn(x)
    return x


def strip_whitespace(text):
    return ''.join(ch for ch in text if not ch.isspace())


def decompressed_length(text):
    '''
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


    >>> decompressed_length('(3x3)XYZ')
    9
    >>> decompressed_length('X(8x2)(3x3)ABCY')
    20
    >>> decompressed_length('(27x12)(20x12)(13x14)(7x10)(1x12)A')
    241920
    >>> decompressed_length('(25x3)(3x3)ABC(2x3)XY(5x2)PQRSTX(18x9)(3x2)TWO(5x7)SEVEN')
    445
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
    total_length = 0

    # fulltext = ''

    while re.search(pattern, text):
        match = re.search(pattern, text)

        prefix = text[:match.start()]
        total_length += len(prefix)
        # fulltext += prefix

        # print('prefix:', prefix, file=sys.stderr)
        #
        text = text[match.end():]  # Remove the marker

        data_length, multiplier = findints(match.group())
        data = text[:data_length]
        # total_length += len(data) * multiplier

        text = text[data_length:]  # Remove the data section
        text = (data * multiplier) + text

        # print('text:', text, file=sys.stderr)
        # print('fulltext:', fulltext, file=sys.stderr)

    total_length += len(text)

    return total_length


if __name__ == '__main__':
    main()
