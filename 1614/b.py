import functools
import itertools
import hashlib
from util import consecutives
from progress import ProgressBar


# puzzle_input = 'abc'
puzzle_input = 'cuanljph'


def main():
    progress = ProgressBar(64)
    for i, n in enumerate(key_indices(), start=1):
        progress.show(i)
        if i == 64:
            break

    print()
    print(n)


def key_indices():
    for n in itertools.count():
        has_triple, ch = triple_check(n)
        if has_triple:
            for p in range(n+1, n+1001):
                if quint_check(p, ch):
                    yield n
                    break


def triple_check(n):
    myhash = iterated_md5(f'{puzzle_input}{n}')
    for x, y, z in consecutives(myhash, 3):
        if x == y == z:
            return (True, x)
    return (False, None)


def quint_check(n, ch):
    myhash = iterated_md5(f'{puzzle_input}{n}')
    for v, w, x, y, z in consecutives(myhash, 5):
        if ch == v == w == x == y == z:
            return True
    return False


@functools.cache
def iterated_md5(s):
    for n in range(2016 + 1):
        s = md5(s)
    return s


def md5(asciistring):
    return hashlib.md5(asciistring.encode('utf-8')).hexdigest()

if __name__ == '__main__':
    main()
