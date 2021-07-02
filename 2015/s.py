import fileinput, collections, collections as cl, itertools, itertools as it, math, random, sys, re, string, functools
from grid import gridsource as grid, gridcustom # *, gridsource, gridcardinal, gridplane
from util import *
from game1 import game as game1
from game2 import game as game2
from game3 import game as game3
from game4 import game as game4

def main():
    numbers, n, prog = [6,19,0,5,7,13,1], 2020-1, 100
    numbers, n, prog = [6,19,0,5,7,13,1], 30000000-1, 1000000
    # numbers, n = [0,3,6], 10-1

    game = game4

    for i, x in zip(range(1, n+2), game(numbers)):
        if i % prog == 0 or i == n + 1:
            print(f'{i}th:', x)

def nth(iterable, n):
    return next(it.islice(iterable, n, n+1))

main() # if __name__ == '__main__' and not sys.flags.inspect: main()
