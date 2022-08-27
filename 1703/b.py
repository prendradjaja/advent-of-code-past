UP = (-1, 0)
DOWN = (1, 0)
LEFT = (0, -1)
RIGHT = (0, 1)


def main():
    puzzle_input = 325489

    my_spiral = spiral(999999)
    next(my_spiral)  # Skip the first value since it's a special case...
    values = {(0, 0): 1}  # ...and put its value in the dict at init instead
    for pos in my_spiral:
        new_value = sum(values.get(neighbor, 0) for neighbor in neighbors(pos))
        values[pos] = new_value
        if new_value > puzzle_input:
            break

    print(new_value)


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


def neighbors(pos):
    for offset in [
        (-1, -1), (-1, 0), (-1, 1),
        ( 0, -1),          ( 0, 1),
        ( 1, -1), ( 1, 0), ( 1, 1),
    ]:
        yield addvec(pos, offset)


if __name__ == '__main__':
    main()
