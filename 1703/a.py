UP = (-1, 0)
DOWN = (1, 0)
LEFT = (0, -1)
RIGHT = (0, 1)


def main():
    puzzle_input = 325489
    for i, pos in enumerate(spiral(999999), start=1):
        if i == puzzle_input:
            break
    answer = absmanhattan(pos)
    print(answer)


def spiral(layers):
    pos = (0, 0)
    yield pos
    for i in range(layers - 1):
        length = (i + 1) * 2
        pos = addvec(pos, RIGHT)
        for pos in make_line(pos, UP, length):
            yield pos
        pos = addvec(pos, LEFT)
        for pos in make_line(pos, LEFT, length):
            yield pos
        pos = addvec(pos, DOWN)
        for pos in make_line(pos, DOWN, length):
            yield pos
        pos = addvec(pos, RIGHT)
        for pos in make_line(pos, RIGHT, length):
            yield pos


def make_line(start, direction, count_points):
    pos = start
    yield pos
    for _ in range(count_points - 1):
        pos = addvec(pos, direction)
        yield pos


def addvec(v, w):
    return (v[0] + w[0], v[1] + w[1])


def absmanhattan(v):
    return abs(v[0]) + abs(v[1])


if __name__ == '__main__':
    main()
