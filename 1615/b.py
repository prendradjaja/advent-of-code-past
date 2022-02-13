# TODO Solve using system of modular equations (Chinese remainder theorem)

import sys
import collections
import itertools
from util import findints


Disc = collections.namedtuple('Disc', 'index positions_count start_position')


def main():
    # Read file
    f = open(sys.argv[1] if len(sys.argv) > 1 else 'in')
    lines = [l.rstrip('\n') for l in f]
    lines.append('Disc #7 has 11 positions; at time=0, it is at position 0.')

    # Parse
    discs = {}
    for line in lines:
        index, positions_count, _zero, start_position = findints(line)
        discs[index] = Disc(index, positions_count, start_position)

    # Solve
    for n in itertools.count():
        if falls_through(discs, n):
            break
    print(n)


def falls_through(discs, drop_time):
    return all(
        get_position(disc, drop_time + index) == 0
        for index, disc in discs.items()
    )


def get_position(disc, time):
    return (disc.start_position + time) % disc.positions_count


if __name__ == '__main__':
    main()
