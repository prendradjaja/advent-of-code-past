import sys
from gridlib import gridsource as gridlib
from copy import deepcopy

from progress import ProgressBar


def main():
    f = open('in')
    grid = [list(l.rstrip('\n')) for l in f]

    print('Part 1 answer:', count_on(simulate(deepcopy(grid), 100, show_progress=True)))

    print()
    print('Part 2 answer:', count_on(simulate(deepcopy(grid), 100, show_progress=True, corners_on=True)))


def simulate(grid, steps, /, corners_on=False, show_progress=False):
    '''
    Warning: May mutate the grid!

    >>> problem_input = [list(l.rstrip('\\n')) for l in open('in')]
    >>> example_input = [list(l.rstrip('\\n')) for l in open('ex')]

    >>> count_on(simulate(deepcopy(example_input), 4))
    4

    >>> count_on(simulate(deepcopy(example_input), 5, corners_on=True))
    17

    # >>> count_on(simulate(deepcopy(problem_input), 100))
    # 768

    # >>> count_on(simulate(deepcopy(problem_input), 100))
    # 781
    '''
    if show_progress: progress = ProgressBar(100)
    if corners_on: light_corners(grid)

    for i in range(steps):
        grid = step(grid)

        if show_progress: progress.show(i + 1)
        if corners_on: light_corners(grid)

    if show_progress: progress.done()

    return grid


def step(grid):
    '''
    Warning: May mutate the grid!
    '''
    newgrid = []
    height, width = dimensions(grid)
    for _ in range(height):
        row = [None] * width
        newgrid.append(row)

    for r in range(height):
        for c in range(width):
            onnei = 0
            for each in neighbors(grid, (r, c)):
                if each == '#':
                    onnei += 1
            if onnei in [2, 3] and gridlib.getindex(grid, (r, c)) == '#':
                gridlib.setindex(newgrid, (r, c), '#')
            elif onnei in [3] and gridlib.getindex(grid, (r, c)) == '.':
                gridlib.setindex(newgrid, (r, c), '#')
            else:
                gridlib.setindex(newgrid, (r, c), '.')

    return newgrid


def neighbors(grid, pos):
    height = len(grid)
    width = len(grid[0])
    for offset in gridlib.neivecs:
        nei = gridlib.addvec(offset, pos)
        r, c = nei
        if 0 <= r < height and 0 <= c < width:
            yield gridlib.getindex(grid, nei)


def dimensions(grid):
    height = len(grid)
    width = len(grid[0])
    return height, width


def count_on(grid):
    height, width = dimensions(grid)
    result = 0
    for r in range(height):
        for c in range(width):
            result += int(gridlib.getindex(grid, (r, c)) == '#')
    return result


def light_corners(grid):
    '''
    Warning: May mutate the grid!
    '''
    height, width = dimensions(grid)
    gridlib.setindex(grid, (0,        0),       '#')
    gridlib.setindex(grid, (height-1, 0),       '#')
    gridlib.setindex(grid, (0,        width-1), '#')
    gridlib.setindex(grid, (height-1, width-1), '#')


if __name__ == '__main__':
    main()
