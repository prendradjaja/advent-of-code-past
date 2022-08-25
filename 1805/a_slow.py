# import fileinput, collections, collections as cl, itertools, itertools as it, math, random, sys, re, string, functools
# from gridlib import gridsource as gridlib, gridcustom # *, gridsource, gridcardinal, gridplane
from util import consecutives
import sys


def main():
    f = open(sys.argv[1] if len(sys.argv) > 1 else 'in')
    polymer = f.read().strip()
    changed = True
    i = 0
    while changed:
        polymer, changed = react(polymer)
        if i % 2000 == 0:
            print('Still reacting... Polymer length is currently', len(polymer))
        i += 1
    print('\nAnswer:')
    print(len(polymer))


def react(polymer):
    for i, (a, b) in enumerate(consecutives(polymer)):
        if a != b and a.lower() == b.lower():
            break
    else:
        return polymer, False

    polymer = polymer[:i] + polymer[i+2:]
    return polymer, True


if __name__ == '__main__':
    main()
