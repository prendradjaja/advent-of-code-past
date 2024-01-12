def main():
    bug_positions = frozenset(
        (0, (r, c))
        for r, line in enumerate(open('in').read().splitlines())
        for c, ch in enumerate(line)
        if ch == '#'
    )
    for i in range(200):
        bug_positions = step(bug_positions, i)
    print(len(bug_positions))


def step(bug_positions, step_index):
    max_depth = step_index + 1
    result = set()
    for pos in all_positions(max_depth):
        if pos in bug_positions:
            if count_live_neighbors(bug_positions, pos) == 1:
                result.add(pos)
            else:
                pass  # Bug dies
        else:
            if count_live_neighbors(bug_positions, pos) in [1, 2]:
                result.add(pos)  # Empty space becomes infested with a bug
            else:
                pass
    return frozenset(result)


def count_live_neighbors(bug_positions, pos):
    result = 0
    for neighbor_pos in neighbor_positions(pos):
        if neighbor_pos in bug_positions:
            result += 1
    return result


def addvec(v, w):
    return (v[0] + w[0], v[1] + w[1])


def neighbor_positions(pos):
    depth, rc = pos
    r, c = rc
    offsets = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    result = []
    for offset in offsets:
        r2, c2 = addvec(rc, offset)
        if r2 == c2 == 2:
            if offset == (-1, 0):
                result.extend([
                    (depth + 1, (4, 0)),
                    (depth + 1, (4, 1)),
                    (depth + 1, (4, 2)),
                    (depth + 1, (4, 3)),
                    (depth + 1, (4, 4)),
                ])
            elif offset == (1, 0):
                result.extend([
                    (depth + 1, (0, 0)),
                    (depth + 1, (0, 1)),
                    (depth + 1, (0, 2)),
                    (depth + 1, (0, 3)),
                    (depth + 1, (0, 4)),
                ])
            elif offset == (0, -1):
                result.extend([
                    (depth + 1, (0, 4)),
                    (depth + 1, (1, 4)),
                    (depth + 1, (2, 4)),
                    (depth + 1, (3, 4)),
                    (depth + 1, (4, 4)),
                ])
                pass
            elif offset == (0, 1):
                result.extend([
                    (depth + 1, (0, 0)),
                    (depth + 1, (1, 0)),
                    (depth + 1, (2, 0)),
                    (depth + 1, (3, 0)),
                    (depth + 1, (4, 0)),
                ])
            else:
                raise Exception('unreachable case')
        elif not in_bounds_2d(r2, c2):
            if r2 == -1:
                result.extend([
                    (depth - 1, (1, 2))
                ])
            elif r2 == 5:
                result.extend([
                    (depth - 1, (3, 2))
                ])
            elif c2 == -1:
                result.extend([
                    (depth - 1, (2, 1))
                ])
            elif c2 == 5:
                result.extend([
                    (depth - 1, (2, 3))
                ])
            else:
                raise Exception('unreachable case')
        else:
            neighbor = (depth, (r2, c2))
            result.append(neighbor)
    return result


def in_bounds_2d(r, c):
    return (
        0 <= r < 5 and
        0 <= c < 5
    )


def all_positions(max_depth):
    for r in range(5):
        for c in range(5):
            if not (r == c == 2):
                for depth in range(-max_depth, max_depth+1):
                    yield (depth, (r, c))


if __name__ == '__main__':
    main()
