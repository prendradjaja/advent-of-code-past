import fileinput, collections, collections as cl, itertools, itertools as it, math, random, sys, re, string, functools
from gridlib import gridsource as gridlib, gridcustom # *, gridsource, gridcardinal, gridplane
from util import *

from termcolor import colored


DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)


def count(grid):
    waters = 0
    for value in grid.values():
        if value in '|~':
            waters += 1
    return waters


def main():
    input_path = sys.argv[1] if len(sys.argv) > 1 else 'in'
    grid = parse_input_file(input_path)
    grid[(500, 0)] = '+'

    xs = [x for (x, y) in grid]
    ys = [y for (x, y) in grid]
    # print(min(xs), max(xs))
    # print(min(ys), max(ys))
    # exit()

    # while True:
    #     tick(grid, max(ys))
    #     show(grid, 494, 507, 0, 16, color=True)
    #     import os
    #     input()
    #     os.system('clear')

    ylimit = max(ys)

    last_waters = 0
    ticks = 0
    while True:
        ticks += 1
        tick(grid, ylimit)
        waters = count(grid)
        if ticks % 10 == 0:
            print(ticks, f'{waters:,}')
        if waters == last_waters:
            break
        last_waters = waters

    if ylimit < 100:
        show(grid, 494, 507, 0, 16, color=True)

    print(waters)

    # for _ in range(2):
    #     tick(grid, max(ys))
    #     show(grid, 494, 507, 0, 13)

    # tick(grid, max(ys))
    # show(grid, 494, 507, 0, 13)
    #
    # tick(grid, max(ys))
    # show(grid, 494, 507, 0, 13)
    #
    # tick(grid, max(ys))
    # show(grid, 494, 507, 0, 13)
    #
    # tick(grid, max(ys))
    # show(grid, 494, 507, 0, 13)

def get(d, key):
    '''
    Given a defaultdict, return d[key] if it exists.

    If it doesn't exist, return the dict's default value -- without actually mutating the dict!
    '''
    if key in d:
        return d[key]
    else:
        return d.default_factory()


def tick(grid, ylimit):
    # Drop phase
    to_drop = []
    to_spread_from = []
    for pos, value in grid.items():
        below_pos = gridlib.addvec(pos, DOWN)
        below_value = get(grid, below_pos)
        if value in '+|' and below_value == ',':
            to_drop.append(below_pos)
        elif (
            value in '+|'
            and below_value in '#~'
            and (
                get(grid, gridlib.addvec(pos, LEFT)) == ','
                or get(grid, gridlib.addvec(pos, RIGHT)) == ','
            )
        ):
            to_spread_from.append(pos)
    for pos in to_drop:
        x, y = pos
        if y <= ylimit:
            grid[pos] = '|'

    # Spread phase
    for pos in to_spread_from:
        spread(grid, pos)


def spread(grid, origin):
    left_edge = origin
    pos = origin
    while (
        grid[pos] != '#' and
        grid[(below := gridlib.addvec(pos, DOWN))] in '~#'
    ):
        left_edge = pos
        pos = gridlib.addvec(pos, LEFT)

    right_edge = origin
    pos = origin
    while (
        grid[pos] != '#' and
        grid[(below := gridlib.addvec(pos, DOWN))] in '~#'
    ):
        right_edge = pos
        pos = gridlib.addvec(pos, RIGHT)

    char = '~'
    if (
        grid[gridlib.addvec(left_edge, LEFT)] == ',' and
        grid[gridlib.addvec(left_edge, LEFT, DOWN)] == ','
    ):
        char = '|'
        grid[gridlib.addvec(left_edge, LEFT)] = '|'

    if (
        grid[gridlib.addvec(right_edge, RIGHT)] == ',' and
        grid[gridlib.addvec(right_edge, RIGHT, DOWN)] == ','
    ):
        char = '|'
        grid[gridlib.addvec(right_edge, RIGHT)] = '|'

    for x in range(left_edge[0], right_edge[0]+1):
        grid[(x, origin[1])] = char


def parse_input_file(path):
    f = open(path)
    lines = [l.rstrip('\n') for l in f]
    grid = cl.defaultdict(lambda: ',')
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


def show(grid, xlo, xhi, ylo, yhi, *, color=False):
    for y in range(ylo, yhi+1):
        line = ''
        for x in range(xlo, xhi+1):
            value = grid[(x, y)]
            if not color:
                line += value
            else:
                if value == '#':
                    color = 'red'
                elif value == '~':
                    color = 'blue'
                elif value == '|':
                    color = 'cyan'
                elif value== '+':
                    color = 'yellow'
                else:
                    color = 'white'
                line += colored(value, color)
        print(line)
    print()


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
