#!/usr/bin/env python3
'''
Usage:
    ./a.py PATH_TO_INPUT_FILE
'''

import sys
import re
from collections import namedtuple
import itertools


Node = namedtuple('Node', 'size used avail')


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
        nodes[(x, y)] = Node(size, used, avail)

    answer = sum(
        1
        for a, b in itertools.permutations(nodes.values(), 2)
        if a.used != 0 and a.used <= b.avail
    )
    print(answer)


if __name__ == '__main__':
    main()
