import fileinput, collections, collections as cl, itertools, itertools as it, math, random, sys, re, string, functools
from gridlib import gridsource as gridlib, gridcustom # *, gridsource, gridcardinal, gridplane
from util import *

from termcolor import colored
import os


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


    frontier = [(500, 0)]

    # while True:
    #     tick(grid, 13, frontier)
    #     show(grid, 494, 507, 0, 15, color=True)
    #     input()
    #     os.system('clear')

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
        tick(grid, ylimit, frontier)
        waters = count(grid)
        if ticks % 10 == 0:
            print(ticks, f'{waters:,}')
        if waters == last_waters:
            break
        last_waters = waters

    if ylimit < 100:
        show(grid, 494, 507, 0, 16, color=True)

    print(waters)


def get(d, key):
    '''
    Given a defaultdict, return d[key] if it exists.

    If it doesn't exist, return the dict's default value -- without actually mutating the dict!
    '''
    if key in d:
        return d[key]
    else:
        return d.default_factory()


def tick(grid, ylimit, frontier):
    new_frontier = []
    for pos in frontier:
        # assert get(grid, pos) in '|+'
        if not get(grid, pos) in '|+':
            continue

        value = get(grid, pos)
        below_pos = gridlib.addvec(pos, DOWN)
        below_value = get(grid, below_pos)
        if below_value == ',':
            if below_pos[1] <= ylimit:
                grid[below_pos] = '|'
                new_frontier.append(below_pos)
        else:
            left_pos = gridlib.addvec(pos, LEFT)
            left_value = get(grid, left_pos)
            right_pos = gridlib.addvec(pos, RIGHT)
            right_value = get(grid, right_pos)
            if left_value == ',':
                grid[left_pos] = '|'
            if right_value == ',':
                grid[right_pos] = '|'
            settled, climbs = maybe_settle(grid, pos)
            if not settled:
                if left_value == ',':
                    new_frontier.append(left_pos)
                if right_value == ',':
                    new_frontier.append(right_pos)
            if settled:
                new_frontier.extend(climbs)

    frontier[:] = new_frontier


def maybe_settle(grid, origin):
    assert get(grid, origin) == '|'

    left_edge = origin
    pos = origin
    while get(grid, pos) == '|':
        pos = gridlib.addvec(pos, LEFT)
    left_edge = pos

    right_edge = origin
    pos = origin
    while get(grid, pos) == '|':
        pos = gridlib.addvec(pos, RIGHT)
    right_edge = pos

    segment = ''
    for x in range(left_edge[0], right_edge[0]+1):
        y = origin[1]
        segment += get(grid, (x, y))

    middle = segment[1:-1]
    is_shut_in = segment[0] == segment[-1] == '#'

    climbs = None

    if is_shut_in:
        for x in range(left_edge[0]+1, right_edge[0]):
            y = origin[1]
            grid[(x, y)] = '~'
        climbs = []
        for x in range(left_edge[0]+1, right_edge[0]):
            y = origin[1] - 1
            if get(grid, (x, y)) == '|':
                climbs.append((x, y))

    return is_shut_in, climbs



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
