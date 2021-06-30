# Doesn't implement the whole connected components algorithm, just what's reachable from program 0

from collections import defaultdict
from util import *

def main():
    programs = {}
    for line in open('input.txt'):
        program, *neighbors = findints(line)
        programs[program] = neighbors
    reachable = []
    unvisited = set(programs)
    dfs(0, programs, unvisited, reachable)

    print('Answer for part 1:', len(reachable))

def dfs(u, graph, unvisited, reachable):
    reachable.append(u)
    unvisited.remove(u)
    for v in graph[u]:
        if v in unvisited:
            dfs(v, graph, unvisited, reachable)

if __name__ == '__main__':
    main()
