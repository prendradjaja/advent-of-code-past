DIRECTIONS = {
    '^': (-1, 0),
    '>': (0, 1),
    '<': (0, -1),
    'v': (1, 0),
}


def main():
    pos = (0, 0)
    seen = {pos}
    for move in open('in').read().strip():
        offset = DIRECTIONS[move]
        pos = addvec(pos, offset)
        seen.add(pos)
    answer = len(seen)
    print(answer)


def addvec(a, b):
    return tuple(x + y for (x, y) in zip(a, b))


main()
