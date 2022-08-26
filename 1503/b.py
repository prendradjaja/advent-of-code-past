DIRECTIONS = {
    '^': (-1, 0),
    '>': (0, 1),
    '<': (0, -1),
    'v': (1, 0),
}


def main():
    santa = (0, 0)
    robo = (0, 0)
    seen = {(0, 0)}
    moves = iter(open('in').read().strip())

    while True:
        try:
            move = next(moves)
            santa = addvec(santa, DIRECTIONS[move])
            seen.add(santa)

            move = next(moves)
            robo = addvec(robo, DIRECTIONS[move])
            seen.add(robo)

        except StopIteration:
            break

    answer = len(seen)
    print(answer)


def addvec(a, b):
    return tuple(x + y for (x, y) in zip(a, b))


main()
