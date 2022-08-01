import sys
import itertools
from collections import deque
from gridlib import gridsource as gridlib
from util import *


def main():
    global grid

    f = open(sys.argv[1] if len(sys.argv) > 1 else 'in')
    grid = [l.rstrip('\n') for l in f]
    digits = '123456789'

    start = find('0')
    targets = [t for t in digits if find(t)]

    print('Working... (should take up to about 1 minute)')
    answer = min(journey_length(each) for each in itertools.permutations(targets))
    print('Answer:')
    print(answer)


def journey_length(journey):
    length = 0
    for a, b in consecutives(('0',) + journey):
        length += distance(a, b)
    return length


def find(char_to_find):
    for r, row in enumerate(grid):
        for c, char in enumerate(row):
            if char == char_to_find:
                return r, c
    return None


@functools.cache
def bfs(node):
    visited = set()
    parents = {}  # parents[u] = v means the parent of u is v
    parents[node] = None
    visited.add(node)
    q = deque([node])
    while q:
        node = q.popleft()
        for v in neighbors(node):
            if v not in visited:
                parents[v] = node
                visited.add(v)
                q.append(v)
    return parents


def neighbors(node):
    for offset in gridlib.directions:
        neighbor = gridlib.addvec(node, offset)
        if gridlib.getindex(grid, neighbor) != '#':
            yield neighbor


def distance(n1, n2):
    n1 = find(n1)
    n2 = find(n2)
    parents = bfs(n1)
    result = 0
    while n2 != n1:
        result += 1
        n2 = parents[n2]
    return result


if __name__ == '__main__':
    main()
