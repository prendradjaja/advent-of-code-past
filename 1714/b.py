import sys
from collections import defaultdict

from util import enumerate2d

from day10 import knot_hash


MY_PUZZLE_INPUT = 'amgozmfv'


def main():
    sys.setrecursionlimit(20000)

    puzzle_input = sys.argv[1] if len(sys.argv) > 1 else MY_PUZZLE_INPUT

    grid = []
    for row in range(128):
        hexstring = knot_hash(f'{puzzle_input}-{row}')
        number = int(hexstring, 16)
        bitstring = f'{number:0128b}'
        grid.append(bitstring)

    print(len(connected_components(grid)))


def connected_components(grid):
    '''
    Adapted from day 12 solution
    '''
    ccs = defaultdict(list)
    visited = set()
    for pos, value in enumerate2d(grid):
        if value == '1':
            dfs(pos, pos, grid, visited, ccs)
    return ccs


def dfs(u, component_name, grid, visited, ccs):
    if u in visited:
        return
    ccs[component_name].append(u)
    visited.add(u)
    for v in neighbors(u, grid):
        dfs(v, component_name, grid, visited, ccs)


def neighbors(u, grid):
    for offset in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
        v = (u[0] + offset[0], u[1] + offset[1])
        if (
            0 <= v[0] < 128 and
            0 <= v[1] < 128 and
            grid[v[0]][v[1]] == '1'
        ):
            yield v


if __name__ == '__main__':
    main()
