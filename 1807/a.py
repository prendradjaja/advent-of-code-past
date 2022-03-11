import sys
import collections
import re


def main():
    f = open(sys.argv[1] if len(sys.argv) > 1 else 'in')
    lines = [l.rstrip('\n') for l in f]

    g = DiGraph()
    for line in lines:
        v, w = re.fullmatch(r'Step (.) must be finished before step (.) can begin\.', line).groups()
        g.add_edge(v, w)

    print(''.join(linearize_destructive(g)))


def linearize_destructive(g):
    result = []
    for _ in range(len(g.get_vertices())):
        v = sorted(g.get_sources())[0]
        result.append(v)
        for w in g.get_neighbors(v):
            g.remove_edge(v, w)
        g.remove_vertex(v)
    return result


# TODO Try just using networkx
class DiGraph:
    def __init__(self):
        self._edges = collections.defaultdict(set)
        self._reverse_edges = collections.defaultdict(set)
        self._vertices = set()

    def get_vertices(self):
        return [*self._vertices]

    def add_edge(self, v, w):
        self._edges[v].add(w)
        self._reverse_edges[w].add(v)
        self._vertices.add(v)
        self._vertices.add(w)

    def remove_edge(self, v, w):
        self._edges[v].remove(w)
        self._reverse_edges[w].remove(v)

    def remove_vertex(self, v):
        self._vertices.remove(v)

    def get_neighbors(self, v):
        return [*self._edges[v]]

    def is_source(self, v):
        return not self._reverse_edges[v]

    def get_sources(self):
        result = []
        for v in self.get_vertices():
            if self.is_source(v):
                result.append(v)
        return result


if __name__ == '__main__':
    main()
