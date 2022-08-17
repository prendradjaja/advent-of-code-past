import math
import sys
import itertools
from gridlib import gridsource as gridlib
from util import consecutives, enumerate2d, obj
from termcolor import cprint


def main():
    def distance_from_laser(pos):
        return gridlib.absmanhattan(gridlib.subvec(pos, laser))

    global asteroids, grid

    f = open(sys.argv[1] if len(sys.argv) > 1 else 'in')
    grid = [l.rstrip('\n') for l in f]
    asteroids = [pos for pos, value in enumerate2d(grid) if value == '#']

    # Find where to place the laser (i.e. solve part 1)
    laser = max(asteroids, key=count_visible_from)

    groups = group_by_angle(laser)
    for group in groups:
        group.sort(key=lambda item: distance_from_laser(item.asteroid))

    print('First two asteroids to be destroyed:')
    groups = itertools.cycle(groups)
    vaporized = []
    for i in range(
        min(
            200,  # This value will be used for puzzle input and big example
            len(asteroids) - 1  # This value will be used for small example
        )
    ):
        group = next(groups)
        while not group:
            group = next(groups)
        item = group.pop(0)
        vaporized.append(item.asteroid)
        if i < 2:
            show(grid, laser, vaporized)

    if len(asteroids) > 200:  # Skip this step for the small example, since there is no 200th asteroid destroyed
        x = item.asteroid[1]
        y = item.asteroid[0]
        answer = 100 * x + y
        print('Answer:')
        print(answer)


def show(grid, laser, vaporized):
    for r, row in enumerate(grid):
        for c, value in enumerate(row):
            pos = (r, c)
            if pos == laser:
                cprint('X', color='green', end='')
            elif pos in vaporized:
                cprint('O', color='red', end='')
            else:
                print(value, end='')
        print()
    print()


def count_visible_from(a):
    return len(group_by_angle(a))


def group_by_angle(a):
    items = []
    for b in asteroids:
        if a == b:
            continue
        offset = gridlib.subvec(b, a)
        angle = -math.atan2(-offset[1], -offset[0])
        if float_equals(angle, 0):
            angle = 0
        elif angle < 0:
            angle += 2 * math.pi
        items.append(obj(asteroid=b, angle=angle))

    items.sort(key=lambda a: a.angle)
    return groupby(items, lambda a, b: float_equals(a.angle, b.angle))


def groupby(lst, eq):
    '''
    Similar to itertools.groupby, but uses an equality-check function instead
    of a key function.

    The return type is a bit different (no key), and it uses lists instead of
    iterators.
    '''
    groups = [[lst[0]]]
    for prev, curr in consecutives(lst):
        if not eq(prev, curr):
            groups.append([])
        groups[-1].append(curr)
    return groups


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
