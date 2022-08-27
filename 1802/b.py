import sys
import collections
import itertools


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else 'in'
    boxids = open(path).read().strip().splitlines()
    for x, y in itertools.combinations(boxids, 2):
        if match(x, y):
            print(common(x, y))
            break


def common(id1, id2):
    result = ''
    for x, y in zip(id1, id2):
        if x == y:
            result += x
    return result


def match(id1, id2):
    assert len(id1) == len(id2)
    return len(common(id1, id2)) == len(id1) - 1


main()
