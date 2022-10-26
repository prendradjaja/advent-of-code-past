import hashlib


puzzle_input = 'qtetzkpl'


def md5(s):
    return hashlib.md5(s.encode('utf-8')).hexdigest()


def get_doors(path):
    result = []
    for direction, ch in zip('UDLR', md5(puzzle_input + path)[:4]):
        if ch in 'bcdef' and endpoint_is_in_bounds(path + direction):
            result.append(direction)
    return result


def get_endpoint(path):
    r, c = 0, 0
    for ch in path:
        if ch == 'U':
            r -= 1
        elif ch == 'D':
            r += 1
        elif ch == 'L':
            c -= 1
        elif ch == 'R':
            c += 1
        else:
            1/0
    return r, c


def endpoint_is_in_bounds(path):
    r, c = get_endpoint(path)
    return (
        0 <= r < 4 and
        0 <= c < 4
    )


def bfs(node):
    q = [node]
    while q:
        node = q.pop(0)
        for direction in get_doors(node):
            neighbor = node + direction
            if get_endpoint(neighbor) == (3, 3):
                return neighbor
            q.append(neighbor)


print(bfs(''))
