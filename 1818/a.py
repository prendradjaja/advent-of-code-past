import collections
import sys
import copy
from gridlib import gridsource as gridlib
from util import enumerate2d, listify


OPEN = '.'
TREES = '|'
LUMBERYARD = '#'


def main():
    # Parse
    f = open(sys.argv[1] if len(sys.argv) > 1 else 'in')
    lines = f.read().splitlines()
    grid = [list(line) for line in lines]

    # Simulate
    for _ in range(10):
        grid = step(grid)

    # Count
    counts = collections.Counter()
    for _, value in enumerate2d(grid):
        counts[value] += 1
    print(counts[TREES] * counts[LUMBERYARD])


def step(grid):
    result = copy.deepcopy(grid)

    for pos, value in enumerate2d(grid):
        neighbors = get_neighbors(grid, pos)

        # "An open acre will become filled with trees if three or more
        # adjacent acres contained trees. Otherwise, nothing happens."
        if value == OPEN and neighbors.count(TREES) >= 3:
            gridlib.setindex(result, pos, TREES)

        # "An acre filled with trees will become a lumberyard if three or more
        # adjacent acres were lumberyards. Otherwise, nothing happens."
        if value == TREES and neighbors.count(LUMBERYARD) >= 3:
            gridlib.setindex(result, pos, LUMBERYARD)

        # "An acre containing a lumberyard will remain a lumberyard if it was
        # adjacent to at least one other lumberyard and at least one acre
        # containing trees. Otherwise, it becomes open."
        if value == LUMBERYARD:
            if neighbors.count(LUMBERYARD) >= 1 and neighbors.count(TREES) >= 1:
                pass  # Remain a lumberyard
            else:
                gridlib.setindex(result, pos, OPEN)

    return result


@listify
def get_neighbors(grid, pos):
    for offset in gridlib.neighborvecs:
        neighbor = gridlib.addvec(pos, offset)
        if in_bounds(grid, neighbor):
            yield gridlib.getindex(grid, neighbor)


def in_bounds(grid, pos):
    x1, x2 = pos
    len1 = len(grid)
    len2 = len(grid[0])
    return 0 <= x1 < len1 and 0 <= x2 < len2


if __name__ == '__main__':
    main()
