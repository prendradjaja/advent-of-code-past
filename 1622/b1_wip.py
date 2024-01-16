#!/usr/bin/env python3
'''
Usage:
    ./b1.py PATH_TO_INPUT_FILE
'''

import sys
import re
from collections import namedtuple
import itertools
import statistics


Node = namedtuple('Node', 'size used avail type')


def main():
    nodes = {}
    for line in open(sys.argv[1]).read().splitlines():
        if not line.startswith('/dev'):
            continue
        x, y, size, used, avail, _ = [
            int(n)
            for n in
            re.findall(r'\d+', line)
        ]
        nodes[(x, y)] = Node(size, used, avail, type)

    answer = sum(
        1
        for a, b in itertools.permutations(nodes.values(), 2)
        if a.used != 0 and a.used <= b.avail
    )

    cutoff = 2 * statistics.median([node.size for node in nodes.values()])

    xmin = min(x for x, y in nodes)
    xmax = max(x for x, y in nodes)
    ymin = min(y for x, y in nodes)
    ymax = max(y for x, y in nodes)
    for y in range(ymin, ymax+1):
        for x in range(xmin, xmax+1):
            node = nodes[x, y]
            if node.used == 0:
                ch = '_'
            elif node.size < cutoff:
                ch = '.'
            else:
                ch = '#'
            print(ch, end='')
        print()


if __name__ == '__main__':
    main()
