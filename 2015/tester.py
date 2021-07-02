import itertools as it

def tester(game):
    numbers, n, prog = [6,19,0,5,7,13,1], 2020-1, 100
    print(nth(game(numbers), n))

    numbers, n, prog = [6,19,0,5,7,13,1], 3000000-1, 1000000
    print(nth(game(numbers), n))

def nth(iterable, n):
    return next(it.islice(iterable, n, n+1))
