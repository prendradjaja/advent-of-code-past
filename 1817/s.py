import fileinput, collections, collections as cl, itertools, itertools as it, math, random, sys, re, string, functools
from gridlib import gridsource as gridlib, gridcustom # *, gridsource, gridcardinal, gridplane
from util import *


def main():
    input_path = sys.argv[1] if len(sys.argv) > 1 else 'in'
    grid = parse_input_file(input_path)
    grid[(500, 0)] = '+'

    show(grid, 494, 507, 0, 13)


def parse_input_file(path):
    f = open(path)
    lines = [l.rstrip('\n') for l in f]
    grid = cl.defaultdict(lambda: '.')
    for line in lines:
        for pos in parse_line(line):
            grid[pos] = '#'
    return grid


def parse_line(line):
    if values := sscanf(line, 'x=%u, y=%u..%u'):
        x, ylo, yhi = values
        for y in range(ylo, yhi+1):
            yield (x, y)
    elif values := sscanf(line, 'y=%u, x=%u..%u'):
        y, xlo, xhi = values
        for x in range(xlo, xhi+1):
            yield (x, y)
    else:
        1/0


def show(grid, xlo, xhi, ylo, yhi):
    for y in range(ylo, yhi+1):
        line = ''.join(grid[(x, y)] for x in range(xlo, xhi+1))
        print(line)


def sscanf(s, fmt):
    '''
    Parses the string against the given template, returning the values of the
    slots. If no match, return None.

    The string must be a full match (like re.fullmatch()).

    Each slot is parsed non-greedily. (Is this a good approach?)

    Supported placeholders:
    %s: Scan a string. Unlike C sscanf(), the scan is not terminated at
        whitespace.
    %u: Scan for a nonnegative ("unsigned") integer.

    TODO Add support for %d

    >>> sscanf(
    ...     'The quick brown fox jumped over 2 lazy dogs',
    ...     'The %s brown fox jumped over %u lazy dogs',
    ... )
    ('quick', 2)

    >>> sscanf(
    ...     'quick fox, 2 dogs, 31 cats, wow!',
    ...     '%s fox, %u dogs, %u cats, %s',
    ... )
    ('quick', 2, 31, 'wow!')

    >>> sscanf(
    ...     'quick fox, 2 dogs, 31 cats',
    ...     '%s fox, %u dogs, %u cats, %s',
    ... ) == None
    True
    '''
    # Parse `fmt` into `pattern`
    slot_pattern = r'(%s|%u)'
    pattern = ''
    slot_types = []
    for part in re.split(slot_pattern, fmt):
        is_slot = bool(re.fullmatch(slot_pattern, part))
        if is_slot:
            slot_types.append(part)
            if part == '%s':
                pattern += r'(.+?)'
            elif part == '%u':
                pattern += r'(\d+?)'
            else:
                1/0  # Invalid placeholder
        else:
            pattern += re.escape(part)

    # Try to match
    match = re.fullmatch(pattern, s)
    if not match:
        return None

    # If match, parse values and return
    result = ()
    for raw_value, slot_type in zip(match.groups(), slot_types):
        if slot_type == '%s':
            value = raw_value
        elif slot_type == '%u':
            value = int(raw_value)
        result += (value,)
    return result


if __name__ == '__main__':
    main()
