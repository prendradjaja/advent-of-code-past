import collections


def main():
    boxids = open('in').read().strip().splitlines()
    answer = (
        len([x for x in boxids if has_double(x)]) *
        len([x for x in boxids if has_triple(x)])
    )
    print(answer)


def has_double(boxid):
    counts = collections.Counter(boxid)
    return 2 in counts.values()


def has_triple(boxid):
    counts = collections.Counter(boxid)
    return 3 in counts.values()


main()
