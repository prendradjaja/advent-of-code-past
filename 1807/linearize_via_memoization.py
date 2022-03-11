import sys
import functools
import collections
import re


def main():
    print("This doesn't work to solve the given problem because we need a specific linearization, not just any linearization. (But it's fun)")

    f = open(sys.argv[1] if len(sys.argv) > 1 else 'in')
    lines = [l.rstrip('\n') for l in f]

    g = DiGraph()
    for line in lines:
        v, w = re.fullmatch(r'Step (.) must be finished before step (.) can begin\.', line).groups()
        g.add_edge(v, w)

    print(''.join(linearize(g)))


def linearize(g):
    result = []
    unvisited = set(g.get_vertices())

    # This implementation of traverse() is equivalent to the commented-out
    # version below, but this one is funnier
    @functools.cache
    def traverse(v):
        for w in g.get_neighbors(v):
            traverse(w)
        result.append(v)
        unvisited.remove(v)

    while unvisited:
        node = next(iter(unvisited))  # Pick an arbitrary node
        traverse(node)

    return list(reversed(result))

    # # No decorator
    # def traverse(v):
    #     if v in unvisited:
    #         for w in g.get_neighbors(v):
    #             traverse(w)
    #         result.append(v)
    #         unvisited.remove(v)


class DiGraph:
    def __init__(self):
        self._edges = collections.defaultdict(set)
        self._vertices = set()

    def get_vertices(self):
        return [*self._vertices]

    def add_edge(self, v, w):
        self._edges[v].add(w)
        self._vertices.add(v)
        self._vertices.add(w)

    def get_neighbors(self, v):
        return [*self._edges[v]]


if __name__ == '__main__':
    main()
