from collections import defaultdict
from util import *

def main():
    programs = {}
    for line in open('input.txt'):
        program, *neighbors = findints(line)
        programs[program] = neighbors
    ccs = connected_components_undirected(programs)

    print('Answer for part 1:', len(ccs[0]))
    print('Answer for part 2:', len(ccs))

def connected_components_undirected(graph):
    unvisited = set(graph)
    ccs = defaultdict(list)
    while unvisited:
        node = one(unvisited, only=False)
        dfs(node, node, graph, unvisited, ccs)
    return ccs

def dfs(u, component_name, graph, unvisited, ccs):
    ccs[component_name].append(u)
    unvisited.remove(u)
    for v in graph[u]:
        if v in unvisited:
            dfs(v, component_name, graph, unvisited, ccs)

if __name__ == '__main__':
    main()
