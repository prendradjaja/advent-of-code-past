"""
Reuse my solution from Year 2021 Day 22 :)

For that problem, I implemented n-dimensional "region subtraction". For n = 1,
this is interval subtraction.
"""

import sys
from util import ints
from aoc_2021_22 import region_subtract


# Data type:
#
# Interval: (lo: int, hi: int)
# - An interval on the integers.
# - Endpoints are inclusive.
# - Example: (1, 4) represents the interval containing 1, 2, 3, and 4.


def main():
    valid_ips = [(0, 4294967295)]  # A list of intervals describing valid IPs

    f = open(sys.argv[1] if len(sys.argv) > 1 else 'in')
    lines = [l.rstrip('\n') for l in f]
    for line in lines:
        left, right = ints(line.split('-'))
        interval = (left, right)

        valid_ips = flatten(
            [interval_subtract(existing, interval) for existing in valid_ips]
        )

    valid_ips = list(sorted(valid_ips))
    print('Part 1 answer:')
    print(valid_ips[0][0])

    allowed_count = 0
    for interval in valid_ips:
        interval_size = interval[1] - interval[0] + 1
        allowed_count += interval_size
    print('\nPart 2 answer:')
    print(allowed_count)


def flatten(t):
    return [item for sublist in t for item in sublist]


def interval_subtract(ia, ib):
    '''
    interval_subtract() is a simple wrapper around region_subtract() that
    makes it more ergonomic to use for the 1-dimensional case.

    Example:
    >>> interval_subtract((1, 10), (2, 4))
    [(1, 1), (5, 10)]

    Previous example is equivalent to this region_subtract() call:
    >>> region_subtract(((1, 10),), ((2, 4),))  # region_subtract, NOT interval_subtract()
    [((1, 1),), ((5, 10),)]

    Other test cases:
    >>> interval_subtract((1, 10), (20, 40))
    [(1, 10)]
    >>> interval_subtract((1, 10), (5, 10))
    [(1, 4)]

    '''
    ra = (ia,)
    rb = (ib,)
    result = []
    for region in region_subtract(ra, rb):
        interval = region[0]
        result.append(interval)
    return result


if __name__ == '__main__':
    main()
