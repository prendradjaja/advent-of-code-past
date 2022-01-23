import sys


def main():
    f = open(sys.argv[1] if len(sys.argv) > 1 else 'in')

    answer = pipe(f.read().strip(), [
        strip_whitespace,
        decompress,
        len
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

    chars = list(text)
    state_name = 0
    marker_length_string = ''
    multiplier_string = ''
    output = ''

    while chars:
        ch, *chars = chars
        if state_name == 0:
            if ch == '(':
                state_name = 1
            else:
                output += ch
        elif state_name == 1:
            if ch in '0123456789':
                marker_length_string += ch
            elif ch == 'x':
                state_name = 2
            else:
                raise Error('Expected x or [0-9]')
        elif state_name == 2:
            if ch in '0123456789':
                multiplier_string += ch
            elif ch == ')':
                state_name = 0
                marker_length = int(marker_length_string)
                multiplier = int(multiplier_string)
                marker_length_string = ''
                multiplier_string = ''
                assert marker_length <= len(chars)
                data = ''.join(chars[:marker_length])
                chars[:marker_length] = []
                output += data * multiplier
            else:
                raise Error('Expected ) or [0-9]')
        else:
            raise Error('Unreachable')

    return output


if __name__ == '__main__':
    main()
