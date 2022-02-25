# import fileinput, collections, collections as cl, itertools, itertools as it, math, random, sys, re, string, functools
# from gridlib import gridsource as gridlib, gridcustom # *, gridsource, gridcardinal, gridplane
# from util import *
# from math import inf

import itertools
import collections
import sys
from gridlib import gridsource as gridlib
from util import findints
from math import inf


Node = collections.namedtuple('Node', 'x y size used avail pctused')


def main():
    f = open(sys.argv[1] if len(sys.argv) > 1 else 'in')
    lines = [l.rstrip('\n') for l in f]
    nodes = {}
    xmin = 0
    ymin = 0
    xmax = -inf
    ymax = -inf
    for line in lines:
        if '/dev' not in line:
            continue
        node = Node(*findints(line.replace('-', ' ')))
        nodes[pos(node)] = node
        xmax = max(xmax, node.x)
        ymax = max(ymax, node.y)

    # def neighbors(node):
    #     for offset in gridlib.directions:
    #         npos = gridlib.addvec(pos(node), offset)
    #         if (
    #             xmin <= npos.x <= xmax and
    #             ymin <= npos.y <= ymax
    #         ):
    #             yield nodes[npos]

    answer = 0
    for a, b in itertools.product(nodes.values(), repeat=2):
        if (
            a != b
            and a.used != 0
            and a.used <= b.avail
        ):
            answer += 1
    print(answer)


def pos(node):
    return (node.x, node.y)


if __name__ == '__main__':
    main()
