import fileinput, collections, collections as cl, itertools, itertools as it, math, random, sys, re, string, functools
from grid import gridsource as grid, gridcustom # *, gridsource, gridcardinal, gridplane
from util import *

def main():
    numbers, n = [6,19,0,5,7,13,1], 2020-1
    numbers, n = [0,3,6], 10-1

    for i, x in zip(range(1, n+1), game(numbers)):
        print(f'{i}th:', x)

def obj(**kwargs):
    result = types.SimpleNamespace()
    for key, value in kwargs.items():
        setattr(result, key, value)
    return result

def game(numbers):
    log = []
    last_spoken = {}
    for i, n in enumerate(numbers, start=1):
        log.append(obj(
            value = n,
            prev = None,
            i = i,
        ))
        yield n
        last_spoken[n] = i

    while True:
        i += 1
        last = log[-1]
        print(last)
        return

def nth(iterable, n):
    return next(it.islice(iterable, n, n+1))

main() # if __name__ == '__main__' and not sys.flags.inspect: main()
