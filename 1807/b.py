import sys
import collections
import re


def main():
    print('Example input:')
    simulate(
        path = 'ex',
        min_step_duration = 1,
        count_workers = 2,
        omit = [],
    )

    print('\nPuzzle input:')
    simulate(
        path = 'in',
        min_step_duration = 61,
        count_workers = 5,
        omit = range(5, 1260),
    )


def simulate(path, min_step_duration, count_workers, omit):
    def step_duration(step):
        return ord(step) - ord('A') + min_step_duration

    def get_next_step():
        sources = sorted(g.get_sources())
        available = [step for step in sources if step not in time_left]
        if available:
            return available[0]
        else:
            return None

    f = open(path)
    lines = [l.rstrip('\n') for l in f]

    g = DiGraph()
    for line in lines:
        v, w = re.fullmatch(r'Step (.) must be finished before step (.) can begin\.', line).groups()
        g.add_edge(v, w)

    # While a worker W is working on a step S,
    #     workers[W] = S
    #     time_left[S] = WHATEVER_TIME_LEFT
    time_left = {}
    workers = { w: None for w in range(1, count_workers+1) }

    done = ''
    count_steps = len(g.get_vertices())
    second = 0
    while len(done) < count_steps:
        for worker in workers:
            if step := workers[worker]:
                time_left[step] -= 1
                if time_left[step] == 0:
                    done += step
                    workers[worker] = None
                    del time_left[step]
                    for next_step in g.get_neighbors(step):
                        g.remove_edge(step, next_step)
                    g.remove_vertex(step)
            if not workers[worker]:
                if step := get_next_step():
                    workers[worker] = step
                    time_left[step] = step_duration(step)
        if second in omit and second == omit[0]:
            print(f'\t({len(omit)} rows omitted)')
        if second not in omit:
            TAB = '\t'
            summary = (
                TAB
                + str(second)
                + TAB
                + TAB.join(str(v or ".") for v in workers.values())
                + TAB
                + done
            )
            print(summary)
        second += 1


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
