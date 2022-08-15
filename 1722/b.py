import sys
import collections
from gridlib import gridsource as gridlib
from util import enumerate2d


DIRECTIONS = [
    RIGHT := (0, 1),
    DOWN := (1, 0),
    LEFT := (0, -1),
    UP := (-1, 0),
]


def main():
    f = open(sys.argv[1] if len(sys.argv) > 1 else 'in')
    lines = f.read().splitlines()
    grid = collections.defaultdict(lambda: '.')
    for pos, pixel in enumerate2d(lines):
        grid[pos] = pixel

    carrier_position = (len(lines) // 2, len(lines[0]) // 2)  # midpoint
    carrier_direction = UP

    infections = 0
    for i in range(10_000_000):
        if i % 100_000 == 0:
            print(f'... {i / 10_000_000:%}')

        # Turn
        if grid[carrier_position] == '.':
            carrier_direction = rotate(carrier_direction, clockwise=False)
        elif grid[carrier_position] == 'W':
            pass
        elif grid[carrier_position] == '#':
            carrier_direction = rotate(carrier_direction, clockwise=True)
        elif grid[carrier_position] == 'F':
            carrier_direction = rotate(carrier_direction, clockwise=True)
            carrier_direction = rotate(carrier_direction, clockwise=True)
        else:
            1/0

        # Clean or infect (or weaken or flag)
        if grid[carrier_position] == '.':
            grid[carrier_position] = 'W'
        elif grid[carrier_position] == 'W':
            grid[carrier_position] = '#'
            infections += 1
        elif grid[carrier_position] == '#':
            grid[carrier_position] = 'F'
        elif grid[carrier_position] == 'F':
            grid[carrier_position] = '.'
        else:
            1/0

        # Move forward
        carrier_position = gridlib.addvec(carrier_position, carrier_direction)

    print(infections)


def rotate(current_direction, *, clockwise):
    if clockwise:
        idx = (DIRECTIONS.index(current_direction) + 1) % len(DIRECTIONS)
    else:
        idx = (DIRECTIONS.index(current_direction) - 1) % len(DIRECTIONS)
    return DIRECTIONS[idx]


if __name__ == '__main__':
    main()
