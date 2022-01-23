import sys
import re
from util import findints


def main():
    f = open(sys.argv[1] if len(sys.argv) > 1 else 'in')
    pipe(f.read().strip(), [
        strip_whitespace,
        decompressed_length,
        print,
    ])


def pipe(x, fns):
    for fn in fns:
        x = fn(x)
    return x


def strip_whitespace(text):
    return ''.join(ch for ch in text if not ch.isspace())


def decompressed_length(text):
    '''
    >>> decompressed_length('(3x3)XYZ')
    9
    >>> decompressed_length('X(8x2)(3x3)ABCY')
    20
    >>> decompressed_length('(27x12)(20x12)(13x14)(7x10)(1x12)A')
    241920
    >>> decompressed_length('(25x3)(3x3)ABC(2x3)XY(5x2)PQRSTX(18x9)(3x2)TWO(5x7)SEVEN')
    445
    '''
    if match := re.search(r'\(\d+x\d+\)', text):
        total_length = 0

        prefix = text[:match.start()]
        total_length += len(prefix)

        # Remove marker from text
        text = text[match.end():]

        data_length, multiplier = findints(match.group())

        # Remove data from text
        data = text[:data_length]
        text = text[data_length:]

        # Recurse into data
        total_length += multiplier * decompressed_length(data)
        # Recurse into remainder of text
        total_length += decompressed_length(text)
        return total_length
    else:
        return len(text)


if __name__ == '__main__':
    main()
