import math
import sys
from gridlib import gridsource as gridlib
from util import consecutives, enumerate2d


def main():
    global asteroids, grid

    f = open(sys.argv[1] if len(sys.argv) > 1 else 'in')
    grid = [l.rstrip('\n') for l in f]
    asteroids = [pos for pos, value in enumerate2d(grid) if value == '#']

    answer = max(count_visible_from(pos) for pos in asteroids)
    print(answer)


def count_visible_from(a):
    angles = []
    for b in asteroids:
        if a == b:
            continue
        offset = gridlib.subvec(b, a)
        angle = math.atan2(offset[1], offset[0])
        angles.append(angle)

    angles.sort()
    unique_angles = 1
    for prev, curr in consecutives(angles):
        if not float_equals(prev, curr):
            unique_angles += 1
    return unique_angles


def float_equals(a, b, EPSILON=0.000000001):
    return abs(a - b) < EPSILON


def in_bounds(pos):
    r, c = pos
    return (
        0 <= r < len(grid) and
        0 <= c < len(grid[0])
    )


if __name__ == '__main__':
    main()
